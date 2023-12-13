import pandas as pd
import requests

import time
import numpy as np
import datetime


def parse_log_to_dataframe(log_text):
    # Regular expression to match the log pattern
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+) (\w+).+? (\d+)- (.+)'

    # Find all matches
    matches = re.findall(log_pattern, log_text)

    # Create a dataframe from the matches
    df = pd.DataFrame(matches, columns=['timestamp', 'logId', 'level', 'message'])
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round("min")

    return df


def format_json(file):
    text = file.getvalue().decode('utf-8')
    text = text.replace('\\n', '')

    text = text.replace('<startInternalLog>', '')
    text = text.replace('<endInternalLog>', '')
    df = parse_log_to_dataframe(text)
    return df


def get_filter_local(df, responses):
    """
     Filters the given DataFrame based on the provided criteria.

     Parameters:
     df (DataFrame): The DataFrame containing log data.
     responses (dict): A dictionary containing 'start_date', 'end_date', and 'filter' keys.

     Returns:
     DataFrame: The filtered DataFrame.
     """

    # Extracting filter criteria from the responses dictionary
    start_date = responses.get('start_date')
    end_date = responses.get('end_date')
    filter_text = responses.get('filter')

    # Converting start and end dates from ISO format to datetime
    start_date = datetime.datetime.fromisoformat(start_date)
    end_date = datetime.datetime.fromisoformat(end_date)

    # Filtering the DataFrame
    filtered_df = df[
        (pd.to_datetime(df['timestamp']) >= start_date) &
        (pd.to_datetime(df['timestamp']) <= end_date)
        ]

    # If filter_text is provided, further filter the DataFrame
    if filter_text:
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: row.astype(str).str.contains(filter_text).any(), axis=1)
        ]

    return filtered_df


def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."


def time_intervals(result):
    today_date = datetime.datetime.now().date()

    # Format today's date as 'YYYY-MM-DD'
    formatted_today_date = today_date.strftime('%Y-%m-%d')
    # Current time
    now = datetime.datetime.now()

    if result[1] != formatted_today_date:
        now = now.replace(hour=23, minute=59, second=59)

    # Start time at 00:00 of the current day
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # List to store time intervals
    intervals = []

    # Generate intervals
    while start_time < now:
        intervals.append(start_time.strftime('%H:%M:%S'))
        start_time += datetime.timedelta(minutes=30)

    # Append 'Now' to the list
    intervals.append('Now')

    return tuple(intervals)


def convert_to_iso(start_date, end_date, start_time, end_time):
    # Convert date strings to datetime objects
    print(start_time)
    start_datetime = datetime.datetime.strptime(start_date + ' ' + str(start_time), '%Y-%m-%d %H:%M:%S')

    if end_time.lower() == 'now':
        # If end_time is 'Now', use current datetime
        end_datetime = datetime.datetime.now()
    else:
        print(end_time)
        end_datetime = datetime.datetime.strptime(end_date + ' ' + str(end_time), '%Y-%m-%d %H:%M:%S')

    # Convert datetime objects to ISO format
    start_timestamp = start_datetime.isoformat()
    end_timestamp = end_datetime.isoformat()

    return start_timestamp, end_timestamp


import requests
import json


# This function will remain the same for handling API requests
def get_log(config, api_key_input, raw=False):
    url = 'http://10.142.91.197:8443/facclog/falcon_access_logs'
    api_key = api_key_input
    headers = {"X-API-Key": api_key}

    # Prepare your query and variables
    query = """
        query GetLogs($startTimestamp: DateTime, $endTimestamp: DateTime, $logId: String, $searchString: String) {
            getLogs(startTimestamp: $startTimestamp, endTimestamp: $endTimestamp, logId: $logId, searchString: $searchString) {
                timestamp
                logId
                level
                message
            }
        }
    """
    # Convert datetime to ISO format for GraphQL
    start_timestamp = config['start_date']
    end_timestamp = config['end_date']

    # Variables
    variables = {
        'startTimestamp': start_timestamp,
        'endTimestamp': end_timestamp,

    }
    if (config['filter']):
        variables['searchString'] = config['filter']

    # Send POST request
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    # Return the response content as per your requirement
    if not raw:
        return pd.DataFrame.from_dict(response.json()['data']['getLogs'])
    else:
        return response.json()


# The function call_for_log will remain unchanged as per your instructions
import pandas as pd
import re


def extract_logs_info(logs):
    filtered_logs = [log for log in logs["data"]["getLogs"] if
                     "http://localhost:8000/v1/chat/predictLB" in log["message"]]
    grouped_logs = {}
    for log in filtered_logs:
        log_id = re.search(r"id=(\d+)", log["message"])
        if log_id:
            log_id = log_id.group(1)
            if log_id not in grouped_logs:
                grouped_logs[log_id] = {"request_token_length": None, "response_token_length": None, "model": None,
                                        "prompt": None, "response": None}
            request_token_length = re.search(r"request_token_length\":(\d+)", log["message"])
            if request_token_length:
                grouped_logs[log_id]["request_token_length"] = int(request_token_length.group(1))
            response_token_length = re.search(r"response_token_length\":(\d+)", log["message"])
            if response_token_length:
                grouped_logs[log_id]["response_token_length"] = int(response_token_length.group(1))
            model = re.search(r"model\": \"([^\"]+)", log["message"])
            if model:
                grouped_logs[log_id]["model"] = model.group(1)
            prompt = re.search(r'"query": "(.*?)\s*, \"config": {', log['message'])
            if prompt:
                grouped_logs[log_id]["prompt"] = prompt.group(0)[10:-13]
            response = re.search(r'Response=b\'\{"status":"success","message":"(.*?)",', log["message"])
            if response:
                grouped_logs[log_id]["response"] = response.group(1)
            grouped_logs[log_id]["timestamp"] = log['timestamp']

    data = []
    for log_id, info in grouped_logs.items():
        data.append({
            "Select": True,
            "timestamp": info["timestamp"],  # Extract from logs if available
            "logId": log_id,
            "Service": "Falcon Dev",
            "Model": info["model"],
            "Prompt": info["prompt"],
            "Response": info["response"],
            "Request Token": info["request_token_length"],
            "Response Token": info["response_token_length"],
            "Other": ["", "", "", "", ""]
        })

    return pd.DataFrame(data)


# Assuming 'logs_json' contains the provided JSON data
logs_json = {
    "data": {
        # ... (JSON logs data)
    }
}

def parse_log_data(log_data):
    text = log_data.getvalue().decode('utf-8')
    text = text.replace('\\n', '')
    # text = text.replace('<startInternalLog>', '')
    # text = text.replace('<endInternalLog>', '')
    # Updated regular expressions to identify relevant parts of the log
    # Adjusted to match the provided log format more accurately
    regex_query = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} .+ INFO \d+- Text Query:<startInternalLog> (.+?) <endInternalLog>"
    regex_answer_azure = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ .+ INFO \d+- Generated Answer= \{.+ 'message': \{.+, 'content': '(.+)'\}\}"
    regex_answer_other = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ .+ INFO \d+- Generated Answer= \{.+ 'message': '(.+)', 'request_token_length'"
    regex_tokens_azure = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ .+ INFO \d+- Generated Answer= \{.+ 'usage': \{'prompt_tokens': (\d+), 'completion_tokens': (\d+)"
    regex_tokens_other = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ .+ INFO \d+- Generated Answer= \{.+ 'request_token_length': (\d+), 'response_token_length': (\d+)"

    # Splitting the log data into individual lines
    lines = text.split("\n")

    # Lists to store parsed data
    timestamps = []
    log_ids = []

    services = []
    log_levels = []
    models = []
    prompts = []
    responses = []
    request_tokens = []
    response_tokens = []

    # Process each line

    # Process each line
    for line in lines:
        if "Text Query:" in line:
            print(line)
            timestamp_str = line[:19]
            timestamps.append(datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S'))

            log_id_match = re.search(r"INFO (\d+)- Text Query:", line)
            log_ids.append(log_id_match.group(1) if log_id_match else "N/A")

            service_match = re.search(r"Service=<startInternalLog> (.+?) <endInternalLog>", line)
            services.append(service_match.group(1) if service_match else "N/A")

            log_levels.append("INFO")

            model_match = re.search(r"'model': '(.+?)'", line)
            models.append(model_match.group(1) if model_match else "N/A")

            query_match = re.search(regex_query, line)
            prompts.append(query_match.group(1) if query_match else "N/A")

        elif "Generated Answer=" in line:
            service = services[-1]  # Get the last added service

            if service == "azure":
                answer_match = re.search(regex_answer_azure, line)
                responses.append(answer_match.group(1) if answer_match else "N/A")

                tokens_match = re.search(regex_tokens_azure, line)
                if tokens_match:
                    request_tokens.append(int(tokens_match.group(1)))
                    response_tokens.append(int(tokens_match.group(2)))
                else:
                    request_tokens.append(0)
                    response_tokens.append(0)
            else:
                answer_match = re.search(regex_answer_other, line)
                responses.append(answer_match.group(1) if answer_match else "N/A")

                tokens_match = re.search(regex_tokens_other, line)
                if tokens_match:
                    request_tokens.append(int(tokens_match.group(1)))
                    response_tokens.append(int(tokens_match.group(2)))
                else:
                    request_tokens.append(0)
                    response_tokens.append(0)
    # Create a DataFrame
    df = pd.DataFrame({
        'Select': [True] * len(timestamps),
        'timestamp': timestamps,
        'logId': log_ids,
        'Service': services,
        'LogLevel': log_levels,
        'Model': models,
        'Prompt': prompts,
        'Response': responses,
        'Request Token': request_tokens,
        'Response Token': response_tokens,
        'Other': ['']*len(timestamps)
    })
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round("min")

    return df