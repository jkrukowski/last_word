import pandas as pd
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
            result.add(line.strip().decode('utf-8'))
    return result


def clean_text(text):
    for pattern, sub_text in to_replace.iteritems():
        text = pattern.sub(sub_text, text)
    return text.strip()


def lemmatize(text):
    return TextBlob(text).words.lower().lemmatize()


swords = get_stopwords()

# clean, lemmatize and remove stopwords
df['clear_stm'] = df.stm.apply(clean_text)
df.clear_stm.replace('[\w\W]+offender declined to make a last statement[\w\W]+', '', inplace=True, regex=True)
df['text_blob'] = df.clear_stm.apply(lemmatize)
df['text_blob'] = df.text_blob.apply(lambda x: [i for i in x if i not in swords])

# make and save dictionary
dictionary = corpora.Dictionary(df.text_blob)
dictionary.save('../dictionary.dict')

# add bow column
df['bow'] = df.text_blob.apply(lambda x: dictionary.doc2bow(x))
df.to_pickle('../data.pkl')
