import streamlit as st
from datetime import datetime
import about_texts
import helper
import explorer as ex


class About():
    def __init__(self):
        #self.wq_data = data.get_water_quality_data()
        #self.stations_list = list(self.wq_data['station_id'].unique())
        #self.well_records = data.get_well_records([])
        pass
    
    def show_menu(self):
        """
        numbers from 
        https://www.aue.bs.ch/wasser/grundwasser/grundwasserpegel-grundwasserqualitaet.html > 84

        """
        st.image('./img/splash.jpg', caption=None, width=None, use_column_width='auto', clamp=False, channels='RGB', output_format='auto')
        figure = '[image source](https://www.bs.ch/bilddatenbank)'
        st.markdown(helper.font_size_small(figure), unsafe_allow_html=True)
        cols = st.columns([1, 6, 1])
        with cols[1]:
            st.markdown(about_texts.intro.format(28, 84))
            st.markdown('#### Sensoren')
            for key in ex.SENSORS_DICT:
                text = ex.SENSORS_DICT[key]['intro'].format(152)
                st.markdown(text, unsafe_allow_html=True)
