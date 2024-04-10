import requests
import json
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify,Response
import threading
import time
import os

app = Flask(__name__)

def get_stock_price(symbol, index, language):
    target_url = f"https://www.google.com/finance/quote/{symbol}:{index}?hl={language}"
    while True:
        try:
            # Make an HTTP request
            page = requests.get(target_url)
            page.raise_for_status()  # Raise an exception for HTTP errors
            soup = BeautifulSoup(page.content, "html.parser")

            # Find the element containing the stock price
            price_element = soup.find("div", {"class": "YMlKec fxKbKc"})
            if price_element:
                stock_price = price_element.text
                yield stock_price
            else:
                yield "Stock price not found or website structure has changed."
        except requests.RequestException as e:
            yield f"Error fetching stock price: {str(e)}"

        # Wait before fetching again
        time.sleep(1)  # Wait for 1 second before checking for an update

@app.route('/<symbol>', methods=['GET'])
def stock_price(symbol):
    index = request.args.get('index', 'NSE')
    language = request.args.get('language', 'en')
    price = next(get_stock_price(symbol, index, language))
    response_data = {'symbol': symbol, 'price': price}
    json_response = json.dumps(response_data, ensure_ascii=False)
    return Response(json_response, content_type='application/json; charset=utf-8')


if __name__ == '__main__':
    prt = int(os.environ.get('PORT', 3000))
    app.run(debug=True, host='0.0.0.0',  port=prt)
