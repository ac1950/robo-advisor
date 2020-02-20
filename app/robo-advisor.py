# app/robo_advisor.py


import requests
import json
import datetime


def to_usd(my_price):
    return f"${my_price:,.2f}" 
    ## Taken from shopping-cart project
    ##Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency

#
# INFO INPUTS
#
request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)


parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

lastest_close = parsed_response["Time Series (Daily)"]["2020-02-19"]["4. close"]


# 
# INFO OUTPUTS
#


#print  time and date
now = datetime.datetime.now()
time = now.strftime("%H:%M:%p")
day = datetime.date.today()

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {day} {time}")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(lastest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")