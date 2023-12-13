# AIaaS Falcon Observability

# Falcon Observability

The Falcon Observability project is a Streamlit-based application designed for comprehensive log analytics and performance evaluation of AI models. This tool offers insightful visualizations and metrics derived from log data, enabling users to assess model behavior, track performance indicators, and conduct cost analysis for Azure services based on token usage.

## Features

### Log Analytics and Visualization

·        **Date Range Selection**: Allows users to select date ranges for log analysis.

·        **Time Filtering**: Provides the option to filter logs based on specified start and end times.

·        **Filter ID Input**: Enables users to input a filter ID for more granular log retrieval.

·        **Log Display**: Renders log data in a table format using Streamlit's `st.data_editor`.

·        **Request Flow Visualization**: Generates a line chart using Plotly Express to visualize the flow of requests over time.

·        **Average Token Count Visualization**: Displays the average token count over time in a line chart.

### Performance Analysis

·        **Metrics Overview**: Presents metrics such as total requests, average perplexity, toxicity, ARI (Automated Readability Index), Flesch-Kincaid Grade (FKG), total/request token count, and average token count.

·        **Performance Metrics Visualization**: Offers a detailed analysis of model performance metrics (e.g., Perplexity, Toxicity, ARI, FKG) over time through line chart visualizations.

### Cost Analysis (Azure)

·        **Token-Based Cost Calculation**: Computes and displays costs for Azure services based on token usage rates.

·        **Price Visualization**: Illustrates the calculated prices for request and response tokens in a line chart and table format.

### User Interface and Interaction

·        **Sidebar Selection**: Allows users to choose between 'Online' or 'Local' mode for log retrieval.

·        **Form Submission**: Utilizes Streamlit forms for submitting date range, time, and filter criteria.

·        **Expander for Data Selection**: Provides an expandable interface for users to select log data based on specified criteria.

·        **Performance Analysis Trigger**: Allows users to trigger the analysis of model performance metrics with a button click.

### Session State Management

·        **State Persistence**: Uses Streamlit's session state (`st.session_state`) to manage and update various analytics results, loading states, and dataframes.

## Installation

Clone the repository and install the required dependencies:

```
pip install falcon_observability
```
## Usage

### Starting the Service
```
from falcon_observability.main import FalconObservability
server=FalconObservability(port=8555)
server.start()
```


### Manage Service
```
server.status()
```


### Stop Service
```
server.stop()
```

