import numpy as np
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
    @st.cache
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