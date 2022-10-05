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
    'date': {'avg': 'Tagesmittel', 'min': 'Tages-Minimum', 'max': 'Tages-Maximum',
            'std': 'Tages-Standardardabweichung', 'sum': 'Tages-Total'},
    'week_date': {'avg': 'Wochenmittel', 'min': 'Wochen-Minimum', 'max': 'Wochen-Maximum',
              'std': 'Wochen-Standardardabweichung', 'sum': 'Wochen-Total'},
    'month_date': {'avg': 'Monatsmittel', 'min': 'Monats-Minimum', 'max': 'Monats-Maximum',
              'std': 'Monats-Standardardabweichung', 'sum': 'Monats-Total'},
    'year_date': {'avg': 'Jahresmittel', 'min': 'Jahres-Minimum', 'max': 'Jahres-Maximum',
             'std': 'Jahres-Standardardabweichung', 'sum': 'Jahrs-Total'}
}

GRID_ROW_HEIGHT = 30
DMY_FORMAT = "%d.%m.%Y"
YMD_FORMAT = "%Y-%m-%d"

TIME_SERIES_AGGREGATION_DICT = {0: 'keine Aggregation', 1: 'Mittelwert', 2: 'Werteband (Standardabweichung)'}
HiSTO_VALUES_DICT = {0: 'Einzelwerte', 1: 'Aggregierte Werte'}


HELP_DICT = {
    'histo_basis': "Aggregierte Werte = Auf Karte pro Station aggregierter Werte (1 pro STation), Einzelwerte: jeder einzelne Messwert im Zeitintervall (n pro Station)"
}
TIME_SELECTION_DICT = {
    0: "Nur Werte aus diesem Zeitraum", 1: "Keine Werte aus diesem Zeitraum"
}