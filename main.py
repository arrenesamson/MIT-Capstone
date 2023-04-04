import streamlit as st
from streamlit_option_menu import option_menu
import pagesnew as pg



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

############################
#password implementation
def login():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        
        
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            
            # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.image("Prediction-removebg.png",width=300,output_format='PNG')
        name = st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.image("Prediction-removebg.png",width=300,output_format='PNG')
        name = st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if login():
    
    ############################
    #title for the page
    # name = "Arrene"
    # st.write(f"""
    #     # Welcome Back {name}
    #         """)

    with st.sidebar:
        col1,col2 = st.columns([2,4])
        col1.image("Prediction-removebg.png",width=300,output_format='PNG')
        
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
    if selected =="Result":
        pg.result()
  #  if selected =="Setting":
   #     pg.setting()
        
    if selected == "About":
        pg.about()