from datetime import datetime, timedelta
import entsoe
import pandas as pd
import demo_src.config as config

API_KEY = config.api_key
CLIENT = entsoe.EntsoePandasClient(API_KEY)

def _get_todays_prices():
    today = datetime.now()
    tmrrw = today + timedelta(days=1)

    today = today.strftime("%Y%m%d")
    tmrrw = tmrrw.strftime("%Y%m%d")

    start = pd.Timestamp(today, tz='Europe/Helsinki')
    end = pd.Timestamp(tmrrw, tz='Europe/Helsinki')
    country_code = "FI"

    prices = CLIENT.query_day_ahead_prices(country_code, start, end)
    return prices.to_dict()

def _write(prices:dict):
    with open("demo_src/todays_prices.csv", "w") as file:
        for timestamp, price in prices.items():
            timestamp = str(timestamp).split("+")[0] # Get rid of time zone offset
            row = f"{timestamp};{price}"
            file.write(row + "\n")

def _read():
    data = {}
    with open("demo_src/todays_prices.csv", "r") as file:
        for row in file:
            timestamp, price = row.replace("\n", "").split(";")
            data[timestamp] = price
    return data

def get_price_now(current_time:datetime):
    date = current_time.strftime("%Y-%m-%d")

    check = date + " 00:15:00"
    data = _read()

    if check not in data:
        # Data file contains old data
        todays_prices = _get_todays_prices()
        _write(todays_prices)
        data = _read()

    quart_intervals = ["00", "15", "30", "45"]
    last_quart = "00"
    for interval in quart_intervals:
        if int(interval) <= int(current_time.minute):
            last_quart = interval

    hour = current_time.hour
    hour = str(hour) if hour > 9 else "0" + str(hour)
    fetchtime = f"{date} {hour}:{last_quart}:00"
    current_price = float(data[fetchtime])

    return current_price
