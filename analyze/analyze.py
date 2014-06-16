import pandas as pd
import pickle
import re
from textblob import TextBlob

DATA_PATH = '../fetched_data/full_table.pkl'
data = pickle.load(open(DATA_PATH))
df = pd.DataFrame(data)


to_replace = {
    re.compile('\([\w]+ statement\)'): '',
    re.compile('\r\n'): ' ',
    re.compile('\n'): ' ',
    re.compile('\r'): ' '
    }


def clean_text(text):
    for pattern, sub_text in to_replace.iteritems():
        text = pattern.sub(sub_text, text)
    return text.strip()

def make_blob(text):
    return TextBlob(text).words.lemmatize()

def lemmatize(text):
    pass


df['clear_stm'] = df.stm.apply(clean_text)
df['text_blob'] = df.clear_stm.apply(make_blob)

print df.clear_stm, df.text_blob


test_text = u"(Written statement) \r\n  I always said that if I even get to this point, I would have already said everything that needed to be said to all of those who I love and have been with me throughout this whole journey. Today, I realized that I can never say everything that needed to be said, because there is still so much that needs to be said. First of all, I love you. My children, my friends, and all my brothers who have shared this experience with me on the row and who continue to experience this without me, keep your heads up. I love all of you. Secondly, I am ok. I have peace in my heart and ready for the next journey. I'm really ok. Last but not least, to my true brother in life, Crazy J, I love you, man. You and Bella have been the best. I'm sorry I couldn't talk with you before all of this, but you know me...You are my bro. I love you. I'm ok. My babies, remember what I said. We'll be together soon. I love all of you. John 14:27.  (Spoken statement)\r\nYes, I left a written statement. I do \r\nhave a verbal statement. I would like to remind my children once again, I love them. Crazy J, I forgot to write a list. Everything is ok. I love you all, and I love my children. I am at peace. John 14:27. I am done, Warden. \n"
ctext = clean_text(test_text)
print ctext
