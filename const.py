config = 's3'
base= {'local':'./data/',
        's3': 'https://lc-opendata01.s3.amazonaws.com/'}
datasource = {
        'smart-noise':f'{base[config]}100087.gzip', 
        'smart-noise-station':f'{base[config]}100087-station.gzip', 
        'smart-climate':f'{base[config]}100009.gzip', 
        'smart-climate-station':f'{base[config]}100009-station.gzip', 
        
    }

SENSORS_DICT = {
    'Lufttemperatur [°C]':{
        'data-source': 'smart-climate',
        'data-source-station': 'smart-climate-station',
        'field':'air_temp',
        'label':'Lufttemperatur [°C]',
        'group_fields': ['station_id','name', 'lat', 'long'],
        'time_agg': ['Stunde', 'Tag', 'Woche', 'Monat', 'Jahr'],
        'map_agg': ['Mittelwert', 'Minimum','Maximum', 'Standard Abweichung']
    },
    'Niederschlag [mm]':{
        'data-source': 'smart-climate',
        'field':'diff_prec',
        'label':'Niederschlag [mm]',
        'group_fields': ['station_id','name', 'lat', 'long'],
        'time_agg': ['Stunde', 'Tag', 'Woche', 'Monat', 'Jahr'],
        'map_agg': ['Mittelwert', 'Minimum','Maximum', 'Standard Abweichung']
    },
    'Lärm [db]':{
        'data-source': 'smart-noise',
        'data-source-station': 'smart-noise-station',
        'field':'mean_noise',
        'label': 'Lärm [db]',
        'group_fields': ['station_id','name', 'lat', 'long'],
        'time_agg': ['Stunde', 'Tag', 'Woche', 'Monat', 'Jahr'],
        'map_agg': ['Mittelwert', 'Minimum','Maximum', 'Standard Abweichung']
    },
}

# defines which time field should be used for a given aggregation on the map
# e.g. if aggregation level on the map is day, then the raw data is shown: timestamp
TS_FIELD_DICT = {'Tag':'timestamp', 'Woche':'timestamp', 'Monat':'date', 'Jahr':'week_date'}

AGG_FIELD_DICT = {
        'Tag': 'date', 
        'Woche': 'week_date', 
        'Monat': 'month_date', 
        'Jahr': 'year'
}
AGG_FUNCTION_DICT = {
    'Mittelwert': 'mean',
    'Minimum': 'min',
    'Maximum': 'max', 
    'Standard Abweichung': 'std'
}

METRIC_LABEL_DICT = {
    'Tag': {'Mittelwert': 'Tagesmittel', 'Minimum': 'Tages-Minimum', 'Maximum':'Tages-Maximum', 'Standard Abweichung': 'Tages-Standardardabweichung'},
    'Woche': {'Mittelwert': 'Wochenmittel', 'Minimum': 'Wochen-Minimum', 'Maximum':'Wochen-Maximum', 'Standard Abweichung': 'Wochen-Standardardabweichung'},
    'Monat': {'Mittelwert': 'Monatsmittel', 'Minimum': 'Monats-Minimum', 'Maximum':'Monats-Maximum', 'Standard Abweichung': 'Monats-Standardardabweichung'},
    'Jahr': {'Mittelwert': 'Jahresmittel', 'Minimum': 'Jahres-Minimum', 'Maximum':'JAhres-Maximum', 'Standard Abweichung': 'Jahres-Standardardabweichung'}
}

SENSORS = list(SENSORS_DICT.keys())
GRID_ROW_HEIGHT = 30
DMY_FORMAT = "%d.%m.%Y"