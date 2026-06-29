import pandas as pd

df = pd.read_parquet('data/lifecycles.parquet')

executed  = df[df['exit_type'].isin(['E', 'C'])]

buy_orders = executed[executed['side'].isin(['B'])]
sell_orders = executed[executed['side'].isin(['S'])]



def latency_stats(df):

    stats = {}

    
    stats['p50'] = df['time_on_book_ns'].quantile(0.5) / 1000
    stats['p90'] = df['time_on_book_ns'].quantile(0.9) / 1000
    stats['p95'] = df['time_on_book_ns'].quantile(0.95) / 1000
    stats['p99'] = df['time_on_book_ns'].quantile(0.99) / 1000
    stats['p99_9'] = df['time_on_book_ns'].quantile(0.999) / 1000
    stats['max'] = df['time_on_book_ns'].max() / 1000

    return stats

def latency_by_side(buy, sell):


    buy_latency = latency_stats(buy)
    sell_latency = latency_stats(sell)

    stats = {'buy': buy_latency, 'sell': sell_latency}

    return stats




print(latency_stats(executed))
print(latency_by_side(buy_orders, sell_orders))