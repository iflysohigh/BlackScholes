# trading_bot.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('calculate_option_price')
def calculate_option_price(data):
    try:
        # Extract parameters from the front-end
        spot_price = float(data['spot_price'])
        strike_price = float(data['strike_price'])
        time_to_maturity = float(data['time_to_maturity'])
        volatility = float(data['volatility'])
        interest_rate = float(data['interest_rate'])
        
        # Calculate Black-Scholes option price
        d1 = (np.log(spot_price / strike_price) + (interest_rate + (volatility**2) / 2) * time_to_maturity) / (volatility * np.sqrt(time_to_maturity))
        d2 = d1 - volatility * np.sqrt(time_to_maturity)
        
        call_price = spot_price * norm.cdf(d1) - strike_price * np.exp(-interest_rate * time_to_maturity) * norm.cdf(d2)
        put_price = strike_price * np.exp(-interest_rate * time_to_maturity) * norm.cdf(-d2) - spot_price * norm.cdf(-d1)
        
        # Send the calculated option prices to the front-end
        socketio.emit('option_prices', {'call_price': round(call_price, 3), 'put_price': round(put_price, 3)})
    except Exception as e:
        print(f"Error: {e}")
        socketio.emit('option_prices', {'error': str(e)})

if __name__ == '__main__':
    from scipy.stats import norm
    socketio.run(app, debug=True)
