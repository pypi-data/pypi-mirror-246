import datetime

import pandas as pd

from streamlit_autorefresh import st_autorefresh
from streamlit_extras.mandatory_date_range import date_range_picker
import streamlit as st

st.set_page_config(layout="wide", page_title="Log Monitor", page_icon="📈")
from utils.format import format_json, get_filter_local, read_text_from_file, time_intervals, convert_to_iso, get_log


def call_for_log(start_date, end_date, start_time, end_time, filter):
    start_timestamp, end_timestamp = convert_to_iso(str(start_date), str(end_date), start_time, end_time)

    responses = {'start_date': start_timestamp, 'end_date': end_timestamp, 'filter': filter}
    if option == 'Online':

        results = get_log(responses, api_key_input)
    else:
        if uploaded_file:
            results = get_filter_local(st.session_state['original_file'],responses)
        else:
            results = pd.DataFrame(
                {"timestamp": ["Now"], "logId": ["00000"], "level": ["START"], "message": ["Hello, start a query"]})
    st.session_state['log_current'] = results


col1, col2 = st.columns([3, 1])

col2.image('./static/AIAAS_FALCON.jpg')

col1.markdown("# Log Monitor")
st.sidebar.header("Authentication")
option = st.sidebar.selectbox(
    'Selection Mode',
    ('Online', 'Local'))
if option == 'Local':
    api_key_input = ''
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file:
        response = format_json(uploaded_file)
        st.session_state['log_current'] = response
        st.session_state['original_file']=response
else:
    st.sidebar.selectbox('Endpoint Type',('Falcon_AiaaS','OpenAI/SingtelGPT','Falcon_Audio'))
    api_key_input = st.sidebar.text_input('Falcon API Key', '')
    uploaded_file = ''

st.write(
    """
The Log Monitor tab displays real-time API logs and offers time-based filtering, enabling users to efficiently track and analyze current activities. Enjoy!
"""
)

if 'log_current' not in st.session_state.keys():
    st.session_state['log_current'] = pd.DataFrame(
        {"timestamp": ["Now"], "logId": ["00000"], "level": ["START"], "message": ["Hello, start a query"]})

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
if st.session_state['endtime'] == 'Now' and api_key_input != '':
    count = st_autorefresh(interval=30000, key="fizzbuzzcounter")
    call_for_log(result[0], result[1], t, e, filter)

colu, colu2 = st.columns(2)

st.dataframe(st.session_state['log_current'], width=2000, height=800)
