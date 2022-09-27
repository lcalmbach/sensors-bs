from enum import Enum

class TSAggregation(Enum):
    NONE = 0
    MEAN = 1
    BAND = 2

TIME_AGG_DICT = {
    'date': {
        'key': 'date',
        'label': 'Datum',
        'time_selector_field': 'date',
        'map_time_field': 'date',
        'ts_time_field': 'date_hour',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date_hour','value'], 
                        TSAggregation.MEAN.value: ['date_hour','value'], 
                        TSAggregation.BAND.value: ['date_hour','value'], 
                    },
    },
    'week_date': {
        'key': 'week_date',
        'label': 'Jahr-Kalenderwoche',
        'second_label_field': 'week',
        'time_selector_field': 'date',
        'ts_time_field': 'date_hour',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date_hour','value'], 
                        TSAggregation.MEAN.value: ['date_hour','value'], 
                        TSAggregation.BAND.value: ['date_hour','value'], 
                    },
    },
    'month_date': {
        'key': 'month_date',
        'label': 'Jahr-Monat',
        'second_label_field': 'month',
        'time_selector_field': 'date',
        'ts_time_field': 'date_hour',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date_hour','value'], 
                        TSAggregation.MEAN.value: ['date_hour','value'], 
                        TSAggregation.BAND.value: ['date_hour','value'], 
                    },
    },

    'year_date': {
        'key': 'year_date',
        'label': 'Jahr',
        'second_label_field': 'year',
        'time_selector_field': 'data',
        'ts_time_field': 'date',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date','value'], 
                        TSAggregation.MEAN.value: ['date','value'], 
                        TSAggregation.BAND.value: ['date','value'], 
                    }
    },
}


# used for  options list
_v = [TIME_AGG_DICT[x]['label'] for x in TIME_AGG_DICT]
_k = [x for x in TIME_AGG_DICT]
AGG_OPTIONS_DICT = dict(zip(_k, _v))

AGG_FUNCTION_DICT = {
    'avg': 'Mittelwert',
    'min': 'Minimum',
    'max': 'Maximum',
    'std': 'Standard Abweichung'
}

METRIC_LABEL_DICT = {
    'Tag': {'Mittelwert': 'Tagesmittel', 'Minimum': 'Tages-Minimum', 'Maximum': 'Tages-Maximum',
            'Standard Abweichung': 'Tages-Standardardabweichung'},
    'Woche': {'Mittelwert': 'Wochenmittel', 'Minimum': 'Wochen-Minimum', 'Maximum': 'Wochen-Maximum',
              'Standard Abweichung': 'Wochen-Standardardabweichung'},
    'Monat': {'Mittelwert': 'Monatsmittel', 'Minimum': 'Monats-Minimum', 'Maximum': 'Monats-Maximum',
              'Standard Abweichung': 'Monats-Standardardabweichung'},
    'Jahr': {'Mittelwert': 'Jahresmittel', 'Minimum': 'Jahres-Minimum', 'Maximum': 'JAhres-Maximum',
             'Standard Abweichung': 'Jahres-Standardardabweichung'}
}

GRID_ROW_HEIGHT = 30
DMY_FORMAT = "%d.%m.%Y"
YMD_FORMAT = "%Y-%m-%d"

TIME_SERIES_AGGREGATION_DICT = {0: 'keine Aggregation', 1: 'Mittelwert', 2: 'Werteband'}




