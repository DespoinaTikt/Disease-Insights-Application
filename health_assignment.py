import os
import streamlit as st
import openai
import json
import pandas as pd


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_disease_info(disease_name):
    """
    Function to query OpenAI and return structured information about a disease.
    """
    medication_format = '''"Name":""
    "Side effects":[
    0:""
    1:""
    ...
    ]
    "Dosage":""'''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Please provide information on the following aspects for {disease_name}: 1. Key Statistics, 2. Recovery Options, 3. Recommended Medications. Format the response in JSON with keys for 'name', 'statistics', 'total_cases' (this always has to be a number), 'recovery_rate' (this always has to be a percentage), 'mortality_rate' (this always has to be a percentage) 'recovery_options', (explain each recovery option in detail), and 'medication', (give some side effect examples and dosages) always use this json format for medication : {medication_format} ."}
        ]
    )
    return response.choices[0].message.content

def display_disease_info(disease_info):
    """
    Function to display the disease information in a structured way using Streamlit.
    """
    try:
        info = json.loads(disease_info)

        recovery_rate = float(info['statistics']["recovery_rate"].strip('%'))
        mortality_rate = float(info['statistics']["mortality_rate"].strip('%'))

        chart_data = pd.DataFrame(
            {
                "Recovery Rate": [recovery_rate],
                "Mortality Rate": [mortality_rate],
            },
            index = ["Rate"]
        )

        st.write(f"## Statistics for {info['name']}")
        #st.write(info['statistics'])
        st.bar_chart(chart_data)
        st.write("## Recovery Options")
        recovery_options = info['recovery_options']
        for option, description in recovery_options.items():
            st.subheader(option)
            st.write(description)
        st.write("## Medication")
        medication = info['medication']
        medication_count = 1
        for option, description in medication.items():

            st.subheader(f"{medication_count}. {option}")
            st.write(description)
            medication_count += 1
    except json.JSONDecodeError:
        st.error("Failed to decode the response into JSON. Please check the format of the OpenAI response.")

st.title("⚕️ Medical Disease Insights")
st.warning("The information provided by this application is generated by AI and may be inaccurate or incomplete. For medical topics, always consult a qualified professional. This tool is for educational purposes only.")
disease_name = st.text_input("Enter the name of the disease:", placeholder="e.g., Stomachache, Hypertension")
st.button("Get Disease Information")
if disease_name:
    with st.spinner("Fetching information..."):
        disease_info = get_disease_info(disease_name)
    display_disease_info(disease_info)

