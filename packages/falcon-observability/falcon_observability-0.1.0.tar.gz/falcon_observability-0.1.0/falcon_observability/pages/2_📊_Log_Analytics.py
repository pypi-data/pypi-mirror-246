import datetime

import pandas as pd
import streamlit as st
from falcon_evaluate.fevaluate_results import ModelScoreSummary
from falcon_evaluate.fevaluate_plot import ModelPerformancePlotter
import time
import plotly.express as px

import numpy as np
from streamlit_autorefresh import st_autorefresh
from streamlit_extras.mandatory_date_range import date_range_picker
from utils.format import time_intervals, get_log, get_filter_local, convert_to_iso, extract_logs_info, format_json, \
    parse_log_data

if 'log_current_an' not in st.session_state.keys():
    st.session_state['loading'] = False
    st.session_state['average_perplexity']='NA'
    st.session_state['average_tox']='NA'
    st.session_state['average_ari']='NA'
    st.session_state['per_ana'] = pd.DataFrame(
        {'time': [], 'log_id': [], 'prompt': [],
         'response': [],'ari': [], "fkg": [], "ppy": [], 'tl': []})

    st.session_state['average_fkg']='NA'
    st.session_state['log_current_an'] = pd.DataFrame(
        {"Select": [True,True,True,True,True],"timestamp": [datetime.datetime(2020, 5, 17,3,50),datetime.datetime(2020, 5, 17,4,50),datetime.datetime(2020, 5, 17,4,50),datetime.datetime(2020, 5, 17,4,50),datetime.datetime(2020, 5, 17,4,55)],"logId": ["00000",'00001','00002','00003','00004'],"Service":["Falcon Dev","Falcon Dev","Falcon Dev",'Azure','Azure'],  'Model':["llama2-13b",'llama2-13b','llama2-13b','gpt-35-turbo-0613-vanilla','gpt-35-turbo-0613-vanilla'],"Prompt": ["What is 1+1","What is the capital of France?","What is the capital of France?","What is the capital of France?","What is the capital of France?"], "Response": ["It is 2", "Paris is the capital of France.","Paris is the capital of France.","Paris is the capital of France.","Paris is the capital of France."],"Request Token":[113,50,32,32,3000],"Response Token":[120,300,32,32,1000],"Other":["","",'','','']})


def call_for_log(start_date, end_date, start_time, end_time, filter):
    start_timestamp, end_timestamp = convert_to_iso(str(start_date), str(end_date), start_time, end_time)

    responses = {'start_date': start_timestamp, 'end_date': end_timestamp, 'filter': filter}
    if option == 'Online':
        results = get_log(responses, api_key_input,True)
        results=extract_logs_info(results)
        results['timestamp'] = pd.to_datetime(results['timestamp']).dt.round("min")

    else:
        if uploaded_file:
            results = get_filter_local(st.session_state['original_file'],responses)
        else:
            results = pd.DataFrame(
                {"timestamp": ["Now"], "logId": ["00000"], "level": ["START"], "message": ["Hello, start a query"]})

    st.session_state['log_current_an'] = results


st.set_page_config(layout="wide", page_title="Plotting Demo", page_icon="📈")
col1, col2 = st.columns([3, 1])

col2.image('./static/AIAAS_FALCON.jpg')
col1.markdown("# Log Analytics")
st.sidebar.header("Authentication")

option = st.sidebar.selectbox(
    'Selection Mode',
    ('Online', 'Local'))
if option == 'Local':
    api_key_input=''
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    if uploaded_file:
        response = parse_log_data(uploaded_file)
        st.session_state['log_current_an'] = response
        st.session_state['original_file']=response
else:
    st.sidebar.selectbox('Endpoint Type',('Falcon_AiaaS','OpenAI/SingtelGPT','Falcon_Audio'))

    api_key_input = st.sidebar.text_input('Falcon API Key', '')
    uploaded_file = ''
st.session_state['test']=''
st.session_state['ec']=''

with st.expander("Data Selector"):
    with st.form('my_form'):
        result = date_range_picker("Select a date range")
        col1, col2 = st.columns(2)

        with col1:
            t = st.time_input('Start Time', datetime.time(0, 0))
        with col2:
            e = st.selectbox('End Time', time_intervals(result), index=len(time_intervals(result)) - 1, key='endtime')

        filter = st.text_input(label='Filter ID')
        submit = st.form_submit_button('Filter')
        if submit:
            call_for_log(result[0], result[1], t, e, filter)
    if st.session_state['endtime'] == 'Now' and api_key_input != '' and st.session_state['loading']==False:
        count = st_autorefresh(interval=30000, key="fizzbuzzcounters")
        call_for_log(result[0], result[1], t, e, filter)

    colu, colu2 = st.columns(2)
    with st.form('data_selector'):
        data=st.data_editor(st.session_state['log_current_an'], width=2000, height=400)
        data_submit = st.form_submit_button('Get Analytics')
        if data_submit:
            with st.spinner('Initialising'):
                import nltk
                nltk.download('punkt')
            with st.spinner('Processing'):
                st.session_state['filtered_df'] = data[data['Select'] == True]
                st.session_state['formatted_df'] = pd.DataFrame({
                    'prompt': list(st.session_state['filtered_df']['Prompt']),
                    'reference': [' ' for _ in range(len(st.session_state['filtered_df']))],
                    'response': list(st.session_state['filtered_df']['Response'])
                })
                st.session_state['formatted_df'].reset_index(drop=True, inplace=True)



col1, col2, col3,col4,col5 = st.columns(5)
col1.metric("Total Request", len(st.session_state['log_current_an']))
col2.metric("Average Perplexity", st.session_state['average_perplexity'])
col3.metric("Average Toxicity",st.session_state['average_tox'])
col4.metric("Average ARI", st.session_state['average_ari'])
col5.metric("Average FKG", st.session_state['average_fkg'])
col6, col7, col8,col9 = st.columns(4)

col8.metric("Total Request Token", st.session_state['log_current_an']['Request Token'].sum())
col9.metric("Total Response Token",st.session_state['log_current_an']['Response Token'].sum())
col6.metric("Average Request Token", round(st.session_state['log_current_an']['Request Token'].mean()))
col7.metric("Average Response Token",round(st.session_state['log_current_an']['Response Token'].mean()))
st.markdown('### Request Analysis')

col1, col2 = st.columns(2)


def request_flow():
    counts_per_timestamp = st.session_state['log_current_an']['timestamp'].value_counts().sort_index()

    # Create a new DataFrame with timestamp and corresponding counts
    data = {'timestamp': counts_per_timestamp.index, 'count': counts_per_timestamp.values}
    counts_df = pd.DataFrame(data)
    return counts_df


# Assuming `col1` is a Streamlit column defined elsewhere in your code
with col1:
    st.markdown('#### Request Flow')

    # Get data for Plotly chart
    data_for_chart = request_flow()

    # Create a Plotly line chart
    fig = px.line(data_for_chart, x='timestamp', y='count', title='Request Flow')

    # Render the Plotly chart using Plotly's `plotly_chart` function
    st.plotly_chart(fig)


def average_token_count():
    # Assuming 'log_current_an' contains the DataFrame with 'timestamp', 'Request Token', and 'Response Token'
    data = st.session_state['log_current_an']

    # Group data by timestamp and calculate the mean of Request Token and Response Token
    averaged_data = data.groupby('timestamp')[['Request Token', 'Response Token']].mean().reset_index()
    return averaged_data


# Assuming `col2` is a Streamlit column defined elsewhere in your code
with col2:
    st.markdown('#### Average Token Count')

    # Get data for Plotly chart
    averaged_data = average_token_count()

    if not averaged_data.empty:
        # Create a Plotly line chart
        fig = px.line(averaged_data, x='timestamp', y=['Request Token', 'Response Token'], title='Average Token Count')

        # Render the Plotly chart using Plotly's `plotly_chart` function
        st.plotly_chart(fig)
    else:
        st.write("No data available for visualization.")

col11, col12 = st.columns([3, 1])
with col11:
    st.markdown('### Performance Analysis')
with col12:
    ana=st.button('Load Performance Analyse (Take a Break)')
if ana:
    with st.spinner('Analysing'):
        st.session_state['loading'] = True
        model_score_summary = ModelScoreSummary(st.session_state['formatted_df'])
        result, agg_score = model_score_summary.execute_summary(False)
        st.session_state['average_perplexity']=round(agg_score['response-Scores'][0]['Language Modeling Performance']['Perplexity'])
        st.session_state['average_tox']=round(agg_score['response-Scores'][0]['Text Toxicity']['Toxicity Level'])
        st.session_state['average_ari']=round(agg_score['response-Scores'][0]['Readability and Complexity']['ARI'])
        st.session_state['average_fkg']=round(agg_score['response-Scores'][0]['Readability and Complexity']['Flesch-Kincaid Grade Level'])
        ari = result['response-Scores'].apply(lambda x: x['Readability and Complexity']['ARI'])
        fkg = result['response-Scores'].apply(
            lambda x: x['Readability and Complexity']['Flesch-Kincaid Grade Level'])
        ppy = result['response-Scores'].apply(lambda x: x['Language Modeling Performance']['Perplexity'])
        tl = result['response-Scores'].apply(lambda x: x['Text Toxicity']['Toxicity Level'])
        st.session_state['per_ana']=pd.DataFrame({'time':st.session_state['filtered_df']['timestamp'],'log_id':st.session_state['filtered_df']['logId'],'prompt':st.session_state['filtered_df']['Prompt'],'response':st.session_state['filtered_df']['Response'],'ari': ari, "fkg": fkg, "ppy": ppy, 'tl': tl})

chart3=st.plotly_chart(px.line(st.session_state['per_ana'], x='time', y=['ari', 'fkg', 'ppy', 'tl'], title='Metrics over Time'), use_container_width=True)
chart6=st.dataframe(st.session_state['per_ana'])
import pandas as pd

# Assuming st.session_state['log_current_an'] contains the DataFrame

# Sample data for token rates
token_rates = [
    {
        'model': "gpt-35-turbo-0613-vanilla",
        "request_token_per_k": 0.0015,
        "response_token_per_k": 0.002
    },
    {
        "model": "gpt-35-turbo-16k-0613-vanilla",
        "request_token_per_k": 0.003,
        "response_token_per_k": 0.004
    }
]

# Convert token_rates into a DataFrame for easier lookup
token_rates_df = pd.DataFrame(token_rates)

# Filter rows where 'Service' is 'Azure'
azure_rows = st.session_state['log_current_an'][st.session_state['log_current_an']['Service'] == 'Azure'].copy()

# Calculate price for each row
for index, row in azure_rows.iterrows():
    model = row['Model']
    request_token_rate = token_rates_df[token_rates_df['model'] == model]['request_token_per_k'].values[0]
    response_token_rate = token_rates_df[token_rates_df['model'] == model]['response_token_per_k'].values[0]

    # Calculate prices
    request_price = (row['Request Token']/1000) * request_token_rate
    response_price = (row['Response Token']/1000) * response_token_rate
    azure_rows = azure_rows.drop('Select', axis=1, errors='ignore')

    # Add columns to the DataFrame with calculated prices
    azure_rows.at[index, 'Price'] = request_price+response_price


# Display the DataFrame with calculated prices

st.markdown('### Cost Analysis (Azure)')
if len(azure_rows):
    chart7 = st.line_chart(azure_rows.reset_index(drop=True),x='timestamp',y='Price')
st.dataframe(azure_rows.reset_index(drop=True))

