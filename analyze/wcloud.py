import wordcloud
from gensim import corpora


def make_words(dictionary):
    result = []
    for word, token_id in dictionary.token2id.iteritems():
        result.append((word, dictionary.dfs[token_id]))
    return result

wordcloud.FONT_PATH = 'C:/Windows/Fonts/DroidSansMono.ttf'
dictionary = corpora.Dictionary.load('../dictionary.dict')
words = make_words(dictionary)
elements = wordcloud.fit_words(words, width=500, height=500)
wordcloud.draw(elements, '../word_cloud.png', width=500, height=500, scale=2)
