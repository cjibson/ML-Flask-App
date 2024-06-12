import json
import datetime
import os

import alpaca_trade_api as tradeapi
import pandas as pd
import yfinance as yf

from alpaca_keys import alpaca_config

#Function to obtain data from Yahoo Finance
def get_data_from_yahoo(tickers, start_date, end_date):
    #Initialize an empty DataFrame to store the data
    data = pd.DataFrame()

    #Loop through each ticker and retrieve data
    for ticker in tickers:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        stock_data['Ticker'] = ticker
        data = pd.concat([data, stock_data], axis=0)

    #Reset index to ensure 'Date' becomes a column
    data.reset_index(inplace=True)

    return data

#Function to store the data on AWS Cloud9 server
def store_csv_data(data):
    file_path = r'C:\Users\jibso\OneDrive\Desktop\machine-learning-and-data-analytics\Machine-Learning-and-Data-Analytics\live_trading_bot\data\stock_data.csv'
    #If the file already exists, append new data to it
    if os.path.exists(file_path):
        existing_data = pd.read_csv(file_path)
        updated_data = pd.concat([existing_data, data], axis=0)
        updated_data.to_csv(file_path, index=False)
    else:
        data.to_csv(file_path, index=False)

#Function for mean_reversion_strategy
def mean_reversion_strategy(data):
    #Calculate the mean of the closing prices
    mean_price = data['Close'].mean()

    #Determine the position based on the current closing price compared to the mean
    if data['Close'].values[-1] < mean_price:
        return 'buy'
    elif data['Close'].values[-1] > mean_price:
        return 'sell'
    else:
        return 'hold'

#Function for bollinger_bands_strategy
def bollinger_bands_strategy(data, window=20, num_std=2):
    #Calculate rolling mean and standard deviation
    rolling_mean = data['Close'].rolling(window=window).mean()
    rolling_std = data['Close'].rolling(window=window).std()

    #Calculate upper and lower bands
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)

    #Determine the position based on the current closing price compared to the bands
    if data['Close'].values[-1] > upper_band.values[-1]:
        return 'sell'
    elif data['Close'].values[-1] < lower_band.values[-1]:
        return 'buy'
    else:
        return 'hold'

#Function for sma_crossover_strategy
def sma_crossover_strategy(data, short_window=50, long_window=200):
    #Calculate short and long moving averages
    data['Short_SMA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['Long_SMA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

    #Determine the position based on the crossover of short and long moving averages
    if data['Short_SMA'].values[-1] > data['Long_SMA'].values[-1] and \
            data['Short_SMA'].values[-2] < data['Long_SMA'].values[-2]:
        return 'buy'
    elif data['Short_SMA'].values[-1] < data['Long_SMA'].values[-1] and \
            data['Short_SMA'].values[-2] > data['Long_SMA'].values[-2]:
        return 'sell'
    else:
        return 'hold'

#Function to perform_analysis
def perform_analysis(data):
    results = []  #List to store results for each day
    stocks_to_buy = []  #List to store stocks to buy on the last day
    stocks_to_sell = []  #List to store stocks to sell on the last day
    grouped_data = data.groupby('Ticker')
    
    #Loop through each day in the data
    for index, row in data.iterrows():
        analysis_result = {}  # Dictionary to store analysis result for the current day
        
        #Make a copy of the data up to the current day for analysis
        data_slice = data.iloc[:index+1].copy()
        
        #Mean Reversion strategy
        mean_reversion_signal = mean_reversion_strategy(data_slice)
        
        #Bollinger Bands strategy
        bollinger_bands_signal = bollinger_bands_strategy(data_slice)
        
        #Simple Moving Average Crossover strategy
        sma_crossover_signal = sma_crossover_strategy(data_slice)
        
        #Determine the overall position based on the signals
        if 'buy' in [mean_reversion_signal, bollinger_bands_signal, sma_crossover_signal]:
            position = 'Long'
        elif 'sell' in [mean_reversion_signal, bollinger_bands_signal, sma_crossover_signal]:
            position = 'Short'
        else:
            position = 'Hold'
        
        #Print the analysis for the current day
        print(f"Date: {row['Date']}")
        print(f"Stock: {row['Ticker']}")
        print(f"Open: ${row['Open']:.2f}")
        print(f"Close: ${row['Close']:.2f}")
        print(f"Mean Reversion: {mean_reversion_signal}")
        print(f"SMA Crossover: {sma_crossover_signal}")
        print(f"Bollinger Bands: {bollinger_bands_signal}")
        print(f"Position: {position}")
        print()
        
        #Store the analysis results for the current day
        analysis_result['Date'] = str(row['Date'])  #Convert Timestamp to string
        analysis_result['Stock'] = row['Ticker']
        analysis_result['Open'] = round(row['Open'], 2)
        analysis_result['Close'] = round(row['Close'], 2)
        analysis_result['Mean Reversion'] = mean_reversion_signal
        analysis_result['SMA Crossover'] = sma_crossover_signal
        analysis_result['Bollinger Bands'] = bollinger_bands_signal
        analysis_result['Position'] = position
        
        #Append the analysis result to the list of results
        results.append(analysis_result)
        
        #Check if it's the last day for the current ticker and add stocks to buy or sell lists accordingly
        if index == grouped_data.groups[row['Ticker']][-1]:
            if mean_reversion_signal == 'buy' or sma_crossover_signal == 'buy' or bollinger_bands_signal == 'buy':
                stocks_to_buy.append(row['Ticker'])
            if mean_reversion_signal == 'sell' or sma_crossover_signal == 'sell' or bollinger_bands_signal == 'sell':
                stocks_to_sell.append(row['Ticker'])
    
    #Print the list of stocks to buy and sell on the last day
    if stocks_to_buy:
        print("You should buy the following stocks today:", ', '.join(stocks_to_buy))
    if stocks_to_sell:
        print("You should sell the following stocks today:", ', '.join(stocks_to_sell))
    
    #Determine which strategy made the most profit
    profits = {'Mean Reversion': 0, 'Bollinger Bands': 0, 'SMA Crossover': 0}
    for result in results:
        if result['Mean Reversion'] == 'buy' or result['Mean Reversion'] == 'sell':
            profits['Mean Reversion'] += 1
        if result['Bollinger Bands'] == 'buy' or result['Bollinger Bands'] == 'sell':
            profits['Bollinger Bands'] += 1
        if result['SMA Crossover'] == 'buy' or result['SMA Crossover'] == 'sell':
            profits['SMA Crossover'] += 1
    
    max_profit_strategy = max(profits, key=profits.get)
    max_profit_value = profits[max_profit_strategy]
    
    #Print the strategy that made the most profit and its value
    print(f"The strategy that made the most profit is {max_profit_strategy} with {max_profit_value} profitable trades.")
    
    #Store results in a JSON object
    results_dict = {'Results': results, 'Max Profit Strategy': max_profit_strategy}
    store_results(results_dict)
    
    #Return the stocks to buy and sell
    return stocks_to_buy, stocks_to_sell

#Function to store
def store_results(results_dict):
    
    with open(r'C:\Users\jibso\OneDrive\Desktop\machine-learning-and-data-analytics\Machine-Learning-and-Data-Analytics\live_trading_bot\results.json', 'w') as f:
        json.dump(results_dict, f, indent=4)
        
#Function to submit paper orders to Alpaca paper trading account
def submit_paper_orders(alpaca_config, stocks_to_buy, stocks_to_sell):
    #Initialize Alpaca API
    api = tradeapi.REST(alpaca_config['id'], alpaca_config['secret_key'], base_url='https://paper-api.alpaca.markets')

    #Submit paper orders to buy
    for stock in stocks_to_buy:
        #Submit a market order to buy 1 share of the stock
        api.submit_order(
            symbol=stock,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"Paper order to buy {stock} submitted.")

    #Submit paper orders to sell
    for stock in stocks_to_sell:
        #Submit a market order to sell 1 share of the stock
        api.submit_order(
            symbol=stock,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print(f"Paper order to sell {stock} submitted.")

#Main function
def main():
    #Define the list of stock tickers to retrieve data for
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NFLX', 'TSLA', 'NVDA', 'AMD', 'INTC']

    #Define start and end dates for data retrieval
    start_date = datetime.datetime.now() - datetime.timedelta(days=365)
    end_date = datetime.datetime.now()

    #Obtain data from Yahoo Finance
    data = get_data_from_yahoo(tickers, start_date, end_date)

    #Store the data
    store_csv_data(data)

    #Perform analysis on the data
    stocks_to_buy, stocks_to_sell = perform_analysis(data)

    #Submit paper orders to Alpaca paper trading account
    submit_paper_orders(alpaca_config, stocks_to_buy, stocks_to_sell)

if __name__ == "__main__":
    main()