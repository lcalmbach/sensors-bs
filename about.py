import streamlit as st
from datetime import datetime

import about_texts
import helper
from explorer import SENSORS_DICT
from queries import qry
import database as db


class About():
    def __init__(self):
        #self.wq_data = data.get_water_quality_data()
        #self.stations_list = list(self.wq_data['station_id'].unique())
        #self.well_records = data.get_well_records([])
        pass
    
    def show_menu(self):
        """


        """
        st.image('./img/splash.jpg', caption=None, width=None, use_column_width='auto', clamp=False, channels='RGB', output_format='auto')
        figure = '[image source](https://www.bs.ch/bilddatenbank)'
        st.markdown(helper.font_size_small(figure), unsafe_allow_html=True)
        cols = st.columns([1, 6, 1])
        with cols[1]:
            st.markdown(about_texts.intro.format(28, 84))
            st.markdown('#### Sensoren')
            for key in SENSORS_DICT:
                sql = qry['no_stations_query'].format(SENSORS_DICT[key]['station_db_table'])
                stations, ok, err_msg = db.get_value(sql)
                text = SENSORS_DICT[key]['intro'].format(stations)
                st.markdown(text, unsafe_allow_html=True)
