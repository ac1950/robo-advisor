
from app.robo_advisor import to_usd, get_data, get_recent_high, get_recent_low


def test_to_usd():
    assert to_usd(10.50) == "$10.50"
    assert to_usd(10.58888) == "$10.59"

def test_get_data():
    symbol = "XOM"

    parsed_response = get_data(symbol)

    assert isinstance(parsed_response, dict)#Tests that the parsed_response is of the class "dict"
    assert "Time Series (Daily)" in parsed_response.keys()# test keys 
    assert parsed_response["Meta Data"]["2. Symbol"] == symbol#test that symbols match

def test_recent_high(): 


    dates = [
        {"timestamp": "2019-06-01", "open": "101.0924", "high": "200.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-09", "open": "102.6500", "high": "201.7000", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-07", "open": "102.4800", "high": "200.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "201.400", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-15", "open": "101.2600", "high": "200.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-12", "open": '99.2798',  "high": "202.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
        ]

    assert get_recent_high(dates) == 202.8600

    def test_recent_low():

        dates = [
        {"timestamp": "2019-06-01", "open": "101.0924", "high": "200.9500", "low": "100.5400", "close": "101.6300", "volume": "22165128"},
        {"timestamp": "2019-06-09", "open": "102.6500", "high": "201.7000", "low": "100.3800", "close": "100.8800", "volume": "28232197"},
        {"timestamp": "2019-06-07", "open": "102.4800", "high": "200.6000", "low": "101.9000", "close": "102.4900", "volume": "21122917"},
        {"timestamp": "2019-06-05", "open": "102.0000", "high": "201.400", "low": "101.5300", "close": "102.1900", "volume": "23514402"},
        {"timestamp": "2019-06-15", "open": "101.2600", "high": "200.8600", "low": "100.8510", "close": "101.6700", "volume": "27281623"},
        {"timestamp": "2019-06-12", "open": '99.2798',  "high": "202.8600", "low": "99.1700",  "close": "100.7900", "volume": "28655624"}
        ]

    assert get_recent_low(dates) == 99.1700