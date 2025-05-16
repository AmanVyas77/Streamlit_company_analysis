#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import streamlit as st

# --- Configuration ---
API_KEY_VALUE = "hRz4U9BEIn4HhX2Qozlq5sEzMORI88ep" # Ensure this is your valid API key
API_KEY_PARAM_STRING = f"apikey={API_KEY_VALUE}"
BASE_URL = 'https://financialmodelingprep.com/api'
# --- End Configuration ---

st.set_page_config(layout="wide")
st.header('Financial Modeling Prep Stock Screener')

# Sidebar for inputs
symbol_input = st.sidebar.text_input('Ticker:', value='COF')

financial_data_options_corrected = (
    'income-statement', 'balance-sheet-statement',
    'cash-flow-statement',
    'income-statement-growth',
    'balance-sheet-statement-growth', 'cash-flow-statement-growth',
    'ratios-ttm', 'ratios', 'financial-growth', 'quote', 'rating',
    'enterprise-values', 'key-metrics-ttm', 'key-metrics',
    'historical-rating', 'discounted-cash-flow',
    'historical-discounted-cash-flow-statement', 'historical-price-full',
    'Historical Price smaller intervals'
)
selected_financial_data_type = st.sidebar.selectbox(
    'Financial Data Type',
    options=financial_data_options_corrected,
    index=financial_data_options_corrected.index('income-statement-growth')
)

api_path_financial_data = selected_financial_data_type

if selected_financial_data_type == 'Historical Price smaller intervals':
    interval_options = ('1min', '5min', '15min', '30min', '1hour', '4hour')
    interval = st.sidebar.selectbox('Interval', options=interval_options)
    api_path_financial_data = f'historical-chart/{interval}'

transpose_option = st.sidebar.selectbox('Transpose', options=('Yes', 'No'))

url = f'{BASE_URL}/v3/{api_path_financial_data}/{symbol_input}?{API_KEY_PARAM_STRING}'

st.write("--- Debug Info ---") # Start of debug section
st.write(f"1. Constructed URL: {url}")

try:
    response = requests.get(url)
    st.write(f"2. API Response Status Code: {response.status_code if response else 'No Response Object'}")

    if response is None:
        st.error("Failed to get a response object from the API request.")
    else:
        response.raise_for_status()
        data = response.json()
        st.write("3. Raw data from API (first 500 chars or type):")
        if isinstance(data, (list, dict)) and data:
            st.text(str(data)[:500] + "...") # Show a snippet of the data
        else:
            st.write(f"Type of data: {type(data)}, Data: {data}")


        if data:
            data_for_df = []
            if isinstance(data, dict) and not data.get('Error Message'):
                 data_for_df = [data]
            elif isinstance(data, list):
                 data_for_df = data
            elif isinstance(data, dict) and data.get('Error Message'):
                st.error(f"API Error Message in data: {data['Error Message']}")
                # data_for_df remains empty
            else:
                st.warning(f"Unexpected data format received from API: {type(data)}")
                # data_for_df remains empty
            
            st.write(f"4. data_for_df (length {len(data_for_df)}):")
            if data_for_df:
                st.text(str(data_for_df)[:500] + "...")
            else:
                st.write("data_for_df is empty.")


            if data_for_df:
                df_intermediate = None
                st.write("5. Attempting to create DataFrame...")
                try:
                    if transpose_option == 'Yes':
                        df_intermediate = pd.DataFrame(data_for_df).T
                    else:
                        df_intermediate = pd.DataFrame(data_for_df)
                    st.write("6. DataFrame created. Shape:", df_intermediate.shape if df_intermediate is not None else "None")
                except Exception as e:
                    st.error(f"Error creating DataFrame: {e}")
                    st.stop() # Stop execution if DataFrame creation fails

                
                if df_intermediate is not None and not df_intermediate.empty:
                    st.write("7. DataFrame is not empty. Attempting to display...")
                    df_display = df_intermediate.astype(str)
                    st.write("--- End of Debug Info ---")
                    st.write(df_display) # This is your actual target display
                elif df_intermediate is not None and df_intermediate.empty:
                     st.info("DataFrame is empty after processing (e.g., API returned empty list).")
                     st.write("--- End of Debug Info ---")
                else: # df_intermediate is None (should be caught by the exception above, but as a fallback)
                    st.warning("DataFrame (df_intermediate) is None.")
                    st.write("--- End of Debug Info ---")
            else:
                # This case is hit if data_for_df remains an empty list after initial checks
                if not (isinstance(data, dict) and data.get('Error Message')):
                    st.info("No data to display because 'data_for_df' was empty.")
                st.write("--- End of Debug Info ---")
        else:
            st.info("API returned no data (empty response).")
            st.write("--- End of Debug Info ---")

except requests.exceptions.HTTPError as errh:
    st.error(f"HTTP Error: {errh}")
    st.error(f"URL called: {url}")
    if 'response' in locals() and response is not None:
        st.text_area("API Response Content (if available):", response.text, height=200)
    st.write("--- End of Debug Info ---")
except requests.exceptions.ConnectionError as errc:
    st.error(f"Error Connecting: {errc}")
    st.write("--- End of Debug Info ---")
except requests.exceptions.Timeout as errt:
    st.error(f"Timeout Error: {errt}")
    st.write("--- End of Debug Info ---")
except requests.exceptions.RequestException as err:
    st.error(f"An unexpected error occurred with the request: {err}")
    st.write("--- End of Debug Info ---")
except ValueError as json_err:  # Catches JSONDecodeError
    st.error(f"JSON Decode Error: The API response was not in valid JSON format. {json_err}")
    if 'response' in locals() and response is not None:
        st.text_area("Problematic API Response Text (if available):", response.text, height=200)
    st.write("--- End of Debug Info ---")
except Exception as e_global: # Catch any other unexpected error
    st.error(f"A global unexpected error occurred: {e_global}")
    st.write("--- End of Debug Info ---")


# In[7]:


# Example app.py structure:
import requests
import pandas as pd
import streamlit as st

# --- Configuration ---
# Make sure to replace 'YOUR_ACTUAL_API_KEY_HERE' with your real API key
# It's better to use Streamlit secrets or environment variables for API keys
API_KEY_VALUE = "hRz4U9BEIn4HhX2Qozlq5sEzMORI88ep" # Replace with your key
API_KEY_PARAM_STRING = f"apikey={API_KEY_VALUE}"
BASE_URL = 'https://financialmodelingprep.com/api'
# --- End Configuration ---

st.header('Financial Modeling Prep Stock Screener')
# ... (rest of the corrected Streamlit code from above) ...
# Make sure to use BASE_URL and API_KEY_PARAM_STRING in the url f-string:
# url = f'{BASE_URL}/v3/{api_path_financial_data}/{symbol_input}?{API_KEY_PARAM_STRING}'


# In[ ]:




