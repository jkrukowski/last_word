import pandas as pd
import pickle
import re
from textblob import TextBlob
import numpy as np

DATA_PATH = '../fetched_data/full_table.pkl'
data = pickle.load(open(DATA_PATH))
df = pd.DataFrame(data)


to_replace = {
    re.compile('\([\w]+ statement\)'): '',
    re.compile('\r\n'): ' ',
    re.compile('\n'): ' ',
    re.compile('\r'): ' ',
    re.compile('\t'): ' '
    }


def clean_text(text):
    for pattern, sub_text in to_replace.iteritems():
        text = pattern.sub(sub_text, text)
    return text.strip()

def lemmatize(text):
    if text is np.nan:
        return np.nan
    return list(TextBlob(text).words.lower().lemmatize())


df['clear_stm'] = df.stm.apply(clean_text)
df.clear_stm.replace('[\w\W]+offender declined to make a last statement[\w\W]+', np.nan, inplace=True, regex=True)
df['text_blob'] = df.clear_stm.apply(lemmatize)
df.to_pickle('../data.pkl')
