SENSORS_DICT = {
    'air_temp': {
        'key': 'air_temp',
        'fields': {'air_temp': 'Lufttemperatur',},
        'label': 'Lufttemperatur [°C]',
        'station_db_table': "T_100009_station",
        'agg_functions': ['avg','min','max'],
        'db_table': "T_100009_temperature",
        'map_config': {
            'station_agg_function': 'avg',
            'lat': 'lat',
            'long': 'long',
            'station_col': 'station_id',
            'value_col': 'value',
            'width': 600,
            'height': 600,
            'fig_text': {'avg': 'Mittlere {} Lufttemperatur [°C] pro Station',
                            'min': 'Minimale {} Lufttemperatur [°C] pro Station',
                            'max': 'Maximale {} Lufttemperatur [°C] pro Station',
                            'std': 'Standardabweichung {} Lufttemperatur [°C] pro Station',
                        },
        },
        'histogram_config': {
            'x': 'value',
            'x_title': '',
            'y_title': 'Anzahl',
            'bins': 20,
            'x_domain': [0.100],
            'width': 600,
            'height': 400,
            'fig_text': {'avg': 'Histogramm der Durchschnitts-Lufttemperatur [°C] für {} Stationen.',
                            'min': 'Histogramm der minimalen Lufttemperatur [°C] für {} Stationen.',
                            'max': 'Histogramm der maximalen Lufttemperatur [°C] für {} Stationen.',
                            'std': 'Histogramm der Standardabweichung der Lufttemperatur [°C] pro Station'
                        }
        },
        'timeseries_config': {
            'y': 'value',
            'title': '',
            'x_title': '',
            'y_digits': 1,
            'color': 'station',
            'marker_size': 30,
            'ts_time_field': {'date': 'hour_date', 'week_date': 'hour_date', 'month_date': 'hour_date', 'year_date': 'date'},
            'ts_time_format': {'date': '%H:%M', 'week_date': '%d.%m.%Y', 'month_date': '%d.%m.%y', 'year_date': '%d.%m.%y'},
            'width': 1000,
            'height': 300,
            'fig_text': {'avg': 'Zeitreihe der Durchschnitts-Lufttemperatur [°C] für {} Stationen.',
                            'min': 'Histogramm der minimalen Lufttemperatur [°C] für {} Stationen.',
                            'max': 'Histogramm der maximalen Lufttemperatur [°C] für {} Stationen.',
                            'std': 'Histogramm der Standardaweichung der Lufttemperatur [°C] pro Station'
                        }
        },
        'intro': """**Lufttemperatur [°C]**<br>Die Lufttemperatur wird an {} Stellen mittels Sensoren der Firma [meteoblue](https://www.meteoblue.com/) gemessen. Die meisten Sensoren liefern Daten halbstündlich, diese Werte werden für die App als Stunden-Mittelwert aggregiert.<br>Quelle: [opendata.bs](https://data.bs.ch/explore/dataset/100009/information/)"""
    },
    'precipitation': {
        'key': 'precipitation',
        'fields': {'precipitation': 'Niederschlag',},
        'label': 'Niederschlag [mm]',
        'station_db_table': "T_100009_station",
        'db_table': "T_100009_prec",
        'agg_functions': ['sum'],
        'map_config': {
            'station_agg_function': 'avg',
            'lat': 'lat',
            'long': 'long',
            'station_col': 'station_id',
            'value_col': 'value',
            'station_id': 'station_id',
            'size': 50,
            'width': 600,
            'height': 600,
            'fig_text': {'avg': 'Mittlerer {} Niederschlag [°C] pro Station',
                            'min': 'Minimaler {} Niederschlag [°C] pro Station',
                            'max': 'Maximaler {} Niederschlag [°C] pro Station',
                            'sum': 'Summe {} Niederschlag [°C] pro Station'
                        }
        },
        'histogram_config': {
            'x': 'value',
            'x_title': '',
            'y_title': 'Anzahl',
            'bins': 20,
            'x_domain': [0.100],
            'width': 600,
            'height': 400,
            'fig_text': {'avg': 'Histogramm der Durchschnitts-Niederschlags [°C] für {} Stationen.',
                            'min': 'Histogramm des minimalen Niederschlags [°C] für {} Stationen.',
                            'max': 'Histogramm des maximalen Niederschlags [°C] für {} Stationen.',
                            'sum': 'Histogramm des Niederschlags [°C] pro Station, {} Stationen'
                        }
        },
        'timeseries_config': {
            'y': 'value',
            'title': '',
            'width': 1000,
            'height': 300,
            'x_title': '',
            'y_digits': 1,
            'color': 'station',
            'marker_size': 30,
            'ts_time_field': {'date': 'date', 'week_date': 'date', 'month_date': 'date', 'year_date': 'date'},
            'ts_time_format': {'date': '%H:%M', 'week_date': '%d.%m.%Y', 'month_date': '%d.%m.%y', 'year_date': '%d.%m.%y'}
        },
        'intro': """**Niederschlag [mm]**<br>Der Niederschlag wird an {} Stellen gemessen. Die Messung erfolgt in der Regel stündlich, kann aber auch unregelmässig erfolgen und es wird jeweils die Differenz zur letzten Messung in mm rapportiert. Um eine sinnvolle grafisch und numerische Aufbereitung er ermöglichen wurden die Differenzen der Werte pro Tag summiert, sodass Vergleiche pro Tag möglich sind, nicht aber für Stundenwerte.<br>Quelle: [opendata.bs](https://data.bs.ch/explore/dataset/100009/information/)"""
    },

     'noise': {
        'key': 'noise',
        'fields': {'min_noise': 'Lärm_min', 'max_noise': 'Lärm_max', 'mean_noise': 'Lärm_durchschn'},
        'label': 'Lärm [dB]',
        'station_db_table': "T_100087_station",
        'db_table': "T_100087",
        'agg_functions': ['avg','max','std'],
        'map_config': {
            'station_agg_function': 'avg',
            'lat': 'lat',
            'long': 'long',
            'station_col': 'station_id',
            'value_col': 'value',
            'min_val': 0,
            'max_val': 10,
            'station_id': 'station_id',
            'size': 50,
            'width': 600,
            'height': 600,
            'map_time_field': 'date',
            'fig_text': {'avg': 'Mittlere {} Lärmpegel [dB] pro Station',
                            'min': 'Minimaler {} Lärmpegel [dB] pro Station',
                            'max': 'Maximaler {} Lärmpegel [dB] pro Station',
                            'std': 'Standardabweichung des {} Lärmpegels [dB] pro Station'}
        },
        'histogram_config': {
            'x': 'value',
            'x_title': '',
            'y_title': 'Anzahl',
            'bins': 20,
            'x_domain': [0.100],
            'width': 600,
            'height': 400,
            'fig_text': {'avg': 'Histogramm der Durchschnitts-Lärmpegels [dB] für {} Stationen.',
                            'min': 'Histogramm des minimalen Lärmpegels [dB] für {} Stationen.',
                            'max': 'Histogramm des maximalen Lärmpegels [dB] für {} Stationen.',
                            'std': 'Histogramm der Standardabweichung des {} Lärmpegels [dB] pro Station'},
        },
        'timeseries_config': {
            'y': 'value',
            'title': '',
            'width': 1000,
            'height': 300,
            'x_title': '',
            'y_digits': 1,
            'color': 'station',
            'marker_size': 30,
            'ts_time_field': {'date': 'hour_date', 'week_date': 'hour_date', 'month_date': 'hour_date', 'year_date': 'date'},
            'ts_time_format': {'date': '%H:%M', 'week_date': '%d.%m.%Y', 'month_date': '%d.%m.%y', 'year_date': '%d.%m.%y'},
            'fig_text': {'avg': 'Zeitreihe der Durchschnitts-Lärmpegels [dB] für {} Stationen.',
                            'min': 'Zeitreihe des minimalen Lärmpegels [dB] für {} Stationen.',
                            'max': 'Zeitreihe des maximalen Lärmpegels [dB] für {} Stationen.',
                            'std': 'Zeitreihe der Standardabweichung des {} Lärmpegels [dB] pro Station'},
        },
        'intro': """**Lärm [dB]**</br>Im Rahmen des Projektes «Smart Climate» von Smart Regio Basel (https://smartregiobasel.ch/pilote/smart-climate-plug--sense) werden an {} Standorten in der Region Basel Schallpegeldaten mit LoRa-Sensoren gemessen. Das Lufthygieneamt beider Basel, das Amt für Umwelt und Energie des Kantons Basel-Stadt, der Basler Wetterdienstleister meteoblue AG, die IWB sowie die Sensirion AG schlossen sich zusammen, um in diesem Pilotprojekt den Einsatz von kosteneffizienten Sensoren zur Erfassung des «regionalen Mikroklimas» zu testen. Hier werden die unvalidierten Schallpegeldaten (Leq) zur Verfügung gestellt.<br>Quelle: [opendata.bs](https://data.bs.ch/explore/dataset/100087/information/)"""
    },

    'particles_pm25': {
        'key': 'pm 2.5',
        'fields': {'pm25': 'PM 2.5'},
        'label': 'Feinstab PM2.5 [ug/m³]',
        'station_db_table': "T_100081_station",
        'db_table': "T_100081",
        'agg_functions': ['avg','min','max'],
        'map_config': {
            'station_agg_function': 'avg',
            'lat': 'lat',
            'long': 'long',
            'station_col': 'station_id',
            'value_col': 'value',
            'min_val': 0,
            'max_val': 10,
            'station_id': 'station_id',
            'size': 50,
            'width': 600,
            'height': 600,
            'fig_text': {'avg': 'Mittlere {} Feinstaub- [μg/m³] pro Station',
                            'min': 'Minimale {} Feinstaub- [μg/m³] pro Station',
                            'max': 'Maximale {} Feinstaub- [μg/m³] pro Station',
                            'std': 'Standardabweichung der {} Feinstaub- [μg/m³] pro Station',
                            'sum': 'Summe {} Feinstaub- [μg/m³] pro Station'}
        },
        'histogram_config': {
            'x': 'value',
            'x_title': '',
            'y_title': 'Anzahl',
            'bins': 20,
            'x_domain': [0.100],
            'width': 600,
            'height': 400,
            'fig_text': {'avg': 'Histogramm des Durchschnitts von Feinstaub [μg/m³] für {} Stationen.',
                            'min': 'Histogramm des minimalen Feinstaub [μg/m³] für {} Stationen.',
                            'max': 'Histogramm des maximalen Feinstaub [μg/m³] für {} Stationen.'}
        },
        'timeseries_config': {
            'y': 'value',
            'title': '',
            'width': 1000,
            'height': 300,
            'x_title': '',
            'y_digits': 1,
            'color': 'station',
            'marker_size': 30,
            'ts_time_field': {'date': 'hour_date', 'week_date': 'hour_date', 'month_date': 'hour_date', 'year_date': 'date'},
            'ts_time_format': {'date': '%H:%M', 'week_date': '%d.%m.%Y', 'month_date': '%d.%m.%y', 'year_date': '%d.%m.%y'},
            'fig_text': {'avg': 'Zeitreihe der Durchschnitts von Feinstaub [μg/m³] für {} Stationen.',
                            'min': 'Zeitreihe des minimalen Feinstaubs [μg/m³] für {} Stationen.',
                            'max': 'Zeitreihe des maximalen Feinstaubs [μg/m³] für {} Stationen.'}
        },
        'intro': """**Feinstaub PM 2.5 [μg/m³]**</br>Im Rahmen des Projektes «Smart Climate» von [Smart Regio Basel](https://smartregiobasel.ch/de/projekte/smart-climate-plug-and-sense) wurden in der ersten Projektphase an zehn Standorten in der Region Basel Luftdaten mit Mikrosensoren gemessen. Das Lufthygieneamt beider Basel, das Amt für Umwelt und Energie des Kantons Basel-Stadt, der Basler Wetterdienstleister meteoblue AG, die IWB sowie die Sensirion AG schlossen sich zusammen, um in diesem Pilotprojekt den Einsatz von kosteneffizienten Sensoren zur Erfassung des «regionalen Mikroklimas» zu testen. Hier werden die unvalidierten Daten von Feinstaub PM2.5 zur Verfügung gestellt. Die erste Projektphase wurde Ende 2021 ausgewertet und basierend auf den Ergebnissen das Messnetz verkleinert. Ab Frühling 2022 werden die Messstationen «Erlenparkweg 55», «Feldbergstrasse», «NABEL Binningen», «St. Johanns-Platz» und «Zürcherstrasse 148 (Breite) weiter betrieben.
        <br>Quelle: [opendata.bs](https://data.bs.ch/explore/dataset/100081/information/)"""
    },
}