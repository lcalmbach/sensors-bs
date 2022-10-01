from enum import Enum

class TSAggregation(Enum):
    NONE = 0
    MEAN = 1
    BAND = 2
    
TIME_AGG_DICT = {
    'date': {
        'key': 'date',
        'title': 'Tages',
        'slider_label': 'Wähle ein Datum',
        'label': 'Datum',
        'time_selector_field': 'date',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date','value'], 
                        TSAggregation.MEAN.value: ['date','value'], 
                        TSAggregation.BAND.value: ['date','value'], 
                    },
    },
    'week_date': {
        'key': 'week_date',
        'title': 'Wochen',
        'label': 'Jahr-Kalenderwoche',
        'slider_label': 'Wähle eine Woche',
        'second_label_field': 'week',
        'time_selector_field': 'date',
        'ts_time_field': 'date',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date','value'], 
                        TSAggregation.MEAN.value: ['hour_date','value'], 
                        TSAggregation.BAND.value: ['hour_date','value']
                    },
    },
    'month_date': {
        'key': 'month_date',
        'title': 'Monats',
        'label': 'Wähle einen Monat',
        'second_label_field': 'month',
        'time_selector_field': 'date',
        'ts_time_field': 'date',
        'ts_query': {TSAggregation.NONE.value: 'time_date_stations_raw', 
                        TSAggregation.MEAN.value: 'time_data_average_all',
                        TSAggregation.BAND.value: 'time_date_stations_raw'
                    },
        'ts_tooltip': {TSAggregation.NONE.value: ['station','date','value'], 
                        TSAggregation.MEAN.value: ['date','value'], 
                        TSAggregation.BAND.value: ['date','value']
                    },
    },

    'year_date': {
        'key': 'year_date',
        'title': 'Jahres',
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