import streamlit as st
import pandas as pd
from datetime import datetime, date
import const as cn
import plots

class App():
    def __init__(self):
        pass
        
    
    def init_data(self):
        self.df = self.get_data(self.sensor)
        self.stations_df = self.get_stations()
        self.stations = list(self.stations_df['station_id'])
        self.min_date = self.df['date'].min()
        self.max_date = self.df['date'].max()
        self.min_year = self.df['date'].min().year
        self.max_year = self.df['date'].max().year

    @st.cache()
    def get_data(self, sensor):
        def add_time_aggregation_fields(df):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['date'] = pd.to_datetime(df['timestamp']).dt.date
            df['date'] = pd.to_datetime(df['date'])
            df['week_date'] = df['date'] - pd.offsets.Week(weekday=6)
            df['week'] = df['date'].dt.week
            df['day'] = 15
            df['month'] = df['date'].dt.month
            df['year'] = df['date'].dt.year
            df['month_date'] = pd.to_datetime(df[['year','month','day']])
            df['day'] = pd.to_datetime(df['timestamp']).dt.day
            df['hour'] = df['timestamp'].dt.hour
            df['date_hour'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
            return df

        def get_air_temp():
            min_temp, max_temp = -50, 60
            df = pd.read_parquet(cn.datasource['smart-climate'])
            df = add_time_aggregation_fields(df)
            # filter 125°C values
            df = df[(df['air_temp'] > min_temp) & (df['air_temp'] < max_temp)]
            return df

        def get_noise():
            df = pd.read_parquet(cn.datasource['smart-noise'])
            df = add_time_aggregation_fields(df)
            return df
        
        if sensor['label'] == cn.SENSORS[0]:
            df = get_air_temp()
        elif sensor['label'] == cn.SENSORS[2]:
            df = get_noise()
        return df
    

    @st.cache()
    def get_stations(self):
        key = cn.datasource[self.sensor['data-source-station']]
        df = pd.read_parquet(key)
        df = df[(df['lat'] > 0) & (df['long'] > 0)]
        return df
    

    @st.cache()
    def aggregate_data(self, base_df):
        df = pd.merge(base_df, self.stations_df, left_on=['station_id'], right_on=['station_id'], how='right')
        df = df[self.sensor['group_fields'] + [cn.AGG_FIELD_DICT[self.aggregation], self.sensor['field']]].groupby(self.sensor['group_fields']+ [cn.AGG_FIELD_DICT[self.aggregation]]).agg(['min','max','mean','std']).reset_index()
        df.columns = ['station_id','name', 'lat', 'long', cn.AGG_FIELD_DICT[self.aggregation],'min', 'max', 'mean', 'std']
        df[['min','max','mean', 'std']] = df[['min','max','mean','std']].astype(float).round(decimals = 2)
        return df


    @st.cache()
    def get_df_map_base(self, sel_stations, sel_hours):
        result = self.df
        if sel_stations != []:
            result = result[result['station_id'].isin(sel_stations)]
        if sel_hours != [0,23]:
            result = result[(result['hour'] >= sel_hours[0]) & (result['hour'] <= sel_hours[1])]
        return result


    def get_time_interval(self):
        if self.aggregation == 'Tag':
            result = st.slider('Datum',
                min_value=self.min_date.to_pydatetime(),
                max_value=self.max_date.to_pydatetime(),
                value=self.max_date.to_pydatetime()
            )
        elif self.aggregation=='Woche':
            _df = self.df[['year','week','week_date']].drop_duplicates().sort_values(by='week_date')
            _df = _df.sort_values('week_date', ascending=False)
            _df['label'] = _df.agg(lambda x: f"{x['year']}-{x['week']}", axis=1)
            _df.set_index('week_date', inplace=True)
            dict_weeks = _df['label']
            result = st.selectbox(self.aggregation, 
                options=list(dict_weeks.keys()),
                format_func=lambda x:dict_weeks[x])
        elif self.aggregation=='Monat':
            _df = self.df[['year','month','month_date']].drop_duplicates().sort_values(by='month_date')
            _df = _df.sort_values('month_date', ascending=False)
            _df['label'] = _df.agg(lambda x: f"{x['year']}-{x['month']}", axis=1)
            _df.set_index('month_date', inplace=True)
            dict_months = _df['label']
            result = st.selectbox('Monat', 
                options=list(dict_months.keys()),
                format_func=lambda x:dict_months[x])
        elif self.aggregation=='Jahr':
            _df = self.df[['year']].drop_duplicates().sort_values(by='year')
            _df = _df.sort_values('year', ascending=False)
            result = st.selectbox(self.aggregation, 
                options=list(_df['year'])
            )
        return result

    def show_map(self):
        def get_tooltip_html():
            result = f"""<b>Station:</b> {{}}<br/><b>Name:</b> {{}}<br/><b>{self.sensor['field']}:</b> {{}}<br/>"""
            return result

        def get_min_max_records(df):
            stats = df[cn.AGG_FUNCTION_DICT[self.map_agg_function]].agg(['min', 'max'])
            df = df[df[cn.AGG_FUNCTION_DICT[self.map_agg_function]].isin([stats[0], stats[1]])]
            return df

        def get_metric_label():
            if self.aggregation == 'Tag':
                time = f"am {self.sel_time_interval.strftime(cn.DMY_FORMAT)}"
            elif self.aggregation == 'Woche':
                time = f"Woche {self.sel_time_interval.strftime('%V')} {self.sel_time_interval.strftime('%Y')}"
            elif self.aggregation == 'Monat':
                time = f"Monat {self.sel_time_interval.strftime('%b')} {self.sel_time_interval.strftime('%Y')}"
            elif self.aggregation == 'Jahr':
                time = f"{self.sel_time_interval}"
            result = f"{self.sensor['label']}, {cn.METRIC_LABEL_DICT[self.aggregation][self.map_agg_function]} {time}"
            return result

        self.sel_time_interval = self.get_time_interval()
        # filter stations and hours from map filter to get the base dataframe
        self.df_map_base = self.get_df_map_base(self.sel_stations,self.sel_hours)
        df = self.aggregate_data(self.df_map_base) 
        df = df[df[cn.AGG_FIELD_DICT[self.aggregation]] == self.sel_time_interval]
        if self.min_max:
            df = get_min_max_records(df)
        settings = {
            'lat': 'lat',
            'long': 'long',
            'value_col': cn.AGG_FUNCTION_DICT[self.map_agg_function],
            'station_col': 'station_id',
            'min_val': 0,
            'max_val': 10,
            'station_id':'station_id',
            'size': 50, 
            'tooltip_html': get_tooltip_html(),
            'html_fields': ['station_id','name', cn.AGG_FUNCTION_DICT[self.map_agg_function]]
        }
        stats = df[cn.AGG_FUNCTION_DICT[self.map_agg_function]].agg(['min', 'max', 'mean', 'std'])

        st.metric(label=get_metric_label(), value= f'{stats[2]:.1f} ({stats[0]} - {stats[1]})')
        if self.map:
            plots.plot_colormap(df, settings)
        if self.histogram:
            df = self.df_map_base[self.df_map_base['date'] == self.sel_time_interval]
            settings = {
                'x': self.sensor['field'],
                'title':'Histogramm von {cn.AGG_FUNCTION_DICT[self.map_agg_function]}',
                'x_title': '',
                'y_title': 'Anzahl',
                'bins': 20,
                'x_domain':[0.100],
                'width': 800,
                'height': 400,
                'tooltip_html' : get_tooltip_html()}
            plots.histogram(df, settings)
        if self.timeseries:
            sel_stations = st.multiselect("Selektion Stationen", options=self.stations, help='Wird keine Auswahl getroffen, wird der Mittelwert aller Stationen angezeigt.')
            date_field = 'timestamp'
            title = ''
            if self.aggregation == 'Tag':
                if sel_stations==[]:
                    date_field = 'date_hour'
                    df = self.df_map_base[self.df_map_base['date'] == self.sel_time_interval][[date_field, self.sensor['field']]].groupby([date_field]).agg(['mean']).reset_index()
                    df.columns = [date_field, self.sensor['field']]
                    title = 'Stundenmittel aller Stationen'
                else:
                    df = self.df_map_base[(self.df_map_base['station_id'].isin(sel_stations)) & (self.df['date'] == self.sel_time_interval)]
                    title = f'Zeitreihen von {df.station_id.nunique()} Stationen' 
            elif self.aggregation == 'Woche':
                if sel_stations==[]:
                    date_field = 'date_hour'
                    df = self.df_map_base[self.df_map_base['week_date'] == self.sel_time_interval][[date_field, self.sensor['field']]].groupby([date_field]).agg(['mean']).reset_index()
                    df.columns = [date_field, self.sensor['field']]
                else:
                    df = self.df_map_base[(self.df_map_base['station_id'].isin(sel_stations)) & (self.df_map_base['week_date'] == self.sel_time_interval)]
            elif self.aggregation == 'Monat':
                df = self.df_map_base[(self.df_map_base['station_id'].isin(sel_stations)) & (self.df_map_base['month_date'] == self.sel_time_interval)]
                #df = df[['station_id','date', self.sensor['field']]].groupby(['station_id','date']).agg(['mean']).reset_index()
                #df.columns=['station_id', 'date', self.sensor['field']]
            elif self.aggregation == 'Jahr':
                if sel_stations==[]:
                    pass
                else:
                    date_field = 'date'
                    df = self.df_map_base[(self.df_map_base['station_id'].isin(sel_stations)) & (self.df_map_base['date'].dt.year == self.sel_time_interval)]
                    df = df[['station_id','date', self.sensor['field']]].groupby(['station_id','date']).agg(['mean']).reset_index()
                    df.columns=['station_id', 'date', self.sensor['field']]
            settings = {
                'x': date_field, 
                'y': self.sensor['field'],
                'title': title,
                'width': 800,
                'height': 400,
                'x_title': '',
                'y_title': self.sensor['label'],
                'y_domain': [df[self.sensor['field']].min()-1, df[self.sensor['field']].max()+1],
                'tooltip': [date_field, self.sensor['field']], 
                'marker_size': 30
            }
            if sel_stations != []:
                settings['tooltip'].append('station_id')
                settings['color'] = 'station_id'
            plots.time_series_line(df,settings)
        #if self.summary:
        #    pass


    def show_menu(self):
        self.sensor = cn.SENSORS_DICT[st.sidebar.selectbox('Sensor', options=cn.SENSORS)]
        self.init_data()
        with st.sidebar.expander('🔎 Filter (Karte)'):
            self.sel_stations = st.multiselect("Auswahl Stationen", options=self.stations)
            self.sel_hours = st.slider("Tageszeit", min_value=0,max_value=23,value=[0,23])
        with st.sidebar.expander('⚙️Settings'):
            self.aggregation = st.selectbox('Zeitliche Aggregation', options=self.sensor['time_agg'], index=1)
            self.map_agg_function = st.selectbox('Aggregation Karte', options=self.sensor['map_agg'])
            self.min_max = st.checkbox('Zeige Minimum/Maximum')
            self.map = st.checkbox('Zeige Karte', value=True)
            self.histogram = st.checkbox('Zeige Histogramm')
            self.timeseries = st.checkbox('Zeige Zeitreihe')
            #self.summary = st.checkbox('Zeige Zusammenfassung')
        
        
        self.show_map()