import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, User, Admin
import time
import pandas as pd
import pickle
import base64

st.set_page_config(page_title="Aerosite for User", page_icon=":material/flight:", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    body * {  
        font-family: 'Poppins', sans-serif;
    }
    .navbar {
        background-color: #0077b6;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .navbar .logo img {
        height: 50px;
    }
    .navbar .title-section {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .navbar .title {
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin: 0;
    }
    .navbar .profile {
        display: flex;
        align-items: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .navbar .profile .icon {
        font-family: 'Material Symbols Outlined';
        font-size: 30px;
        margin-right: 10px;
    }
    .navbar .filter-dropdown {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 5px;
        padding: 5px 10px;
        font-size: 14px;
        color: #0077b6;
    }
    section[data-testid="stSidebar"] {
        background-color: #0077b6;
    }
    div.stButton > button {
        background-color: red; 
        color: white;
    }
    div.stButton > button:active {
        background-color: red; 
        color: white;
    }     
    </style>
    """, unsafe_allow_html=True)

def encodedImage(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
logo_aero = encodedImage("./static/images/logowarna.png")  

def show_error(message):
    time.sleep(2)
    st.error(message)

try:
    with app.app_context():
        params = st.query_params
        session_token = params.get('sessionToken', [None])
        
        if not session_token:
            show_error("Tidak ada sesi yang ditemukan. Akses tidak diizinkan.")
        else:
            user = User.query.filter_by(token=session_token).first()  
            if user:
                st.markdown(f"""
                <div class="navbar">
                    <div class="logo">
                        <img src="data:image/png;base64,{logo_aero}" alt="Logo">
                    </div>
                    <div class="profile">
                        <span class="icon">account_circle</span>
                        Welcome, {user.name}!
                    </div>
                </div>
                """, unsafe_allow_html=True)  
                open_model = open("model/model_satisfaction.sav", "rb")
                model = pickle.load(open_model)
                if user.survey:
                    st.session_state.step = 1
                else:
                    st.session_state.step = 0

                selected = option_menu(menu_title=None, options=["Survei Penerbangan", "Pengaturan"],
                                    icons=['airplane-engines', 'gear'],
                                    menu_icon="list", default_index=0, orientation="horizontal")

                if selected == "Survei Penerbangan":
                    if st.session_state.step == 0:
                        with st.form("flight_form", border=False):
                            st.title("Isi Data Penerbangan")
                            with st.container(border=True):
                                st.write("Masukkan Data Penerbangan")
                                col1, col2, col3, col4 = st.columns(4)
                                
                                with col1:
                                    gender = st.selectbox("Gender", options=["Male", "Female"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    flight_distance = st.number_input("Flight Distance", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col2:
                                    age = st.number_input("Age", min_value=0, max_value=120, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    departure_delay = st.number_input("Departure Delay in Minutes", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col3:
                                    travel_type = st.selectbox("Type of Travel", options=["Business travel", "Personal Travel"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                    arrival_delay = st.number_input("Arrival Delay in Minutes", min_value=0, value=0, help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)
                                
                                with col4:
                                    flight_class = st.selectbox("Class", options=["Eco", "Eco Plus", "Business"], help='*required')
                                    st.markdown('<br>', unsafe_allow_html=True)

                            st.title("Isi Survei")
                            with st.container():
                                st.markdown(
                                    """
                                    <div style="background-color: #F7F4A6; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                                        <p style="font-size: 15px; margin-bottom: 0px;"><b>Catatan:</b></p>
                                        <p style="font-size: 15px; margin-top: 0px; margin-bottom: 0;"><b><u>0 untuk sangat tidak puas; 5 untuk sangat puas</u></b></p>
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                            with st.container(border=True):
                                questions = {
                                    "Seat Comfort": "Seat Comfort",
                                    "Food and Drink": "Food and Drink",
                                    "Departure/Arrival Time Convenience": "Departure/Arrival Time Convenience",
                                    "Gate Location": "Gate Location",
                                    "Inflight Wifi Service": "Inflight Wifi Service",
                                    "Inflight Entertainment": "Inflight Entertainment",
                                    "Online Support": "Online Support",
                                    "Ease of Online Booking": "Ease of Online Booking",
                                    "On-board Service": "On-board Service",
                                    "Leg Room Service": "Leg Room Service",
                                    "Baggage Handling": "Baggage Handling",
                                    "Check-in Service": "Check-in Service",
                                    "Cleanliness": "Cleanliness",
                                    "Online Boarding": "Online Boarding"
                                }

                                survey_responses = {}

                                question_keys = list(questions.keys())
                                for i in range(0, len(question_keys), 3):
                                    cols = st.columns(3)

                                    for j, col in enumerate(cols):
                                        if i + j < len(question_keys):
                                            question = question_keys[i + j]
                                            with col:
                                                st.write(questions[question])
                                                survey_responses[question] = st.radio("Skala 0-5", options=[0, 1, 2, 3, 4, 5], key=question, horizontal=True, help='*required')

                                    st.markdown("---")

                            submit_button = st.form_submit_button("Submit")

                            if submit_button:
                                with st.status("Mengirim survei...", expanded=True) as status:
                                    st.write("Survei dikirim...")
                                    data_new_record = pd.DataFrame({
                                        'Gender': [1 if gender == "Male" else 0], 
                                        'Age': [age],
                                        'Type of Travel': [1 if travel_type == "Business travel" else 0],
                                        'Class': [2 if flight_class == "Business" else (1 if flight_class == "Eco Plus" else 0)],
                                        'Flight Distance': [flight_distance],
                                        'Seat comfort': [survey_responses["Seat Comfort"]],
                                        'Departure/Arrival time convenient': [survey_responses["Departure/Arrival Time Convenience"]],
                                        'Food and drink': [survey_responses["Food and Drink"]],
                                        'Gate location': [survey_responses["Gate Location"]],
                                        'Inflight wifi service': [survey_responses["Inflight Wifi Service"]],
                                        'Inflight entertainment': [survey_responses["Inflight Entertainment"]],
                                        'Online support': [survey_responses["Online Support"]],
                                        'Ease of Online booking': [survey_responses["Ease of Online Booking"]],
                                        'On-board service': [survey_responses["On-board Service"]],
                                        'Leg room service': [survey_responses["Leg Room Service"]],
                                        'Baggage handling': [survey_responses["Baggage Handling"]],
                                        'Checkin service': [survey_responses["Check-in Service"]],
                                        'Cleanliness': [survey_responses["Cleanliness"]],
                                        'Online boarding': [survey_responses["Online Boarding"]],
                                        'Departure Delay in Minutes': [departure_delay],
                                        'Arrival Delay in Minutes': [arrival_delay]
                                    })
                                    time.sleep(1.5)
                                    st.write("Survei diprediksi...")
                                    satisfaction_prediction = model.predict(data_new_record)
                                    prediction_text = "satisfied" if satisfaction_prediction[0] == 1 else "dissatisfied"
                                    time.sleep(1.5)
                                    
                                    st.write("Hasil Survei ditambahkan...")
                                    data_new_record['satisfaction'] = prediction_text
                                    data_new_record['Customer Type'] = None
                                    data_new_record['Gender'] = data_new_record['Gender'].replace({1: 'Male', 0: 'Female'})
                                    data_new_record['Type of Travel'] = data_new_record['Type of Travel'].replace({1: 'Business travel', 0: 'Personal Travel'}) 
                                    data_new_record['Class'] = data_new_record['Class'].replace({2: "Business", 1: 'Eco Plus', 0: 'Eco'})
                                    
                                    df = pd.read_csv("./dataset/Invistico_Airline.csv")
                                    df_concated = pd.concat([df, data_new_record], ignore_index=True) 
                                    df_concated.to_csv("./dataset/Invistico_Airline.csv", index=False)

                                    user.survey = True
                                    admin = Admin.query.first()
                                    admin.survey_count += 1
                                    if satisfaction_prediction[0] == 1:
                                        admin.satisfied_count += 1
                                        user.result = True
                                    else:
                                        admin.dissatisfied_count += 1
                                        user.result = False
                                    db.session.commit()
                                    time.sleep(1.5)
                                    status.update(
                                        label="Berhasil!", state="complete", expanded=False
                                    )
                                    time.sleep(2)
                                st.rerun()

                    elif st.session_state.step == 1:
                        st.title("Thanks for your feedback!")
                        st.markdown("<h1 style='text-align: left; color: #4CAF50;'>🎉 Terima Kasih!</h1>", unsafe_allow_html=True)
                        st.markdown("<p style='text-align: left; font-size: 20px;'>Kami menghargai umpan balik Anda.</p>", unsafe_allow_html=True)

                        st.markdown("<p style='text-align: left; font-size: 24px; color: #FFA500;'>✨ Survey Anda telah terkirim dengan sukses!</p>", unsafe_allow_html=True)
                        st.markdown('<br>', unsafe_allow_html=True)

                        st.markdown("<h5>Hasil Survei</h5>", unsafe_allow_html=True)
                        if user.result == True:
                            st.markdown(
                                """
                                <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
                                    <span style="color:#17BE49;font-size:40px;font-weight:700;">Satisfied</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                """
                                <div style="background-color:#f8d7da;padding:10px;border-radius:5px;">
                                    <span style="color:#721c24;font-size:40px;font-weight:700;">Dissatisfied</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        st.markdown('<br>', unsafe_allow_html=True)

                        st.markdown("<h5>Ringkasan Hasil Survei</h5>", unsafe_allow_html=True)
                        if user.result == True:
                            st.markdown(
                                """
                                <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
                                    <span style="color:#17BE49;font-size:20px;font-weight:700;">Kami sangat senang mengetahui bahwa Anda puas dengan pengalaman penerbangan Anda. Terima kasih atas apresiasi yang Anda berikan. Kami akan terus berusaha memberikan pelayanan terbaik untuk setiap pelanggan kami!</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                """
                                <div style="background-color:#f8d7da;padding:10px;border-radius:5px;">
                                    <span style="color:#721c24;font-size:20px;font-weight:700;">Kami mohon maaf atas ketidaknyamanan yang Anda alami selama penerbangan. Masukan Anda sangat berarti bagi kami, dan kami berkomitmen untuk memperbaiki layanan agar pengalaman Anda di masa depan lebih memuaskan. Terima kasih telah berbagi pengalaman Anda.</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                elif selected == "Pengaturan":
                    st.title("Pengaturan")
                    if st.button("Log Out", key='logout_button', icon=':material/logout:'):
                        if "session_token" in st.session_state:
                            del st.session_state["session_token"]
                        user.token = None
                        db.session.commit()
                        st.toast("Log Out Berhasil!")
                        time.sleep(1.5)
                        st.write(st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:5000/logout'>", unsafe_allow_html=True))
                        
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")
                
except Exception as e:
    show_error(f"ERROR! Hubungi Admin jika menurut anda ini adalah kesalahan.")

