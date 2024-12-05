import streamlit as st
from streamlit_option_menu import option_menu
from app import app, db, Admin  
import time
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(page_title="Aerosite for Admin", page_icon=":material/flight:", layout="wide")
    
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
    div.stButton > button {
        background-color: red; 
        color: white;
    }
    div.stButton > button:active {
        background-color: red; 
        color: white;
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
        
        if not session_token or session_token is None:
            show_error("Tidak ada sesi yang ditemukan. Akses tidak diizinkan.")
        else:
            admin = Admin.query.filter_by(token=session_token).first()  
            if admin:
                st.markdown(f"""
                <div class="navbar">
                    <div class="logo">
                        <img src="data:image/png;base64,{logo_aero}" alt="Logo">
                    </div>
                    <div class="profile">
                        <span class="icon">support_agent</span>
                        Welcome, Admin!
                    </div>
                </div>
                """, unsafe_allow_html=True)   
                df = pd.read_csv("./dataset/Invistico_Airline.csv")

                comfort_features = [
                    "Seat comfort",
                    "Departure/Arrival time convenient",
                    "Food and drink",
                    "Gate location",
                    "Inflight wifi service",
                    "Inflight entertainment",
                    "Online support",
                    "Ease of Online booking",
                    "On-board service",
                    "Leg room service",
                    "Baggage handling",
                    "Checkin service",
                    "Cleanliness",
                    "Online boarding"
                ]

                satisfication_rating = admin.satisfied_count/admin.survey_count * 100

                dissatisfication_rating = admin.dissatisfied_count/admin.survey_count * 100

                # Navbar horizontal
                selected = option_menu(
                    menu_title=None,
                    options=["Overview", "Analysis", "Setting"],
                    icons=['database', 'graph-up', 'gear'],
                    menu_icon="cast",
                    default_index=0,
                    orientation="horizontal"
                )
                
                # Metrics
                col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1, 0.1, 1, 0.1, 1, 0.1, 1, 0.1, 1])
                
                with col1:
                    st.metric(label="Total Pengguna Isi Survei :material/person_edit:", value=admin.survey_count)
                with col2:
                    st.markdown(
                        """
                        <div style="border-left: 2px solid #000; height: 70px;"></div>
                        """,
                        unsafe_allow_html=True
                    )
                with col3:
                    st.metric(label="Total Satisfied :material/sentiment_satisfied:", value=admin.satisfied_count)
                with col4:
                    st.markdown(
                        """
                        <div style="border-left: 2px solid #000; height: 70px;"></div>
                        """,
                        unsafe_allow_html=True
                    )
                with col5:
                    st.metric(label="Total Dissatisfied :material/sentiment_dissatisfied:", value=admin.dissatisfied_count)
                with col6:
                    st.markdown(
                        """
                        <div style="border-left: 2px solid #000; height: 70px;"></div>
                        """,
                        unsafe_allow_html=True
                    )
                with col7:
                    st.metric(label="Satisfaction Rate :material/stat_3:", value=f"{satisfication_rating:.2f} %")
                with col8:
                    st.markdown(
                        """
                        <div style="border-left: 2px solid #000; height: 70px;"></div>
                        """,
                        unsafe_allow_html=True
                    )
                with col9:
                    st.metric(label="Dissatisfaction Rate :material/stat_minus_3:", value=f"{dissatisfication_rating:.2f} %")
                
                if selected == "Overview":
                    st.title("Overview")
                    st.header("Detailed Data View")

                    with st.expander("**FILTER**", icon=":material/filter_alt:"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            satisfaction_filter = st.selectbox(
                                "Filter Kepuasan Pelanggan:",
                                options=["All", "satisfied", "dissatisfied"],
                                index=0
                            )
                        with col2:
                            gender_filter = st.selectbox(
                                "Filter Jenis Kelamin:",
                                options=["All"] + list(df['Gender'].unique()),
                                index=0
                            )
                        with col3:
                            travel_filter = st.selectbox(
                                "Filter Tipe Perjalanan:",
                                options=["All"] + list(df['Type of Travel'].unique()),
                                index=0
                            )

                        col1, col2, col3, col4, col5 = st.columns([0.1, 1, 0.1, 1, 0.1  ])

                        with col2:
                            age_range = st.slider(
                                "Filter Rentang Usia:",
                                min_value=int(df['Age'].min()),
                                max_value=int(df['Age'].max()),
                                value=(int(df['Age'].min()), int(df['Age'].max())),
                                step=1
                            )

                        with col4:
                            flight_distance_range = st.slider(
                                "Filter Rentang Jarak Penerbangan:",
                                min_value=int(df['Flight Distance'].min()),
                                max_value=int(df['Flight Distance'].max()),
                                value=(int(df['Flight Distance'].min()), int(df['Flight Distance'].max())),
                                step=1
                            )
                        
                        class_filter = st.multiselect(
                                "Filter Kelas Penerbangan:",
                                options=["Eco", "Eco Plus", "Business"],
                                default=["Eco", "Eco Plus", "Business"], 
                                placeholder="Pilih Opsi" 
                            )
                        
                    filtered_df = df.copy()

                    if satisfaction_filter != "All":
                        filtered_df = filtered_df[filtered_df['satisfaction'] == satisfaction_filter]

                    if gender_filter != "All":
                        filtered_df = filtered_df[filtered_df['Gender'] == gender_filter]

                    if travel_filter != "All":
                        filtered_df = filtered_df[filtered_df['Type of Travel'] == travel_filter]

                    if len(class_filter) > 0: 
                        filtered_df = filtered_df[filtered_df['Class'].isin(class_filter)]

                    filtered_df = filtered_df[
                        (filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1]) &
                        (filtered_df['Flight Distance'] >= flight_distance_range[0]) & (filtered_df['Flight Distance'] <= flight_distance_range[1])
                    ]

                    with st.container(border=True):
                        st.dataframe(filtered_df.drop(columns=['Customer Type']))
                    st.info(f"Dataset ini memiliki **{filtered_df.drop(columns=['Customer Type']).shape[1]}** fitur dan **{filtered_df.drop(columns=['Customer Type']).shape[0]}** data.", icon=":material/info:")
                
                    st.subheader("Distribusi Fitur Demografis")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        with st.container(border=True):
                            satisfaction_counts = filtered_df['satisfaction'].value_counts()
                            fig1 = px.pie(satisfaction_counts, 
                                        names=satisfaction_counts.index, 
                                        values=satisfaction_counts.values, 
                                        title="Distribusi Kepuasan Pelanggan",
                                        color=satisfaction_counts.index,  
                                        color_discrete_map={"satisfied": "blue", "dissatisfied": "red"})
                            st.plotly_chart(fig1)
                        
                    with col2:
                        with st.container(border=True):
                            gender_counts = filtered_df['Gender'].value_counts()
                            fig3 = px.bar(gender_counts, 
                                        x=gender_counts.index, 
                                        y=gender_counts.values, 
                                        title="Distribusi Gender",
                                        color=gender_counts.index,
                                        color_discrete_map={"Male": "#1E90FF", "Female": "#FF69B4"},
                                        category_orders={"Gender": ["Male", "Female"]},
                                        labels={"Gender": "Jenis Kelamin", "y": "Jumlah"})
                            st.plotly_chart(fig3)

                    with col3:
                        with st.container(border=True):
                            fig4 = px.histogram(filtered_df, x='Age', nbins=20, title="Distribusi Usia", marginal="box")
                            fig4.update_layout(xaxis_title="Usia", yaxis_title="Jumlah")
                            st.plotly_chart(fig4)

                    col1, col2, col3 = st.columns(3)
                
                    with col1:
                        with st.container(border=True):
                            travel_counts = filtered_df['Type of Travel'].value_counts()
                            fig8 = px.bar(travel_counts, 
                                        x=travel_counts.index, 
                                        y=travel_counts.values, 
                                        title="Distribusi Tipe Perjalanan", 
                                        color=travel_counts.index,
                                        color_discrete_map={"Personal Travel": "#ADD8E6", "Business travel": "#2C3E50"},
                                        category_orders={"Type of Travel": ["Personal Travel", "Business travel"]},
                                        labels={"Type of Travel": "Tipe Perjalanan", "y": "Jumlah"})
                            st.plotly_chart(fig8)

                    with col2:
                        with st.container(border=True):
                            class_counts = filtered_df['Class'].value_counts()
                            fig5 = px.bar(class_counts, 
                                        x=class_counts.index, 
                                        y=class_counts.values, 
                                        title="Distribusi Kelas Penerbangan", 
                                        color=class_counts.index, 
                                        color_discrete_map={"Eco": "#A9A9A9", "Eco Plus": "#006400", "Business": "#1F4E79"},
                                        category_orders={"Class": ["Business", "Eco Plus", "Eco"]},
                                        labels={"Class": "Kelas Penerbangan", "y": "Jumlah"})
                            st.plotly_chart(fig5)

                    with col3:
                        with st.container(border=True):
                            fig10 = px.histogram(filtered_df, x="Flight Distance", nbins=20, title="Distribusi Jarak Penerbangan", marginal="box")
                            fig10.update_layout(xaxis_title="Jarak Penerbangan", yaxis_title="Jumlah")
                            st.plotly_chart(fig10)

                    with st.container(border=True):
                        comfort_ratings = filtered_df[comfort_features].mean()
                        fig6 = px.bar(comfort_ratings, 
                                    x=comfort_ratings.index, 
                                    y=comfort_ratings.values, 
                                    title="Rata-rata Rating Kenyamanan",
                                    color=comfort_ratings.values,
                                    color_continuous_scale="Blues", 
                                    range_color=[0, 4],
                                    labels={"index": "Fitur Kenyamanan", "y": "Rata-rata"})
                        fig6.update_coloraxes(colorbar_title="Rata-rata")
                        st.plotly_chart(fig6)

                    # st.subheader("Informasi Jenis Pelanggan")
                    # customer_type_counts = df['Customer Type'].value_counts()
                    # fig2 = px.bar(customer_type_counts, 
                    #             x=customer_type_counts.index, 
                    #             y=customer_type_counts.values, 
                    #             title="Informasi Jenis Pelanggan", 
                    #             color=customer_type_counts.index,
                    #             color_discrete_map={"Loyal Customer": "#1E90FF", "disloyal Customer": "#D9534F"},
                    #             labels={"Customer Type":"Jenis Pelanggan", "y":"Jumlah"})  
                    # st.plotly_chart(fig2)

                elif selected == "Analysis":
                    st.title("Analysis")

                    with st.container(border=True):
                        correlation_matrix = df[comfort_features].corr()
                        fig9 = px.imshow(correlation_matrix, text_auto=True, title="Korelasi Antar Fitur Numerik", color_continuous_scale="RdBu")
                        fig9.update_layout(
                            autosize=True,
                            width=1500,   
                            height=1200,   
                        )
                        st.plotly_chart(fig9)

                    with st.container(border=True):
                        fig11 = px.scatter(df, 
                                        x="Departure Delay in Minutes", 
                                        y="Arrival Delay in Minutes", 
                                        color="satisfaction", 
                                        title="Pengaruh Keterlambatan pada Kepuasan",
                                        color_discrete_map={"satisfied": "blue", "dissatisfied": "red"})  
                        st.plotly_chart(fig11)

                    st.subheader("Pengaruh Fitur Kenyamanan terhadap Kepuasan")
                    rows = 7
                    cols = 2
                    i = 0
                    for _ in range(rows):  
                        col_group = st.columns(cols) 
                        for col in col_group:
                            if i < len(comfort_features):  
                                feature = comfort_features[i]
                                with col:
                                    fig11 = px.box(
                                        df, 
                                        x="satisfaction", 
                                        y=feature, 
                                        title=f"Pengaruh {feature} terhadap Kepuasan",
                                        color="satisfaction",
                                        color_discrete_map={"satisfied": "#A3C9FF", "dissatisfied": "#F4A6A6"}
                                    )
                                    with st.container(border=True):
                                        st.plotly_chart(fig11, use_container_width=True)
                                i += 1

                elif selected == "Setting":
                    st.title("Setting")
                    if st.button("Log Out", key='logout_button', icon=':material/logout:'):
                        if "session_token" in st.session_state:
                            del st.session_state["session_token"]
                        admin.token = None
                        db.session.commit()
                        st.toast("Log Out Berhasil!")
                        time.sleep(1.5)
                        st.write(st.markdown("<meta http-equiv='refresh' content='0; url=http://localhost:5000/admin_logout'>", unsafe_allow_html=True))
            
            else:   
                show_error("Token tidak valid. Akses tidak diizinkan.")

except Exception as e:
    show_error(f"ERROR! Hubungi Admin jika menurut anda ini adalah kesalahan.")