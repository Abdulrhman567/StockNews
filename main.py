import requests
from twilio.rest import Client


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = None # Get your Stock api from here https://www.alphavantage.co
NEWS_API_KEY = None # Get your News api from here https://newsapi.org
TWILIO_SID = None # Get your Twilio sid from here https://www.twilio.com
TWILIO_AUTH_TOKEN = None # Get your twilio auth token from here https://www.twilio.com

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol' : STOCK_NAME,
    'apikey': STOCK_API_KEY,
}

# Stock response and data
stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()['Time Series (Daily)']
stock_data_list = [value for (key, value) in stock_data.items()]

yesterday_stock_data = stock_data_list[0]
yesterday_closing_price = float(yesterday_stock_data['4. close'])

day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data['4. close'])

difference = yesterday_closing_price - day_before_yesterday_closing_price
up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round((difference / yesterday_closing_price) * 100)

if abs(diff_percent) > 5:
    news_parmeters = {
        'qInTitle': COMPANY_NAME,
        "apiKey": NEWS_API_KEY,
    }

    # News response and data
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parmeters)
    news_response.raise_for_status()
    articles = news_response['articles'][:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in articles]

    # send messages
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=None,# Put your twilio virtual number here
            to=None,# Put your phone number here
        )
