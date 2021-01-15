import os

# Alpaca
import alpaca_trade_api as tradeapi

# Tulip indicators
import tulipy as ti

# email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Ensenada
from psar_ops import detect_sell_sar, detect_buy_sar
import alpaca.constants as constants

class Trade:

    # TODO Pass in initialized API object so this init logic isn't executed every period
    def evaluate_and_execute_trade(self):
        # Initialize Alpaca API
        os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"
        # Insert API Credentials
        api = tradeapi.REST(constants.ALPACA_KEY, constants.ALPACA_SECRET_KEY, api_version='v2')
        account = api.get_account()

        # The mail addresses and password
        sender_address = constants.SENDER_EMAIL_ADDRESS
        sender_pass = constants.SENDER_EMAIL_PASSWORD
        receiver_address = constants.RECEIVING_EMAIL_ADDRESS
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = 'Ensenada'
        message['To'] = receiver_address
        message['Subject'] = 'Order activity'  # The subject line

        # Selection of stocks
        minutes = 1000
        stock = 'TSLA'
        barset = api.get_barset(stock, 'minute', limit=minutes)
        stock_bars = barset[stock]

        # Calculate PSAR
        acc_step = .02
        acc_max = .2
        price_open = stock_bars.df['open'].to_numpy()
        price_close = stock_bars.df['close'].to_numpy()
        price_high = stock_bars.df['high'].to_numpy()
        price_low = stock_bars.df['low'].to_numpy()
        psar = ti.psar(high=price_high, low=price_low, acceleration_factor_step=acc_step,
                       acceleration_factor_maximum=acc_max)

        # Trading_algo
        portfolio = api.list_positions()
        holding = any(x.symbol == stock for x in portfolio)
        clock = api.get_clock()

        # If markets are open
        mail_content = ""
        if clock.is_open == True:
            #If not holding
            if holding == False:
                # Detect should buy
                if detect_buy_sar.detect_buy_sar(psar[len(psar) - 1], price_close[price_close.size-1]):
                    # buy 1 share
                    api.submit_order(symbol=stock, qty=1, side='buy', type='market', time_in_force='day')
                    buy_action_message = "Ordered buy of " + stock + " at " + str(price_close[price_close.size-1])
                    print(buy_action_message)
                    mail_content = buy_action_message
            # Else holding
            else:
                # Detect should sell
                if detect_sell_sar.detect_sell_sar(psar[len(psar) - 1], price_close[price_close.size-1]):
                    # sell 1 share
                    api.submit_order(symbol=stock, qty=1, side='sell', type='market', time_in_force='day')
                    sell_action_message = "Sell has been ordered for" + stock + " with most recent close price " + str(price_close[price_close.size-1])
                    print(sell_action_message)
                    mail_content = sell_action_message
        else:
            print("The Market is Closed")
            mail_content = "The Market is Closed"

        # Only send mail if an action was taken
        if mail_content:
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content))
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()

