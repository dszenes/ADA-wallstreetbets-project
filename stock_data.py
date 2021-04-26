import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web

%matplotlib inline


# Get data from yahoo finance
# Historical stock price 
gme = yf.download('GME','2021-01-01','2021-03-31')


# Compute Daily Volatility
# First let's compute the daily return
gme['Log_Ret'] = np.log(gme['Close'] / gme['Close'].shift(1))

# Compute Volatility using the pandas rolling standard deviation function
wtd = 5 #window of trading days
gme['Volatility'] = gme['Log_Ret'].rolling(window=wtd).std() * np.sqrt(wtd)

# Plot the Price series and the Volatility
gme[['Close', 'Volatility']].plot(title = 'GameStop', subplots=True,figsize=(8, 8))

gme
