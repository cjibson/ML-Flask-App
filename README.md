# Machine Learning and Data Analytics Projects

Welcome to my Machine Learning and Data Analytics repository! This repository serves as a portfolio to showcase various machine learning and data analytics projects I've worked on. Each project demonstrates different skills such as web scraping , data preprocessing, model training, ETL pipelines, and data evaluation.

## Table of Contents

- [Web Scraping](#web-scraping)
- [ETL Pipeline](#etl-pipeline)
- [Transactional Database](#transactional-database)
- [Live Trading Bot](#live-trading-bot)
- [ML1](#ml1)
- [ML2](#ml2)
- [ML3](#ml3)
- [Contact Information](#contact-information)

## Web Scraping

Summary:

This project involves web scraping a webpage that lists new metal music releases, extracting relevant data such as the release date, band name, release title, release type, and genre. The data is then cleaned and formatted into a DataFrame using the Pandas library.

The retrieve_data function sends a GET request to the webpage, parses the HTML content using BeautifulSoup, and extracts the desired information from the table containing the releases. It then constructs a DataFrame with the extracted data.

The clean_data function performs data cleaning tasks such as removing leading and trailing whitespaces, extracting relevant information from the release type column, fixing the date format, and filtering the DataFrame to keep only rows with today's date.

The main script retrieves the data from the specified URL, creates a DataFrame, cleans the data, and saves the cleaned data to a CSV file. Finally, it sends the CSV file to a Dropbox folder.

The project is automated to run daily using a batch script and Windows Task Scheduler, ensuring that the latest metal music releases are captured and saved automatically.

## ETL Pipeline

Project Description

## Transactional Database

Description

## Live Trading Bot

Objective:
The goal of this project is to develop an automated trading bot that runs every weekday at market open. The bot retrieves stock data, performs analysis using various trading strategies, and submits paper trading orders via the Alpaca API.

Key Components:

- Data Retrieval:
    - The bot fetches historical stock data for a defined list of tickers from Yahoo Finance using the yfinance library.
    - Data is stored in a CSV file, appending new data to existing records.

- Trading Strategies:
    - Mean Reversion Strategy: Buys when the current closing price is below the mean price and sells when above.
    - Bollinger Bands Strategy: Uses a 20-day rolling mean and standard deviation to determine upper and lower bands. Buys when the price is below the lower band and sells when above the upper band.
    - SMA Crossover Strategy: Uses short (50-day) and long (200-day) simple moving averages. Buys when the short SMA crosses above the long SMA and sells when it crosses below.

- Data Analysis:
    - The bot iterates through the historical data, applying each strategy daily.
    - It determines the overall position (buy, sell, hold) based on the signals from the strategies.
    - Analysis results are stored in a JSON file and printed out.

- Order Submission:
    - Using the Alpaca API, the bot submits paper trading orders for the stocks to buy and sell based on the analysis results.

- Automation:
    - A batch script (run_trading_bot.bat) and Windows Task Scheduler are used to automate the script execution at market open every weekday.

## ML1

Project Description

## ML2

Project Description

## ML3

Project Description

## Contact Information

- **Name**: Connor Jibson
- **Email**: jibsonconnor@gmail.com
- **LinkedIn**: [Connect with me on LinkedIn](https://www.linkedin.com/in/connor-jibson/)

Thank you for visiting my project repository! I hope you find these projects informative and useful.

