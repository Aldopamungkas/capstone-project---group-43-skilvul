import streamlit as st
from streamlit_option_menu import option_menu
from captcha.image import ImageCaptcha
import random
import string
import dashboard, prediction, profile

# Constants for CAPTCHA
length_captcha = 6
width = 200
height = 150

# Function for CAPTCHA control
def captcha_control():
    if 'control' not in st.session_state or st.session_state['control'] == False:
        st.title("Authorization Aplikasi Biztrack")
        
        st.session_state['control'] = False
        col1, col2 = st.columns(2)
        
        if 'Captcha' not in st.session_state:
            st.session_state['Captcha'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length_captcha))
        
        # Generate CAPTCHA image
        image = ImageCaptcha(width=width, height=height)
        data = image.generate(st.session_state['Captcha'])
        col1.image(data)
        captcha_text = col2.text_area('Enter CAPTCHA text', height=30)
        
        if st.button("Verify the code"):
            captcha_text = captcha_text.replace(" ", "")
            if st.session_state['Captcha'].lower() == captcha_text.lower().strip():
                del st.session_state['Captcha']
                col1.empty()
                col2.empty()
                st.session_state['control'] = True
                st.experimental_rerun() 
            else:
                st.error("🚨 The CAPTCHA code is incorrect, please try again.")
                del st.session_state['Captcha']
                del st.session_state['control']
                st.experimental_rerun()
        else:
            st.stop()

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            st.image('BizTrack_logoo.png', width=200)

            app = option_menu(
                menu_title='Dashboard Biztrack',
                options=['Dashboard', 'Prediction', 'Profile'],
                icons=['house', 'graph-up', 'person'],
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {
                        "padding": "5!important",
                        "background-color": "#1f1f2e",
                    },
                    "menu-title": {
                        "font-size": "20px",
                        "color": "white",
                        "text-align": "left",
                    },
                    "icon": {
                        "color": "white",
                        "font-size": "25px",
                    },
                    "nav-link": {
                        "color": "white",
                        "font-size": "20px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#565679",
                    },
                    "nav-link-selected": {
                        "background-color": "#04AA6D",
                        "color": "white",
                    },
                }
            )

        if app == "Dashboard":
            dashboard.app()
        elif app == "Prediction":
            prediction.app()
        elif app == "Profile":
            profile.app()

# Set up Streamlit configuration
st.set_page_config(
    page_title="Dashboard Biztrack",
)

# Check CAPTCHA control
if 'control' not in st.session_state or st.session_state['control'] == False:
    captcha_control()
else:
    app = MultiApp()
    app.run()
