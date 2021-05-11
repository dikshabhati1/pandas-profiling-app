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
    
    
   
    def dfs_tabs(df_list, sheet_list, file_name):
        writer = pd.ExcelWriter(file_name,engine='xlsxwriter')   
        for dataframe, sheet in zip(df_list, sheet_list):
            dataframe.to_excel(writer, sheet_name=sheet, startrow=0 , startcol=0)   
        writer.save()

    # list of dataframes and sheet names
    dfs = [null_rate_df,fill_rate_df]
    sheets = ['null_rate_df','fill_rate_df']  
    
    # run function
    excel_file = dfs_tabs(dfs, sheets, 'output_files.xlsx')
    
    def filedownload(df):
        #csv = df.to_csv(index=False)
        b64 = base64.b64encode(excel_file.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(excel_file), unsafe_allow_html=True)
