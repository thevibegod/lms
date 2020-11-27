import pandas as pd

df = pd.read_csv('dataset.csv', header=None)
ds = df.sample(frac=1)
ds.to_csv('shuffled_dataset.csv')
print('Shuffled Dataset Generated')