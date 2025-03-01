"""
Bybit a python bot that works with tradingview's webhook alerts!
This bot is not affiliated with tradingview and was created by https://www.freelancer.com/u/Beannsofts

I expect to update this as much as possible to add features as they become available!
Until then, if you run into any bugs let me know!
"""
import sys
from actions import send_order, parse_webhook, parse__price_webhook
from auth import get_token
from flask import Flask, request, abort
from loguru import logger
import threading, time


# Create Flask object called app.
app = Flask(__name__)
api_key=''
api_secret=''
is_test='test'


# Create root to easily let us know its on/working.
@app.route('/')
def root():
    return 'Online.'

@logger.catch
@app.route('/price_webhook', methods=['POST'])
def price_webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        price_data = parse__price_webhook(request.get_data(as_text=True))
        return '', 200
    else:
        abort(400)  

        
@logger.catch
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Parse the string data from tradingview into a python dict
        
        # datas = parse_webhook(request.get_data(as_text=True))
        # print(datas)
        datas = request.get_json()
        print(datas)
        # Check that the key is correct
        print (get_token())
        if is_test == 'test':
            testApi = True
        else:
            testApi = False
        if get_token() == datas['key']:
            print(' [Alert Received] ')
            print('POST Received/Updated Data:', datas)
            send_order(datas, api_key, api_secret, testApi)
            return '', 200
        else:
            logger.error("Incoming Signal From Unauthorized User.")
            abort(403)

    else:
        abort(400)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/isalive', methods=['GET'])
def isalive():
    print('i am alive')
    return '',200
        
if __name__ == '__main__' :
    api_key =sys.argv[1]
    api_secret =sys.argv[2]
    is_test=sys.argv[3]
    print(api_key)
    print(api_secret)
    print(is_test)
    app.run( host="0.0.0.0", debug=True)

"""
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="212.49.95.112:5055")

#if __name__ == "__main__":
    #from waitress import serve
    #serve(app, host="212.49.95.112", port=80)
"""
