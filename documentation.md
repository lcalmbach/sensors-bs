# smart-bs documentation

## data, sensosrs
data is extracted from data.bs using project opendatastore:   
Done:
- [Smart Climate Luftklima](https://data.bs.ch/explore/dataset/100009/) 
- [Smart Climate Schallpegelmessungen](https://data.bs.ch/explore/dataset/100087)   

todo:
- [Smarte Strasse: Fahrzeugdurchfahrten](https://data.bs.ch/explore/dataset/100172)

during extraction, data is normalized to include the following columns
- station_id: str
- timestamp: datetime
- date: datetime
- value: float: this field can be renamed, for example for climate data includes temperature and precipitation.

Stations are extracted seperately as distinct values from the data and include the fields:
- name: gernerally the address of the location 
- station_id: unique identifier
- lat: decimal latitude
- long: decimal longitude

### sensor object
```
'Lufttemperatur °C':{
        'data-source': 'smart-climate',
        'data-source-station': 'smart-climate-station',
        'field':'air_temp','Jahr':'week'},
        'label':'Lufttemperatur °C',
        'group_fields': ['station_id','name', 'lat', 'long', 'date'],
        'time_agg': ['Stunde', 'Tag', 'Woche', 'Monat', 'Jahr'],
        'map_agg': ['Mittelwert', 'Minimum','Maximum', 'Standard Abweichung']
    },
```

### smart elefant system variables
#### sql elefant
DATABASE vrxlzjbq
DB_HOST lucky.db.elephantsql.com
DB_PASS j85OQOVHnc-utChz9drzSRFydOWbdMrm
DB_USER vrxlzjbq

Heroku
DB_HOST ec2-99-80-170-190.eu-west-1.compute.amazonaws.com