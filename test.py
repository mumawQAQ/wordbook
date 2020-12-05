import pandas as pd

df = pd.read_csv("./resource/3000_back1.csv", index_col=0)
df['last_attempt_date'] = 0

df.to_csv('./resource/3000.csv')