import streamlit as st
import pickle
import pandas as pd
import base64

# ------------ Add Background GIF ------------
def add_bg_from_local(gif_file):
    with open(gif_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/gif;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------ Add Neon CSS Styling ------------
def add_neon_css():
    st.markdown("""
        <style>
        /* Title glow */
        h1 {
            color: #00ffe7;
            text-shadow: 0 0 5px #0ff, 0 0 10px #0ff, 0 0 20px #0ff;
        }

        /* Labels */
        label, .stSelectbox label, .stNumberInput label {
            color: #00ffe7 !important;
            font-weight: bold;
            text-shadow: 0 0 3px #0ff;
        }

        /* Input fields */
        .stSelectbox div[data-baseweb="select"], input {
            background-color: rgba(0, 0, 0, 0.6) !important;
            color: #fff !important;
            border: 1px solid #00ffe7 !important;
            border-radius: 5px;
        }

        /* Buttons */
        div.stButton > button {
            background-color: transparent;
            color: #00ffe7;
            border: 2px solid #00ffe7;
            border-radius: 8px;
            padding: 0.5em 1.5em;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 10px #00ffe7;
        }

        div.stButton > button:hover {
            background-color: #00ffe7;
            color: black;
            box-shadow: 0 0 20px #00ffe7;
        }

        /* Success result */
        .stAlert {
            background-color: rgba(0, 0, 0, 0.7) !important;
            border-left: 5px solid #00ffe7;
            color: #00ffe7;
            text-shadow: 0 0 3px #0ff;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------ Initialize UI ------------
add_bg_from_local("car_gif.gif")           # Your animated synthwave car gif
add_neon_css()

# ------------ Load Data and Model ------------
car_data = pd.read_csv("Cleaned_Car_data.csv")
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

# ------------ App UI ------------
st.title("🚗 Used Car Price Predictor")

names = sorted(car_data['name'].unique())
companies = sorted(car_data['company'].unique())
fuel_types = sorted(car_data['fuel_type'].unique())

name = st.selectbox("Car Name", names)
company = st.selectbox("Company", companies)
year = st.number_input("Year of Purchase", min_value=1990, max_value=2025, step=1)
kms_driven = st.number_input("Kilometers Driven", min_value=0, step=500)
fuel_type = st.selectbox("Fuel Type", fuel_types)

if st.button("Predict Price"):
    input_df = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])

    prediction = model.predict(input_df)[0]
    st.success(f"💰 Estimated Car Price: ₹ {round(prediction):,}")
