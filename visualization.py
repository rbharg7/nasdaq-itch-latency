import numpy as np
import matplotlib.pyplot as plt


import pandas as pd

df = pd.read_parquet('data/lifecycles.parquet')

executed = df[df['exit_type'].isin(['E', 'C'])].copy()
buy_orders = executed[executed['side'].isin(['B'])]
sell_orders = executed[executed['side'].isin(['S'])]

percentiles = np.linspace(0, 99.9, 1000)

values = np.percentile(executed['time_on_book_ns'] / 1000, percentiles)
buy_values = np.percentile(buy_orders['time_on_book_ns'] / 1000, percentiles)
sell_values = np.percentile(sell_orders['time_on_book_ns'] / 1000, percentiles)

base_date = pd.Timestamp('2019-05-30')
executed['add_time'] = base_date + pd.to_timedelta(executed['add_ns'], unit='ns')
market_hours = executed[(executed['add_ns'] >= 48600e9) & (executed['add_ns'] <= 72000e9)].copy()
market_hours = market_hours.set_index('add_time')
intraday = market_hours['time_on_book_ns'].resample('1min').quantile(0.99) / 1000

# executed = executed.set_index('add_time')



def plot_cdf(executed, buy_orders, sell_orders):

    plt.yscale('log')
    plt.xlabel('Percentile')
    plt.ylabel('Time on book (μs)')
    plt.title('Order fill latency CDF — NASDAQ BX 2019-05-30')
    plt.plot(percentiles, buy_values, label='Buy')
    plt.plot(percentiles, sell_values, label='Sell')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_intraday(intraday):
    plt.plot(intraday)
    plt.yscale('log')
    plt.xlabel('time of day')
    plt.ylabel('Time on book (μs)')
    plt.title('Order fill latency intraday— NASDAQ BX 2019-05-30')
    plt.grid(True, alpha=0.3)
    plt.show()
   

plot_cdf(executed, buy_orders, sell_orders)
plot_intraday(intraday)