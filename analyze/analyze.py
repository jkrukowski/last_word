import pandas as pd
import numpy as np
import pickle
import re
from textblob import TextBlob
from gensim import corpora, models, similarities

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


def get_stopwords():
    result = set()
    with open('../stopwords.txt', 'rb') as f:
        for line in f:
            result.add(line.strip())
    return result


def clean_text(text):
    for pattern, sub_text in to_replace.iteritems():
        text = pattern.sub(sub_text, text)
    return text.strip()


def lemmatize(text):
    return TextBlob(text).words.lower().lemmatize()


# clean and lemmatize
df['clear_stm'] = df.stm.apply(clean_text)
df.clear_stm.replace('[\w\W]+offender declined to make a last statement[\w\W]+', '', inplace=True, regex=True)
df['text_blob'] = df.clear_stm.apply(lemmatize)

# make and save dictionary
dictionary = corpora.Dictionary(df.text_blob)
dictionary.save('../dictionary.dict')

# add bow column
df['bow'] = df.text_blob.apply(lambda x: dictionary.doc2bow(x))
df.to_pickle('../data.pkl')
