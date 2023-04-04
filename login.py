import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import pagesnew as pg
import yaml
from yaml.loader import SafeLoader

st.set_page_config(layout="wide",
                   page_title="Employability Predictor",
                   page_icon="🧊")

st.markdown("""
<style>
.app-header {
    font-size:50px;
    color: #F63366;
    font-weight: 700;
}
.sidebar-header{
    font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
    font-size: 28px;
    letter-spacing: -1.2px;
    word-spacing: 2px;
    color: #FFFFFF;
    font-weight: 700;
    text-decoration: none;
    font-style: normal;
    font-variant: normal;
    text-transform: capitalize;
}
.positive {
    color: #000000;
    font-size:30px;
    font-weight: 700;  
}
.negative {
    color: #70F140;
    font-size:30px;
    font-weight: 700;  
}

.ag-theme-streamlit-dark {
    --ag-background-color: #1d1d41 !important;
    --ag-odd-row-background-color: #29284d;
    --ag-foreground-color: #fff;
    --ag-alpine-active-color: #ff4b4b;
    --ag-grid-size: 4px;
    --ag-header-background-color: #121031;
    --ag-borders: solid 0.5px;
    --ag-border-color: #33336c;
    --ag-cell-horizontal-border: solid #33336c;
    --ag-header-foreground-color: #ffffff;
    --ag-font-family: "Source Sans Pro";
    --ag-font-size: 9.5pt;
    --ag-subheader-background-color: #000;
    }
</style>
""", unsafe_allow_html=True)

def login():

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login(
        'Login', 'main', logo="Prediction-removebg.png", logo_width=200)

    if authentication_status:
        authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{name}*')
        # st.title('Some Cool content')

        with st.sidebar:
            st.image("Prediction-removebg.png",width=300,output_format='PNG')
            
            selected = option_menu(
                menu_title = "",
                icons = ["grid-fill","calendar","graph-up-arrow","book",'gear'],
                menu_icon = 'fire',
                options = ["Dashboard","Predict",'Result',"About"],
                default_index = 0
            )

        if selected == "Dashboard":
            pg.dashboard()
        if selected == "Predict":
            pg.predict()
        if selected == "Result":
            pg.result()
        # if selected =="Setting":
        #     pg.setting()
        if selected == "About":
            pg.about()

    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')


def main():
    login()

if __name__ == "__main__":
    main()