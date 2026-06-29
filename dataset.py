from itch_parser import parse_itch_file
import pandas as pd

records = parse_itch_file('data/20190530.BX_ITCH_50.gz')
df = pd.DataFrame(records)
print(df.head())
print(df.dtypes)
print(len(df))

df.to_parquet('data/lifecycles.parquet')