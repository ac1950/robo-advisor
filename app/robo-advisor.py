# app/robo_advisor.py

import json
import csv
import os

import requests
import datetime


from dotenv import load_dotenv
load_dotenv() # loads contents of .env file into the scripts environment

## converts a float to a string in USD
def to_usd(my_price):
    return f"${my_price:,.2f}" 
    ## Taken from shopping-cart project
    ##Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency

#
# INFO INPUTS
#

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

formating = True
while formating == True:
    input0 = input("Please Input a Stock Ticker (e.g. XOM): ")
    ticker = input0.upper()
    if len(ticker) > 5: 
        print("Oops! Expecting a Properly Formatted Stock Ticker")
        formating = True
    elif ticker.isalpha() == False:
        print("Oops! Expecting a Properly Formatted Stock Ticker")
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






last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys()) # sort

latest_day = dates[0] #assuming that the latest day is on top

lastest_close = tsd[latest_day]["4. close"]


### CHECK DAYS GONE THROUGH THE LOOP IE HOW MANY TIMES
#get high price and low price from each day
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))

#max of all the high prices over the last 100 days
recent_high = max(high_prices)

#min of all the low prices over the last 100 days
recent_low = min(low_prices)
 

# 
# INFO OUTPUTS
#

##WRITING TO CSV
#csv_file_path = "data/prices.csv" # a relative filepath
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open","high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above
    for date in dates:
        daily_prices = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"],

        })
     

#print  time and date
now = datetime.datetime.now()
time = now.strftime("%H:%M:%p")
day = datetime.date.today()

print("-------------------------")
print(f"SELECTED SYMBOL: {ticker}")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {day} {time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(lastest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


