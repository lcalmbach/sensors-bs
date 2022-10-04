import streamlit as st
import pandas as pd
from datetime import datetime, date

import const as cn
import plots
from queries import qry
import database as db
import helper
from config.sensor import SENSORS_DICT
from config.time_agg import TIME_AGG_DICT


_v = [SENSORS_DICT[x]['label'] for x in SENSORS_DICT]
_k = [x for x in SENSORS_DICT]
SENSOR_OPTIONS_DICT = dict(zip(_k, _v))
SENSORS = list(SENSORS_DICT.keys())


class App:
    def __init__(self):
        self.df = pd.DataFrame()
        self.show_map = True
        self.show_ts = True
        self.show_histogram = True

    def init_data(self, sensor: str):
        """
        reads the sensor-datatable from the database and fills the list of all stations.
        reads the plot default settings from the sensor dictionary 
        
        :param sensor: sensor object 
        :return: None
        """

        def get_time_min_max():
            sql = qry['min_max_time'].format(sensor['db_table'])
            df, ok, err_msg = db.execute_query(sql)
            return (df.iloc[0]['min'].to_pydatetime(),
                    df.iloc[0]['max'].to_pydatetime(),)

        def get_stations():
            sql = qry['stations_all'].format(self.sensor['station_db_table'])
            df, ok, err_msg = db.execute_query(sql)
            return df

        self.stations_df = get_stations()
        self.all_stations_dict = dict(zip(self.stations_df.station_id,
                                          self.stations_df.id_name))
        self.time_interval = get_time_min_max()
        self.years_interval = (self.time_interval[0].year,
                               self.time_interval[1].year)
        self.years = range(self.years_interval[0], self.years_interval[1] + 1)

    # @st.cache()
    def get_map_data(self):
        # 0:time_field_name, 1:agg-func, 2:value_field_name, 3:data_table_name, 4:station_table_name, 5:time_value
        sql = qry['map_data'].format(self.time_agg['time_selector_field'],
                                     self.sensor['map_config']['station_agg_function'],
                                     self.sensor['db_table'],
                                     self.sensor['station_db_table'],
                                     self.sel_time_interval,
                                     self.get_filter(),
                                     self.sel_field)
        df, ok, err_msg = db.execute_query(sql)
        return df
    
    def get_histo_data(self):
        # value_field, data_table_name, time_field_name, time_value, additional_filters
        sql = qry['histo_data'].format(self.sel_field,
                                     self.sensor['db_table'],
                                     self.time_agg['time_selector_field'],
                                     self.sel_time_interval,
                                     self.get_filter())
        df, ok, err_msg = db.execute_query(sql)
        return df

    def get_filter(self):
        add_crit = ''
        if self.sel_stations_list:
            add_crit = f""" AND t2.station_id in ('{"', '".join(self.sel_stations_list)}') """
        if self.sel_hours != [0, 23]:
            add_crit += f" AND hour >= {self.sel_hours[0]} and hour <= {self.sel_hours[1]} "
        return add_crit


    def get_time_data(self, ts_agg):
        qry_key = self.time_agg['ts_query'][ts_agg]
        cfg = self.sensor['timeseries_config']
        if ts_agg in [cn.TSAggregation.NONE.value, cn.TSAggregation.BAND.value]:
            # 0: date_column 1: data_table 2: station_table, 3: date_filter_field, 4: date_filter_value, 5: additional filters
            sql = qry[qry_key].format(cfg['ts_time_field'][self.time_agg['key']],
                                                      self.sensor['db_table'],
                                                      self.sensor['station_db_table'],
                                                      self.time_agg['key'],
                                                      f"{self.sel_time_interval.strftime(cn.YMD_FORMAT)}",
                                                      self.get_filter(),
                                                      self.sel_field)
            df, ok, err_msg = db.execute_query(sql)

        # 0:aggregation function, 1:data_table_name, 2:station_table_name 3:time query ifeld, 4: time_value, 5 additional filters
        elif ts_agg == cn.TSAggregation.MEAN.value:  # no aggregation
            # 0: date_column 1: data_table 2: station_table, 3: date_filter_value,4: additional filters
            sql = qry['time_data_average_all'].format(cfg['ts_time_field'][self.time_agg['key']],
                                                      self.sensor['db_table'],
                                                      self.sensor['station_db_table'],
                                                      self.time_agg['key'],
                                                      f"'{self.sel_time_interval.strftime(cn.YMD_FORMAT)}'",
                                                      self.get_filter(),
                                                      self.sel_field)
            df, ok, err_msg = db.execute_query(sql)
        else:
            df = pd.DataFrame()
        df[cfg['y']] = df[cfg['y']].round(cfg['y_digits'])
        df['zeit'] = df[cfg['x']].dt.strftime('%d.%m.%Y %H:%M')
        return df


    def get_time_interval(self):
        """
        Retrieves a selected date or range of dates to show time-aggregated data on the plots: valid aggregations are:
        date, week_date, month_date and year. The method extracts the list of dates required for the currently selected
        aggregation and retrieves the selection from the user via a slider for dates and a selectbox for the other time 
        aggregation intervals,

        Returns:
            pd.DataFrame: selection from the time aggregation dict
        """            
        def get_options() -> dict:
            """
            generates a dictionary of values for week_date, month_date and year_date aggregations

            Returns:
                dict: dict with format : {'2022-09-22': '2022-37'} used in st.selectbox
            """            
            # 0: aggregation date, 1: 1: label, e.g. concat(year, 'week'), 2: data table
            
            if self.time_agg['key'] == 'year_date':
                sql = qry['date_aggregation_list'].format(self.time_agg['key'], 
                                                        "year", 
                                                        self.sensor['db_table'])
            else:
                sql = qry['date_aggregation_list'].format(self.time_agg['key'], 
                                                        f"concat(year, '-', {self.time_agg['second_label_field']})", 
                                                        self.sensor['db_table'])
            _df, ok, err_msg = db.execute_query(sql)
            _result_dict = dict(zip(_df['key'], _df['value']))
            return _result_dict

        if self.time_agg['key'] == 'date':
            result = st.slider(self.time_agg['slider_label'],
                               min_value=self.time_interval[0],
                               max_value=self.time_interval[1],
                               value=self.time_interval[1])
        else:
            dict_options = get_options()
            default_value = list(dict_options.keys())[len(list(dict_options.keys()))-1]
            
            result = st.select_slider(self.time_agg['label'],
                                  options=list(dict_options.keys()),
                                  format_func=lambda x: dict_options[x],
                                  value = default_value)

        return result


    def explorer(self):
        def get_tooltip_html() -> str:
            result = f"""<b>Station:</b> {{}}<br/>
            <b>Name:</b> {{}}<br/>
            <b>{'value'}:</b>{{}}<br/>"""
            return result

        def get_metric_label():
            def get_aggregation():
                time_key = self.time_agg['key']
                agg_func = self.sensor['map_config']['station_agg_function']
                result = cn.METRIC_LABEL_DICT[time_key][agg_func]
                return result

            def get_time_expression():
                if self.time_agg['key'] == 'date':
                    time = f"am {self.sel_time_interval.strftime(cn.DMY_FORMAT)}"
                elif self.time_agg['key'] == 'week_date':
                    time = f"Woche {self.sel_time_interval.strftime('%V')}, "
                    dates = helper.get_date_range_from_weekno(int(self.sel_time_interval.strftime('%Y')), 
                                                                int(self.sel_time_interval.strftime('%U'))
                                                                )
                    time += f" ({dates[0].strftime(cn.DMY_FORMAT)} - {dates[1].strftime(cn.DMY_FORMAT)})"
                elif self.time_agg['key'] == 'month_date':
                    time = f"Monat {self.sel_time_interval.strftime('%b')} {self.sel_time_interval.strftime('%Y')}"
                elif self.time_agg['key'] == 'year_date':
                    time = f"Jahr {self.sel_time_interval.year}"
                return time
            
            aggregation = get_aggregation()
            time = get_time_expression()

            result = f"{aggregation} {self.sensor['label']}, {time}"
            return result

        self.sel_time_interval = self.get_time_interval()
        # filter stations and hours from map filter to get the base dataframe
        map_df = self.get_map_data()

        if len(map_df) == 0:
            st.info("Es wurden keine Messungen für diesen Filter gefunden")
        else:
            stats = map_df['value'].agg(['min', 'max', 'mean', 'std'])
            st.metric(label = get_metric_label(), value=f'{stats[2]:.1f} ({stats[0]:.1f} - {stats[1]:.1f})')
            plot_index = 0
            plot_cols = st.columns(2)
            if self.show_map:
                cfg = self.sensor['map_config']
                with plot_cols[plot_index]:
                    cfg['tooltip_html'] = get_tooltip_html()
                    cfg['html_fields'] = ['station_id', 'name', 'value']
                    plots.plot_colormap(map_df, cfg)
                    fig_text = cfg['fig_text'][cfg['station_agg_function']].format(self.time_agg['title'])
                    st.markdown(fig_text)
                    plot_index += 1

            if self.show_histogram:
                histo_df = self.get_histo_data() if self.histo_values == 0 else map_df
                cfg = self.sensor['histogram_config']
                self.sensor['histogram_config']['tooltip_html'] = get_tooltip_html()
                with plot_cols[plot_index]:
                    plots.histogram(histo_df, self.sensor['histogram_config'])
                    fig_text = cfg['fig_text'][self.sensor['map_config']['station_agg_function']].format(len(map_df))
                    st.markdown(fig_text)
                    plot_index += 1
                    plot_index = plot_index % 2

            if self.show_ts:
                cfg = self.sensor['timeseries_config']
                ts_agg = cfg['aggregate_stations']
                cfg['x'] = cfg['ts_time_field'][self.time_agg['key']]
                cfg['y_title'] = self.sensor['label']
                ts_df = self.get_time_data(ts_agg)
                cfg['tooltip'] = ['zeit', cfg['y']]
                cfg['y_domain'] = [ts_df['value'].min() - 5, ts_df['value'].max() + 5]
                cfg['x_format'] = cfg['ts_time_format'][self.time_agg['key']]
            
            if cfg['aggregate_stations'] == cn.TSAggregation.NONE.value:
                cfg['color'] = 'station'
                cfg['tooltip'].insert(0, 'station')
            if cfg['aggregate_stations'] == cn.TSAggregation.BAND.value:
                plots.confidence_band(ts_df, cfg)
            else:
                plots.time_series_line(ts_df, cfg)
            fig_text = cfg['fig_text'][self.sensor['map_config']['station_agg_function']].format(len(map_df))
            st.markdown(fig_text)

    def show_menu(self):
        self.sensor = SENSORS_DICT[st.sidebar.selectbox('Sensor', options=list(SENSOR_OPTIONS_DICT.keys()),
                                                        format_func=lambda x: SENSOR_OPTIONS_DICT[x])]
        if len(self.sensor['fields']) > 1:
            self.sel_field = st.sidebar.selectbox('Wert', 
                                        options=list(self.sensor['fields'].keys()),
                                        format_func=lambda x:
                                        self.sensor['fields'][x]
                                    )
        else:
            self.sel_field = list(self.sensor['fields'].keys())[0] 

        self.init_data(self.sensor)
        with st.sidebar.expander('⚙️Settings', expanded=True):
            self.time_agg  = cn.TIME_AGG_DICT[st.selectbox('Zeitliche Aggregation', list(cn.AGG_OPTIONS_DICT.keys()),
                                                          format_func=lambda x: cn.AGG_OPTIONS_DICT[x])]
            tabs = st.tabs(["Karte", "Histogramm", "Zeitreihe"])
            with tabs[0]:
                self.sensor['map_config']['station_agg_function'] = st.selectbox('Aggregation Karte', 
                                                                        options=self.sensor['agg_functions'],
                                                                        format_func=lambda x:
                                                                        cn.AGG_FUNCTION_DICT[x]
                                                                    )
                

            with tabs[1]:
                self.show_histogram = st.checkbox('Zeige Histogramm',
                                                  value=self.show_histogram)
                self.histo_values = st.selectbox('Basis', options=cn.HiSTO_VALUES_DICT,
                                                                        format_func=lambda x:
                                                                        cn.HiSTO_VALUES_DICT[x],
                                                                        help=cn.HELP_DICT['histo_basis'])
            with tabs[2]:
                self.show_ts = st.checkbox(label='Zeige Zeitreihe',
                                           value=self.show_ts)
                self.sensor['timeseries_config']['aggregate_stations'] = st.selectbox("Aggregiere Stationen",
                                                                                      list(
                                                                                          cn.TIME_SERIES_AGGREGATION_DICT.keys()),
                                                                                      format_func=lambda x:
                                                                                      cn.TIME_SERIES_AGGREGATION_DICT[x])

            # self.summary = st.checkbox('Zeige Zusammenfassung')
        with st.sidebar.expander('🔎 Filter (Karte)', expanded=True):
            self.sel_stations_list = st.multiselect("Auswahl Stationen", options=list(self.all_stations_dict.keys()),
                                                    format_func=lambda x: self.all_stations_dict[x])
            self.sel_hours = st.slider("Tageszeit", min_value=0, max_value=23, value=[0, 23])
        self.explorer()
