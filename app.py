import streamlit as st
import os

from about import About
import helper
import explorer


__version__ = '0.0.2'
__author__ = 'Lukas Calmbach'
__author_email__ = 'lcalmbach@gmail.com'
VERSION_DATE = '2022-09-9'
GIT_REPO = 'https://github.com/lcalmbach/smart-bs'
APP_NAME = 'sensors-bs'
APP_ICON = "📐"

MENU_OPTIONS = ['About', 'Explorer']
MENU_ANALYSIS = ['Temperature Trend', 'Nitrate in Groundwater']
LOTTIE_URL = "https://assets1.lottiefiles.com/packages/lf20_1IBhTm.json"

APP_INFO = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>App created by <a href="mailto:{__author_email__}">{__author__}</a><br>
    version: {__version__} ({VERSION_DATE})<br>
    <a href="{GIT_REPO}">git-repo</a>
    """

def main():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=APP_ICON,
        layout="wide")
    st.sidebar.markdown(f"## <center>{APP_NAME}</center>", unsafe_allow_html=True) 
    helper.show_lottie(LOTTIE_URL)
    
    st.session_state.args = st.experimental_get_query_params()
    if not('calls' in st.session_state):
        st.session_state.calls = 0
    
    menu_item = st.sidebar.selectbox('Menu', options=MENU_OPTIONS)
    if st.session_state.args != {} and st.session_state.calls == 0:
        pass
    else:
        if menu_item==MENU_OPTIONS[0]:
            app = About()
        if menu_item==MENU_OPTIONS[1]:
            app = explorer.App()

    st.session_state.calls += 1
    app.show_menu()
    st.sidebar.markdown(APP_INFO, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    