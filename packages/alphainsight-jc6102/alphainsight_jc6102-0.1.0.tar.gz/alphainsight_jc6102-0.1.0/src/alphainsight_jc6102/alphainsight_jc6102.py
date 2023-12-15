import requests
import pandas as pd
import os

class AlphaVantageClient:
    """
    A client for fetching financial data from the Alpha Vantage API.

    This client provides methods to access various financial data including stock prices, 
    foreign exchange rates, technical indicators, and cryptocurrency data.

    Attributes:
        api_key (str): The API key for accessing the Alpha Vantage API.
        base_url (str): The base URL for the Alpha Vantage API.
    """
    def __init__(self, api_key):
        """
        Initializes the AlphaVantageClient with the provided API key.

        Args:
            api_key (str): The API key for accessing the Alpha Vantage API.
        """
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
      
    
    def get_daily_time_series(self, symbol):
        """
        Fetches the daily time series data for a given stock symbol from Alpha Vantage.

        This function queries the Alpha Vantage API to retrieve daily stock price data,
        including open, high, low, close values, and volume. The data is then transformed
        into a pandas DataFrame for easy manipulation and analysis.

        Args:
            symbol (str): The stock symbol to query for (e.g., 'AAPL' for Apple Inc.).

        Returns:
            pandas.DataFrame: A DataFrame with the daily time series data, indexed by date.
            The columns of the DataFrame include 'Open', 'High', 'Low', 'Close', and 'Volume'.
            Returns None if the data is not found or if an error occurs.

        Raises:
            Prints an error message if the API request fails or the expected data
            is not found in the API response.
        """
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
                data = response.json()
                if 'Time Series (Daily)' in data:
                      time_series_data = data['Time Series (Daily)']
                      df = pd.DataFrame.from_dict(time_series_data, orient='index')
                      df.index = pd.to_datetime(df.index)
                      df.sort_index(inplace=True)
                      df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                      return df
                else:
                      # Print the response if the expected key is not found
                      print("Expected key 'Time Series (Daily)' not found in the response. Response:", data)
                      return None
        else:
                  print(f"Error: Request failed with status code {response.status_code}")
                  return None

    
    def get_forex_data(self, from_currency, to_currency):
        """
        Fetches real-time exchange rate data for the given currency pair.

        Args:
            from_currency (str): The currency code for the base currency.
            to_currency (str): The currency code for the target currency.

        Returns:
            dict: A dictionary containing the exchange rate data, or
                  None if an error occurs.
        """
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": self.api_key
            }
        response = requests.get(self.base_url, params=params)
           
        if response.status_code == 200:
                  try:
                        data = response.json()
                        return data
                  except ValueError:
                        print("Error: Unable to decode JSON response")
                        return None
        else:
                  print(f"Error: Request failed with status code {response.status_code}")
                  return None
            

        
    def transform_forex_data(self, forex_data):
        """
        Transforms the raw forex data into a structured pandas DataFrame.

        Args:
            forex_data (dict): Raw forex data as returned by the get_forex_data method.

        Returns:
            DataFrame: A pandas DataFrame containing the transformed forex data.
        """
        exchange_rate_info = forex_data['Realtime Currency Exchange Rate']
        df = pd.DataFrame([exchange_rate_info.values()], columns=exchange_rate_info.keys())
        df.columns = ['From Currency Code', 'From Currency Name', 'To Currency Code', 
                      'To Currency Name', 'Exchange Rate', 'Last Refreshed', 
                      'Time Zone', 'Bid Price', 'Ask Price']
        df['Exchange Rate'] = pd.to_numeric(df['Exchange Rate'], errors='coerce')
        df['Bid Price'] = pd.to_numeric(df['Bid Price'], errors='coerce')
        df['Ask Price'] = pd.to_numeric(df['Ask Price'], errors='coerce')
        df['Last Refreshed'] = pd.to_datetime(df['Last Refreshed'], errors='coerce')
        return df
          
    
    def get_sma(self, symbol, interval, time_period, series_type):
        """
        Fetches the Simple Moving Average (SMA) for a given stock symbol.

        Args:
            symbol (str): The stock symbol to fetch the SMA for.
            interval (str): Time interval (e.g., 'daily', 'weekly', 'monthly').
            time_period (int): Number of data points used to calculate the SMA.
            series_type (str): The type of price series ('close', 'open', 'high', 'low').

        Returns:
            dict: A dictionary containing the SMA data, or None if an error occurs.
        """
        params = {
                "function": "SMA",
                "symbol": symbol,
                "interval": interval,  # e.g., daily, weekly, monthly
                "time_period": time_period,
                "series_type": series_type,  # e.g., close, open, high, low
                "apikey": self.api_key
                }
        response = requests.get(self.base_url, params=params)
        return response.json() if response.status_code == 200 else None

     
      
    def get_rs(self, symbol, interval, time_period, series_type):
        """
        Fetches the Relative Strength Index (RSI) for a given stock symbol.

        Args:
            symbol (str): The stock symbol to fetch the RSI for.
            interval (str): Time interval (e.g., 'daily', 'weekly', 'monthly').
            time_period (int): Number of data points used to calculate the RSI.
            series_type (str): The type of price series ('close', 'open', 'high', 'low').

        Returns:
            dict: A dictionary containing the RSI data, or None if an error occurs.
        """
        params = {
                "function": "RSI",
                "symbol": symbol,
                "interval": interval,
                "time_period": time_period,
                "series_type": series_type,
                "apikey": self.api_key
                }
        response = requests.get(self.base_url, params=params)
        return response.json() if response.status_code == 200 else None
     

    def clean_sma_data(self, sma_data):
        """
        Cleans and structures the SMA data into a pandas DataFrame.

        Args:
            sma_data (dict): Raw SMA data as returned by the get_sma method.

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned SMA data.
        """
        if not sma_data or "Technical Analysis: SMA" not in sma_data:
                print("Invalid or empty data")
                return None
            
        sma_values = sma_data["Technical Analysis: SMA"]
        df = pd.DataFrame.from_dict(sma_values, orient='index')
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df.columns = ['SMA']
        df['SMA'] = pd.to_numeric(df['SMA'], errors='coerce')
        return df
        """
        Cleans and structures the SMA data into a pandas DataFrame.

        Args:
            sma_data (dict): Raw SMA data as returned by the get_sma method.

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned SMA data.
        """
    
    def clean_rsi_data(self, rsi_data):
        """
        Cleans and structures the SMA data into a pandas DataFrame.

        Args:
            sma_data (dict): Raw SMA data as returned by the get_sma method.

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned SMA data.
        """
        if not rsi_data or "Technical Analysis: RSI" not in rsi_data:
            print("Invalid or empty RSI data")
            return None

        rsi_values = rsi_data["Technical Analysis: RSI"]
        df = pd.DataFrame.from_dict(rsi_values, orient='index')
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        df.columns = ['RSI']
        df['RSI'] = pd.to_numeric(df['RSI'], errors='coerce')
        return df
    
    def get_etf_data(self, etf_symbol, time_frame='daily'):
        """
        Cleans and structures the SMA data into a pandas DataFrame.

        Args:
            sma_data (dict): Raw SMA data as returned by the get_sma method.

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned SMA data.
        """
        if time_frame == 'daily':
                return self.get_daily_time_series(etf_symbol)
        elif time_frame == 'weekly':
                return self.get_weekly_adjusted(etf_symbol)
      
    
    def get_crypto_data(self, symbol, market, time_frame='daily'):
        """
        Cleans and structures the SMA data into a pandas DataFrame.

        Args:
            sma_data (dict): Raw SMA data as returned by the get_sma method.

        Returns:
            DataFrame: A pandas DataFrame containing the cleaned SMA data.
        """
        function_map = {
                'daily': 'DIGITAL_CURRENCY_DAILY',
                'weekly': 'DIGITAL_CURRENCY_WEEKLY',
                'monthly': 'DIGITAL_CURRENCY_MONTHLY'
                }
        function = function_map.get(time_frame, 'DIGITAL_CURRENCY_DAILY')

        params = {
                "function": function,
                "symbol": symbol,
                "market": market,
                "apikey": self.api_key
                }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
                data = response.json()
                  # The key in the JSON response for the time series data varies based on the function
                time_series_key = f"Time Series (Digital Currency {time_frame.title()})"
                if time_series_key in data:
                        df = pd.DataFrame.from_dict(data[time_series_key], orient='index')
                        df.index = pd.to_datetime(df.index)
                        df.sort_index(inplace=True)
                        return df
                else:
                        print("Data not found")
                        return None
        else:
                print(f"Error: Request failed with status code {response.status_code}")
                return None
     
