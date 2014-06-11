import pandas as pd
import pickle

DATA_PATH = '../fetched_data/full_table.pkl'
data = pickle.load(open(DATA_PATH))
df = pd.DataFrame(data)
df['age'].hist()
df['race'].value_counts().plot(kind='bar')
df['county'].value_counts().plot(kind='bar')