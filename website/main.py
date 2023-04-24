from flask import Flask, render_template, request, redirect
from apscheduler.schedulers.background import BackgroundScheduler
import yfinance as yf
from flask_mail import Mail, Message
import smtplib
import time

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abc@gmail.com'
app.config['MAIL_PASSWORD'] = 'email_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

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

    # wait for the specified frequency before checking stock price again
    time.sleep(frequency * 3600)

    # Check if the threshold has been met
    if data['Close'][0] >= threshold:
        # Send the notification
        if notification == 'email':

            #  send email notification
            msg = Message('Stock Alert', sender = 'abc@gmail.com', recipients = [email])
            msg.body = f'The stock price of {ticker} has reached the threshold of {threshold}. The current price is {data["Close"][0]}.'
            mail.send(msg)
        elif notification == 'sms':

            # send SMS notification using SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('abc@gmail.com', 'email_password')
            message = f'The stock price of {ticker} has reached the threshold of {threshold}. The current price is {data["Close"][0]}.'
            server.sendmail('abc@gmail.com', f'{phone_number}@sms_gateway_domain.com', message)
            server.quit()

    # Redirect to the home page
    return redirect('/')

scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

if __name__ =='__main__':
    app.run(debug=True)
