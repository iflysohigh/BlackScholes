# trading_bot.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)

html_content = '''
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Black-Scholes Trading Bot</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }

        .navbar-light {
            background-color: #f8f9fa;
        }

        .settings-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            cursor: pointer;
        }

        #settings-modal {
            text-align: center;
        }

        /* Dark mode styles */
        body.dark-mode {
            background-color: #343a40;
            color: #ffffff;
        }

        .navbar-light.dark-mode {
            background-color: #343a40 !important;
        }

        .modal-content.dark-mode {
            background-color: #343a40;
            color: #ffffff;
        }

        /* Fancy styles */
        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        h1, h2 {
            color: #007bff;
        }

        form {
            border: 1px solid #dee2e6;
            padding: 20px;
            border-radius: 10px;
            background-color: #f8f9fa;
        }

        button {
            background-color: #007bff;
            color: #ffffff;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        .mt-4 {
            margin-top: 20px;
        }

        /* Settings Modal Styles */
        .modal-body {
            text-align: left;
        }

        .settings-label {
            margin-bottom: 10px;
        }

        .settings-reset {
            color: #dc3545;
            cursor: pointer;
            text-decoration: underline;
        }

        .settings-reset:hover {
            color: #bd2130;
        }
    </style>

    <style>
        /* Add these styles for dark mode button visibility */
        body.dark-mode input[type="text"],
        body.dark-mode button {
            background-color: #697480;
            color: #ffffff;
        }

        /* Additional styling for dark mode */
        body.dark-mode form {
            background-color: #343a40;
            border: 1px solid #697480;
        }

        #call_price_label,
        #put_price_label {
            font-size: 25px;
            text-decoration: underline;
        }

        #call_price,
        #put_price {
            font-size: 20px;
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Black-Scholes Bot</a>
        <span id="settings-btn" class="settings-btn" data-toggle="modal" data-target="#settings-modal">
            ⚙️
        </span>
    </nav>

    <div class="container mt-4">
        <h1 class="mb-4">Options Pricing with Black-Scholes Model</h1>
        
        <form id="optionForm">
            <div class="form-group">
                <label for="spot_price">Spot Price:</label>
                <input type="text" placeholder="42.00" class="form-control" id="spot_price" name="spot_price" required onkeydown="if(event.keyCode==13) calculateOptionPrice();">
            </div>

            <div class="form-group">
                <label for="strike_price">Strike Price:</label>
                <input type="text" placeholder="40.00" class="form-control" id="strike_price" name="strike_price" required onkeydown="if(event.keyCode==13) calculateOptionPrice();">
            </div>

            <div class="form-group">
                <label for="time_to_maturity">Time to Maturity (in years):</label>
                <input type="text" placeholder="0.5" class="form-control" id="time_to_maturity" name="time_to_maturity" required onkeydown="if(event.keyCode==13) calculateOptionPrice();">
            </div>

            <div class="form-group">
                <label for="volatility">Volatility:</label>
                <input type="text" placeholder="0.2" class="form-control" id="volatility" name="volatility" required onkeydown="if(event.keyCode==13) calculateOptionPrice();">
            </div>

            <div class="form-group">
                <label for="interest_rate">Interest Rate:</label>
                <input type="text" placeholder="0.1" class="form-control" id="interest_rate" name="interest_rate" required onkeydown="if(event.keyCode==13) calculateOptionPrice();">
            </div>

            <div class="text-center">
                <button type="button" class="btn btn-primary" onclick="calculateOptionPrice()">Calculate Option Price</button>
            </div>
        </form>

        <div class="mt-4">
            <h2 class="text-center">Option Prices</h2>
            <div class="row">
                <div class="col-md-6 text-center">
                    <p id="call_price_label">Call Price</p>
                    <p id="call_price"> </p>
                </div>
            <div class="col-md-6 text-center">
                <p id="put_price_label">Put Price</p>
                <p id="put_price"> </p>
            </div>
        </div>

    <p id="error" style="color: red;"></p>
</div>
    </div>

    <!-- Settings Modal -->
    <div class="modal fade" id="settings-modal" tabindex="-1" role="dialog" aria-labelledby="settings-modal-label" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="settings-modal-label">Settings</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="settings-label">
                        <label for="color-scheme">Color Scheme:</label>
                        <select id="color-scheme">
                            <option value="light">Light</option>
                            <option value="dark">Dark</option>
                        </select>
                    </div>

                    <div class="settings-label">
                        <span class="settings-reset" onclick="resetSettings()">Reset to Default Settings</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io.connect('http://' + document.domain + ':' + location.port);

        function calculateOptionPrice() {
            const data = {
                spot_price: $('#spot_price').val(),
                strike_price: $('#strike_price').val(),
                time_to_maturity: $('#time_to_maturity').val(),
                volatility: $('#volatility').val(),
                interest_rate: $('#interest_rate').val(),
            };

            socket.emit('calculate_option_price', data);
        }

        socket.on('option_prices', function(data) {
            if (data.error) {
                $('#error').text('Error: ' + data.error);
            } else {
                $('#call_price').text(data.call_price.toFixed(2));
                $('#put_price').text(data.put_price.toFixed(2));
                $('#error').text('');
            }
        });

        // Dark mode toggle
        $('#color-scheme').change(function() {
            const colorScheme = $(this).val();
            if (colorScheme === 'dark') {
                $('body').addClass('dark-mode');
                $('.navbar-light').addClass('dark-mode');
                $('.modal-content').addClass('dark-mode');
                // Change the color of the text to white in dark mode
                $('.navbar-brand').css('color', '#ffffff');
            } else {
                $('body').removeClass('dark-mode');
                $('.navbar-light').removeClass('dark-mode');
                $('.modal-content').removeClass('dark-mode');
                // Reset the text color to the default color in light mode
                $('.navbar-brand').css('color', ''); // Empty string resets to default color
            }
        });

        // Reset settings
        function resetSettings() {
            $('#font-size').val('normal');
            $('#color-scheme').val('light');

            $('body').removeClass('font-large font-x-large dark-mode');
            $('.navbar-light').removeClass('dark-mode');
            $('.modal-content').removeClass('dark-mode');
            $('form').removeClass('rounded rounded-pill');

            // Reset the text color to the default color
            $('.navbar-brand').css('color', ''); // Empty string resets to default color

            // Close the modal
            $('#settings-modal').modal('hide');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return html_content
    #return render_template('index.html')

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