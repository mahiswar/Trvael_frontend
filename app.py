import streamlit as st
import requests

# Set up the Streamlit app
st.title("Travel Insurance Prediction")
st.write("This app predicts whether an individual is likely to purchase travel insurance based on input features.")

# Input fields
age = st.number_input("Age", min_value=0, max_value=120, step=1, value=30)
annual_income = st.number_input("Annual Income (in USD)", min_value=0.0, step=1000.0, value=50000.0)
family_members = st.number_input("Number of Family Members", min_value=0, max_value=20, step=1, value=3)
chronic_diseases = st.selectbox("Chronic Diseases", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
employment_type = st.selectbox("Employment Type", options=["Salaried", "Self-Employed"])
graduate_status = st.selectbox("Graduate Status", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
frequent_flyer = st.selectbox("Frequent Flyer", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
travel_abroad = st.selectbox("Travel Abroad", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

# API Endpoint URL
api_url = "https://travel-backend-pdet.onrender.com/predict"

# Make a prediction
if st.button("Predict"):
    # Prepare input data
    input_data = {
        "Age": age,
        "AnnualIncome": annual_income,
        "FamilyMembers": family_members,
        "ChronicDiseases": chronic_diseases,
        "EmploymentType": employment_type,
        "GraduateStatus": graduate_status,
        "FrequentFlyer": frequent_flyer,
        "TravelAbroad": travel_abroad,
    }

    # Call the FastAPI endpoint
    try:
        response = requests.post(api_url, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            if prediction["prediction"] == 1:
                st.success("The individual is likely to purchase travel insurance.")
            else:
                st.info("The individual is unlikely to purchase travel insurance.")
        else:
            st.error(f"API Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error("Failed to connect to the API. Please check if the FastAPI server is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")