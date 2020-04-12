# app/robo_advisor.py

import json
import csv
import os
import requests
import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from twilio.rest import Client



load_dotenv() # loads contents of .env file into the scripts environment
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

def to_usd(my_price):
    
    """ 
    Takes a float or int and returns a string formatted in USD  
    Paramater: the number to be converted 
    Example:
    to_usd(5.451) == "$5.45" ## has two decimal places and rounded

    """ 

    return f"${my_price:,.2f}" 
    ## Taken from shopping-cart project

def intro_message(): 
    """ Just a message to welcome """
    print("Hello Welcome to The Stock Market Robo-Advisor!")
    print("Remember: Bulls Make Money, Bears Make Money, Pigs Get Slaughtered")

def get_data(ticker):   
    formating = True
    while formating == True:
        if len(ticker) > 5: 
            print("Oops! Expecting a Properly Formatted Stock Ticker like 'XOM' ")
            formating = True
        elif ticker.isalpha() == False:
            print("Oops! Expecting a Properly Formatted Stock Ticker Such as 'XOM' ")
            formating = True
        else:
            break
    validation = True
    while validation == True:
        request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        response = requests.get(request_url)
        parsed_response = json.loads(response.text)
        if "Error Message" in response.text:
            print("Oops! Could Not Find Data For That Ticker!")
            quit()
        else:
            print("Getting Stock Data...")
            validation = False
    return parsed_response

def readable_response(parsed_response):
    tsd = parsed_response["Time Series (Daily)"]
    dates = []
    for date, daily_prices in tsd.items():# see: https://github.com/prof-rossetti/georgetown-opim-243-201901/blob/master/notes/python/datatypes/dictionaries.md
        date_time_series = {
            "timestamp": date,
            "open": float(daily_prices["1. open"]),
            "high": float(daily_prices["2. high"]),
            "low": float(daily_prices["3. low"]),
            "close": float(daily_prices["4. close"]),
            "volume": int(daily_prices["5. volume"])
        }
        dates.append(date_time_series)

    return dates

def get_latest_close(dates):
    latest_close = dates[0]["close"]
    return latest_close

def get_previous_close(dates): 
    previous_close = dates[1]["close"]
    return previous_close

def get_last_refreshed(parsed_response): 
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
    return last_refreshed    

def get_recent_high(dates):
    high_prices = []
    for date_time_series in dates: 
        high_price = date_time_series["high"]
        high_prices.append(float(high_price))
    
    recent_high = max(high_prices)
    return recent_high

def get_recent_low(dates):
    low_prices = []
    for date_time_series in dates: 
        low_price = date_time_series["low"]
        low_prices.append(float(low_price))

    recent_low = min(low_prices)
    return recent_low

def get_high_100(ticker, parsed_response):

    #request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    #response = requests.get(request_url)
    #parsed_response = json.loads(response.text)
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) # sort

    high_prices = []

    for date in dates:
        high_price = tsd[date]["2. high"]
        high_prices.append(float(high_price))

    #max of all the high prices over the last 100 days
    recent_high = max(high_prices)

    return recent_high

def get_low_100(ticker, parsed_response):

    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) # sort
    
    low_prices = []

    for date in dates:
        low_price = tsd[date]["3. low"]
        low_prices.append(float(low_price))
    
    #min of all the low prices over the last 100 days
    recent_low = min(low_prices)
    
    return recent_low

def to_csv(dates, csv_file_path): 
    csv_headers = ["timestamp", "open","high", "low", "close", "volume"]
    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above
        for date_time_series in dates: 
            writer.writerow(date_time_series)

def get_time(): 
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%p")
    return time

def get_day(): 
    now = datetime.datetime.now()
    day = datetime.date.today()
    return day

def get_recommendation(latest_close, previous_close): 

    if float(latest_close) / float(previous_close) > 1.03:
        recommendation = "BUY"
        reason = "Prices Have Increased 3% Since Previous Trading Day\n                       Could Be An Indication of a Bull Market\n"
    elif float(latest_close) / float(previous_close) < .97:
        recommendation = "SELL"
        reason = "Prices Have Decreased 3% Since Previous Trading Day\n                       Could Be An Indication of a Bear Market\n" 
    else: 
        recommendation = "HOLD"
        reason = "No Strong Indication of Prices Moving One Way or The Other"

        return [recommendation, reason]

def stock_output(ticker, day, time, last_refreshed, latest_close, recent_high, recent_low, recommendation, reason, csv_file_path):

    print("-------------------------")
    print(f"SELECTED SYMBOL: {ticker}")
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print(f"REQUEST AT: {day} {time}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high))}")
    print(f"RECENT LOW: {to_usd(float(recent_low))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {recommendation}!")
    print(f"RECOMMENDATION REASON: {reason}")
    print("-------------------------")
    print(f"WRITING DATA TO CSV: {csv_file_path}")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")

def send_text(latest_close, previous_close, ticker):
    if float(latest_close) / float(previous_close) > 1.04 or float(latest_close) / float(previous_close) < .96:
        TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "OOPS, please specify env var called 'TWILIO_AUTH_TOKEN'")
        TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "OOPS, please specify env var called 'TWILIO_ACCOUNT_SID'")
        SENDER_SMS  = os.environ.get("SENDER_SMS", "OOPS, please specify env var called 'SENDER_SMS'")
        RECIPIENT_SMS  = os.environ.get("RECIPIENT_SMS", "OOPS, please specify env var called 'RECIPIENT_SMS'")

        # AUTHENTICATE
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # COMPILE REQUEST PARAMETERS (PREPARE THE MESSAGE)
        content = "STOCK ALERT: " + ticker + " has moved 4% since last closing day!"

        # ISSUE REQUEST (SEND SMS)
        message = client.messages.create(to=RECIPIENT_SMS, from_=SENDER_SMS, body=content)

        print("\nALERT SENT")

def get_graph(ticker, parsed_response): 
    tsd = parsed_response["Time Series (Daily)"]
    dates = list(tsd.keys()) # sort


    print("Do You Want a Printed Graph?")
    graph_ask = input("Enter 'yes' or enter 'no': ")
    if graph_ask == 'yes' or graph_ask == 'y' or graph_ask == 'YES' or graph_ask == 'Yes':
        print("PRINT GRAPH")
        numdays1 = input("Input the number of days you want analyzed: ")

        x = []
        y = []

        numdays = int(numdays1) - 1

        numdaysint = int(numdays)
        while numdaysint >= 0:
            x.append(dates[numdaysint])


            yday = dates[numdaysint]
            y1 = tsd[yday]["4. close"]
            y2 = (float(y1))
            y.append(y2)


            numdaysint = numdaysint - 1

    

        datesgraph = x
        pricesgraph = y

        plt.xticks(fontsize=4)

    

        plt.plot(datesgraph, pricesgraph, color = 'g')

        plt.xlabel('Dates')
        plt.ylabel('Closing Price')
        plt.title(ticker + " Closing Price Over the Last " + str(numdays + 1) + " days")
        plt.show()



if __name__ == "__main__": 
    # writing CSV
    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

    #Order of Functions
    symbol = input("Please input a stock ticker (e.g. MSFT):  ") #Input Stock Ticker
    ticker = symbol.upper() #Makes sure upper case stock ticker
    parsed_response = get_data(ticker) #Returns data for stock ticker after being capitalized 
    dates = readable_response(parsed_response) # takes data from stock ticker and makes it readable

    latest_close = get_latest_close(dates) # gets latest_close price
    previous_close = get_previous_close(dates) # gets yesterday's closing price
    last_refreshed = get_last_refreshed(parsed_response) # gets date of last available stock information 

    recent_high = get_recent_high(dates) # recent high price
    recent_low = get_recent_low(dates) # get recent low price   

    high_100days = get_high_100(ticker, parsed_response) # returns high over the last 100 days
    low_100days = get_low_100(ticker, parsed_response) # returns low over the last 100 days

    day = get_day()
    time = get_time()

    recommendation = get_recommendation(latest_close, previous_close)[0]
    reason = get_recommendation(latest_close, previous_close)[1]

    to_csv(dates, csv_file_path) # write the stock data from dates to a nicely formatted .csv

    #outputs
    get_recommendation(latest_close, previous_close)
    stock_output(ticker, day, time, last_refreshed, latest_close, recent_high, recent_low, recommendation, reason, csv_file_path) # prints the main outputs for the stock
    send_text(latest_close, previous_close, ticker)
    get_graph(ticker,parsed_response)




