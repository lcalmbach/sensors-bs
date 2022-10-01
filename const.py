from enum import Enum
from config.time_agg import TIME_AGG_DICT

class TSAggregation(Enum):
    NONE = 0
    MEAN = 1
    BAND = 2


# used for  options list
_v = [TIME_AGG_DICT[x]['label'] for x in TIME_AGG_DICT]
_k = [x for x in TIME_AGG_DICT]
AGG_OPTIONS_DICT = dict(zip(_k, _v))

AGG_FUNCTION_DICT = {
    'avg': 'Mittelwert',
    'min': 'Minimum',
    'max': 'Maximum',
    'std': 'Standard Abweichung',
    'sum': 'Summe'

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




