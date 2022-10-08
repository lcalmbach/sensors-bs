import streamlit as st

import about_texts
import helper
from explorer import SENSORS_DICT
from queries import qry
import database as db


class About():
    def __init__(self):
        pass
    
    def show_menu(self):
        """
        Shows a short intro text (from about_texts.py) then a list of all sensors (json from sensoren.py). for noise, a 
        formula for average value calculation is shown: Streamlit does not support latex in fstrings, therefore noise has to 
        be handled seperature. the formula shows how the average value is calculated
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
                if SENSORS_DICT[key]['key']=='noise':
                    st.latex(r"""L_m = 10 · log(\frac{1}{N} · \sum_{i=1}^{N} 10^{0.1·L_i}""")
