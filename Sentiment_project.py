import streamlit as st
import joblib
import re
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(layout="wide")

def  mycleaning(doc):
        return re.sub("[^a-zA-Z ]","",doc).lower()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    if st.sidebar.button("Logout",key="b4"):
            st.session_state.logged_in = False
            st.rerun()

    # ✅ Default value set (first time only)
    if "theme" not in st.session_state:
        st.session_state.theme = True   # 👈 True = Dark Mode default

    # Toggle (linked with session state)
    theme = st.toggle("🌙 Dark Mode", value=st.session_state.theme)

    # Update state
    st.session_state.theme = theme

    # Apply theme
    if theme:
        # 🌙 DARK MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        # ☀️ LIGHT MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)
        

    st.sidebar.image("restaurant_2.jpg")

    st.sidebar.markdown("## 👋 Welcome")
    st.sidebar.write("Login to explore AI-powered food sentiment insights 🍽️")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 🤖 About App")
    st.sidebar.write("This app analyzes restaurant reviews using Machine Learning & NLP.")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 🚀 Features")
    st.sidebar.write("✔ Sentiment Analysis")
    st.sidebar.write("✔ Bulk Review Prediction")
    st.sidebar.write("✔ AI-powered insights")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 🍴 Restaurants")
    st.sidebar.write("• The Royal Saffron")
    st.sidebar.write("• Velvet Table")
    st.sidebar.write("• Aurora Fine Dining")
    st.sidebar.write("• Crystal Flame")
    st.sidebar.write("• Explore more restaurants by clicking the 'Get Credentials' button.")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 📱 How to Login?")
    st.sidebar.write("1. Click 'Get Credentials'")
    st.sidebar.write("2. Select Restaurant")
    st.sidebar.write("3. Scan QR Code")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 🧑‍💻 Developer")
    st.sidebar.write("Made by: Dev Varshney")
    st.sidebar.write("AI/ML Enthusiast 🚀")
    st.sidebar.write("====================================")

    st.sidebar.markdown("## 📞 9058068999")
    st.sidebar.write("Email: varshneyd110@gmail.com")
    st.sidebar.write("====================================")

    # 🎨 Banner
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        ">
            <h1 style="
                color: white;
                font-size: 35px;
                margin-bottom: 10px;
            ">
                🍽️ Food Sentiment Analyzer
            </h1>
            <p style="
                color: #e0e0e0;
                font-size: 18px;
            ">
                Understand customer emotions using AI 🤖
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 🔐 Login Box
    st.markdown("## 🔐 Login to Continue")

    # 🔐 Login inputs
    st.write("\n")
    st.write("### 👤 Enter Username")
    username = st.text_input("",placeholder="please type User Name ......")
    st.write("### 🔑 Enter Password")
    password = st.text_input("", type="password",placeholder="please type Password ......")

    # 🍽️ Restaurant dictionary
    restaurants = {
        "Crimson Crown Dining": "CC@Royal",
        "The Velvet Ember": "VE#Luxury",
        "Golden Orchid Palace": "GO@Elite",
        "Sapphire Feast House": "SF#Fine",
        "The Imperial Platter": "IP@King",
        "Royal Spice Symphony": "RS#Chef",
        "The Grand Saffron Table": "GS@Royal",
        "Opulent Flame Bistro": "OF#Fire",
        "Silver Crest Kitchen": "SC@Elite",
        "Emerald Royal Dine": "ER#Green",
        "The Regal Spoon": "RS@Queen",
        "Aurora Palace Kitchen": "AP#Sky",
        "The Luxe Ember Table": "LE@VIP",
        "Majestic Fork Lounge": "MF#Elite",
        "The Noble Feast House": "NF@Royal",
        "Golden Crown Bistro": "GC#King",
        "The Velvet Royale": "VR@Luxury",
        "Crystal Palace Dining": "CP#Fine",
        "Imperial Orchid Table": "IO@King",
        "The Grand Velvet Bite": "GV#Luxury",
        "Saffron Majesty Kitchen": "SM@Royal",
        "Royal Ember Court": "RE#Fire",
        "The Opal Crown Dine": "OC@Elite",
        "Silver Royal Symphony": "SR#Class",
        "The Regal Orchid": "RO@Queen",
        "Aurora Luxe Dining": "AL#Sky",
        "The Golden Majesty": "GM@Royal",
        "Emerald Crown Feast": "EC#Green",
        "Imperial Velvet Kitchen": "IV@King",
        "The Crystal Royal Bite": "CR#Fine",
        "Noble Saffron Table": "NS@Royal",
        "The Luxe Crown House": "LC#VIP",
        "Grand Imperial Feast": "GI@King",
        "Royal Opulent Spoon": "RO#Elite",
        "The Velvet Spice Court": "VS@Luxury",
        "Golden Ember Palace": "GE#Fire",
        "The Regal Sapphire": "RS@Queen",
        "Silver Luxe Bistro": "SL#Class",
        "The Royal Orchid Table": "RO@Royal",
        "Imperial Flame Feast": "IF#Fire",
        "The Grand Emerald Bite": "GE#Green",
        "Aurora Crown Kitchen": "AC#Sky",
        "The Velvet Majesty": "VM@Luxury",
        "Crystal Luxe Dining": "CL#Fine",
        "The Noble Orchid Feast": "NO@Royal",
        "Golden Regal Table": "GR#King",
        "The Opulent Sapphire": "OS@Elite",
        "Royal Grand Bistro": "RG#Royal",
        "The Luxe Imperial Spoon": "LI@VIP",
        "Emerald Velvet Feast": "EV#Green",
        "The Crown Symphony Kitchen": "CS@Royal",
        "Silver Imperial Table": "SI#Class",
        "The Grand Orchid Palace": "GO@Royal",
        "Majestic Crystal Feast": "MC#Fine",
        "The Regal Flame Dining": "RF@Fire"
    }


    # 🔘 Buttons side by side
    col1, col2 = st.columns(2)

    # 1️⃣ Login Button
    with col1:
        if st.button("Login"):
            if username in restaurants and password == restaurants[username]:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success(f"Welcome {username} 🎉")
                st.rerun()
            else:
                st.error("Wrong Username/Password ❌")

    # 2️⃣ Get Credentials Button
    with col2:
        if st.button("📱 Get Credentials"):
            st.session_state.show_dropdown = True

    # 🔽 STEP 2 → Dropdown open
    if st.session_state.get("show_dropdown", False):

        selected = st.selectbox("🍴 Select Restaurant", list(restaurants.keys()))

    
        import qrcode
        from io import BytesIO

        if st.button("Generate QR"):

            data = f"Username: {selected}\nPassword: {restaurants[selected]}"

            qr = qrcode.make(data)

            # 👉 Convert to bytes (IMPORTANT FIX)
            buf = BytesIO()
            qr.save(buf, format="PNG")
            buf.seek(0)

            st.image(buf, caption="📱 Scan to get credentials", width=200)

            st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(90deg, #28a745, #5cd65c);
            color: white;
            border-radius: 30px;
            padding: 16px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #218838, #4cd137);
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)
            
    st.markdown("""
    <style>
    @keyframes fadeText {
        0% {opacity: 0;}
        10% {opacity: 1;}
        25% {opacity: 1;}
        35% {opacity: 0;}
        100% {opacity: 0;}
    }

    .text-container {
        position: relative;
        height: 40px;
        text-align: left;
        color: #00c6ff;
        font-size: 22px;
        font-weight: bold;
                
        margin-top: 40px;
    }

    .text-container span {
        position: absolute;
        width: 100%;
        opacity: 0;
        animation: fadeText 8s infinite;
    }

    .text-container span:nth-child(1) { animation-delay: 0s; }
    .text-container span:nth-child(2) { animation-delay: 2s; }
    .text-container span:nth-child(3) { animation-delay: 4s; }
    .text-container span:nth-child(4) { animation-delay: 6s; }
    </style>

    <div class="text-container">
        <span>🔍 Analyze Reviews in Seconds</span>
        <span>🤖 Understand Customer Emotions</span>
        <span>📊 Get AI-Powered Insights</span>
        <span>🚀 Grow Your Restaurant Smartly</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>📊 Reviews Analyzed</h4>
            <h2>25K+</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #141e30, #243b55);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>🎯 Accuracy</h4>
            <h2>92%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #42275a, #734b6d);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>🍴 Restaurants</h4>
            <h2>50+</h2>
        </div>
        """, unsafe_allow_html=True)
            
    

def main_app():

    st.sidebar.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)


    # ✅ Logout sabse upar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    theme = st.toggle("🌙 Dark Mode")

    if theme:
        # 🌙 DARK MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    else:
        # ☀️ LIGHT MODE
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: black;
        }
        </style>
        """, unsafe_allow_html=True)

        
    st.write("Welcome to Food Sentiment Analysis 🍽️")

    # 👉 Yaha se tumhara pura code paste karo

    

    model=joblib.load("sentiment_model.pkl")

    
    st.markdown("""
        <div style="
            background: linear-gradient(90deg, #ffff00, #2E7D32);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        ">
            <h1 style="
                color: purple;
                font-size: 40px;
                margin: 0;
            ">
                Food Sentiment Analysis
            </h1>
        </div>
    """, unsafe_allow_html=True)


    st.sidebar.markdown("""
    <h2 style='
        text-align: center;
        background: linear-gradient(90deg, #28a745, #5cd65c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 28px;
        font-weight: bold;'>
        🌿 Control Panel
    </h2>
    """, unsafe_allow_html=True)


    st.sidebar.image("restaurant.jpg")

    st.sidebar.title("About Project 🤖")
    st.sidebar.write("AI-powered sentiment analysis for restaurant reviews")
    st.sidebar.write("Decode customer emotions from restaurant reviews using AI.")
    st.sidebar.write("====================================")

    st.sidebar.title("Libraries 🐍")
    st.sidebar.write("Scikit Learn")
    st.sidebar.write("Pandas")
    st.sidebar.write("Numpy")
    st.sidebar.write("Joblib")
    st.sidebar.write("Streamlit")
    st.sidebar.write("====================================")

    st.sidebar.title("Cloud ☁️💾")
    st.sidebar.write("Streamlit")
    st.sidebar.write("====================================")

    st.sidebar.title("About Us 👥")
    st.sidebar.write("Enter your review and let AI predict the sentiment")
    st.sidebar.write("====================================")

    st.sidebar.title("Contact Us 📞")
    st.sidebar.write("98765XXXXX")
    st.sidebar.write("====================================")


    st.write("\n")
    st.markdown("""
    <h2 style="
        background: linear-gradient(90deg, #28a745, #5cd65c);
        -webkit-background-clip: text;
        letter-spacing: 1px;
        font-weight: bold;
        -webkit-text-fill-color: transparent;">
        🌿 Predict Single Review 
    </h2>
    """, unsafe_allow_html=True)
    sample=st.text_input("",placeholder="type something cool ......")
    if st.button("Predict"):
        pred=model.predict([sample])

        prob=model.predict_proba([sample])
        if pred[0] == 0:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, #ff4b5c, #ff6b6b);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    font-size: 20px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                ">
                    👎 <b>Negative Review</b><br><br>
                    Confidence Score: <b>{prob[0][0]:.2f}</b>
                </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, #28a745, #5cd65c);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    color: white;
                    font-size: 20px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                ">
                    👍 <b>Positive Review</b><br><br>
                    Confidence Score: <b>{prob[0][1]:.2f}</b>
                </div>
            """, unsafe_allow_html=True)

            st.balloons()
            st.snow()

    st.markdown("""
    <h2 style="
        background: linear-gradient(90deg, #28a745, #5cd65c);
        -webkit-background-clip: text;
        letter-spacing: 1px;
        font-weight: bold;
        -webkit-text-fill-color: transparent;">
        🌿 Predict Bulk Review
    </h2>
    """, unsafe_allow_html=True)
    file=st.file_uploader("select file",type=["csv","txt"])
    if file:
        df=pd.read_csv(file,names=["Review"])
        placeholder=st.empty()
        placeholder.dataframe(df)
        

    # Custom CSS

    st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(90deg, #28a745, #5cd65c);
            color: white;
            border-radius: 30px;
            padding: 16px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #218838, #4cd137);
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)
    

    # Button
    if st.button("Predict",key="b2"):
        corpus=df.Review
        pred=model.predict(corpus)
        prob=np.max(model.predict_proba(corpus),axis=1)
        df["Sentiment"]=pred
        df["Confidence"]=prob
        df["Sentiment"]=df["Sentiment"].map({0:"👎Negative Review",1:"👍Positive Review"})
        placeholder.dataframe(df)

        # 📊 Summary calculation
        positive_count = (df["Sentiment"] == "👍Positive Review").sum()
        negative_count = (df["Sentiment"] == "👎Negative Review").sum()

        # 🎉 Attractive Result Card
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="👍 Positive Reviews",
                value=positive_count
            )

        with col2:
            st.metric(
                label="👎 Negative Reviews",
                value=negative_count
            )
        
        with col3:
            st.metric(
                label="📊 Total Reviews",
                value=negative_count + positive_count
            )
        st.success("🎉 Bulk Prediction Completed!")
        st.markdown("""
            ### 💬 Insight
            Turning customer feedback into powerful insights!
            """)
        st.markdown("""
        <style>
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 15px;
            border-radius: 12px;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)

        

        data = {
            "Sentiment": ["Positive", "Negative"],
            "Count": [positive_count, negative_count]
        }

        fig = px.pie(
            values=data["Count"],
            names=data["Sentiment"],
            hole=0.4   # donut style (optional)
        )

        fig.update_layout(
            width=350,   # 👈 size control
            height=350
        )

        st.plotly_chart(fig, use_container_width=False)
        st.balloons()
        st.snow()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1f4037, #99f2c8);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>📊 Reviews Analyzed</h4>
            <h2>25K+</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #141e30, #243b55);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>🎯 Accuracy</h4>
            <h2>92%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #42275a, #734b6d);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-top: 40px;
        ">
            <h4>🍴 Restaurants</h4>
            <h2>50+</h2>
        </div>
        """, unsafe_allow_html=True)

    
    

if st.session_state.logged_in == False:
    login_page()
else:
    main_app()

st.markdown("""
        <style>
        div.stButton > button {
            background: linear-gradient(90deg, #28a745, #5cd65c);
            color: white;
            border-radius: 30px;
            padding: 16px 40px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #218838, #4cd137);
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)











    

