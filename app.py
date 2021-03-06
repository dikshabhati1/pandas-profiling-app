import numpy as np
import base64
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Web App Title
st.markdown('''
# **The EDA App**
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache(allow_output_mutation = True,max_entries = 10, ttl = 3600)
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)
    
    
    columns_list = df.columns
    l = []
    for column in columns_list:
        data = df[df[column].isna()]
        l.append(data['ds_instance_id'].value_counts().to_dict())
    
    null_rate_df = pd.DataFrame(columns=['Column','Count','null_rate'])
    null_rate_df['Column'] = [i for i in df.columns]
    null_rate_df['Count'] = [j for j in df.isnull().sum()]
    null_rates = df.isnull().sum()/df.shape[0]*100
    null_rate_df['null_rate'] = [k for k in null_rates]
    null_rate_df['ds_id_null'] = [l[i] for i in range(len(null_rate_df))]
    
    fill_rate_df = pd.DataFrame(columns=['Column','Count','fill_rate'])
    fill_rate_df['Column'] = [i for i in df.columns]
    fill_rate_df['Count'] = [j for j in df.notnull().sum()]
    fill_rates = 100 - df.isnull().sum()/df.shape[0]*100
    fill_rate_df['fill_rate'] = [k for k in fill_rates]
    
    
    def filedownload_null(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="null_rate.csv">Download Null Rate CSV File</a>'
        return href
    
    def filedownload_fill(df):
        csv_2 = df.to_csv(index=False)
        b64 = base64.b64encode(csv_2.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv_2;base64,{b64}" download="fill_rate.csv">Download Fill Rate CSV File</a>'
        return href

    st.sidebar.markdown(filedownload_null(null_rate_df), unsafe_allow_html=True)
    st.sidebar.markdown(filedownload_fill(fill_rate_df), unsafe_allow_html=True)

    
    
    
    # number of words in street address
    df['no_of_words_in_street_address'] = df['street_address'].apply(lambda x:len(str(x).split()))

    # number of characters in location name
    df['no_of_characters_in_location_name'] = df['location_name'].str.len()

    # number of words in location name
    df['no_of_words_in_location'] = df['location_name'].apply(lambda x:len(str(x).split()))
    
    # street address (word length)
    def street_add_word():
        data_street = df[df['no_of_words_in_street_address'] == next_words]
        data_street.reset_index(inplace=True,drop=True)
        return data_street['ds_instance_id'].value_counts().to_dict()



    st.markdown("<h4 >Enter the street address word length :</h4>", unsafe_allow_html=True)
    next_words = slider = st.slider('', 5, 800)
    button = st.button('Enter')
    
    if button:
        st.markdown(f"""<h3 style='text-align: center; color: white;background :rgba(0, 0, 255, 0.9);'> {street_add_word()}</h3>""", unsafe_allow_html=True)
