
import requests
import pandas as pd
import streamlit as st


API_KEY_VALUE = "hRz4U9BEIn4HhX2Qozlq5sEzMORI88ep"
API_KEY_PARAM_STRING = f"apikey={API_KEY_VALUE}"
BASE_URL = 'https://financialmodelingprep.com/api'


st.set_page_config(layout="wide")
st.header('Financial Modeling Prep Stock Screener')


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

st.write("--- Debug Info ---") 
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
            st.text(str(data)[:500] + "...") 
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
                
            else:
                st.warning(f"Unexpected data format received from API: {type(data)}")
           
            
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
                    st.stop() 

                
                if df_intermediate is not None and not df_intermediate.empty:
                    st.write("7. DataFrame is not empty. Attempting to display...")
                    df_display = df_intermediate.astype(str)
                    st.write("--- End of Debug Info ---")
                    st.write(df_display) 
                elif df_intermediate is not None and df_intermediate.empty:
                     st.info("DataFrame is empty after processing (e.g., API returned empty list).")
                     st.write("--- End of Debug Info ---")
                else: 
                    st.warning("DataFrame (df_intermediate) is None.")
                    st.write("--- End of Debug Info ---")
            else:
                
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
except ValueError as json_err: 
    st.error(f"JSON Decode Error: The API response was not in valid JSON format. {json_err}")
    if 'response' in locals() and response is not None:
        st.text_area("Problematic API Response Text (if available):", response.text, height=200)
    st.write("--- End of Debug Info ---")
except Exception as e_global: 
    st.error(f"A global unexpected error occurred: {e_global}")
    st.write("--- End of Debug Info ---")






import requests
import pandas as pd
import streamlit as st


API_KEY_VALUE = "hRz4U9BEIn4HhX2Qozlq5sEzMORI88ep" 
API_KEY_PARAM_STRING = f"apikey={API_KEY_VALUE}"
BASE_URL = 'https://financialmodelingprep.com/api'


st.header('Financial Modeling Prep Stock Screener')





