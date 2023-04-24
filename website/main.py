from website import create_app

app=create_app()

from flask import Flask, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])

def submit():
    # Get the form data
    ticker = request.form['ticker']
    threshold = float(request.form['threshold'])
    frequency = int(request.form['frequency'])
    notification = request.form['notification']
    email = request.form['email']
    phone_number = request.form['phone_number']

    # Retrieve the stock data
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d')

    # Check if the threshold has been met
    if data['Close'][0] >= threshold:
        # Send the notification
        if notification == 'email':
            # Code to send email notification
            pass
        elif notification == 'sms':
            # Code to send SMS notification
            pass

    # Redirect to the home page
    return redirect('/')

scheduler = BackgroundScheduler(daemon=True)
scheduler.start()


if __name__ =='__main__':
    app.run(debug=True)
    