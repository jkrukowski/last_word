import os
from collections import namedtuple
from gensim import corpora, models, similarities
from textblob import TextBlob
from flask import Flask, request, g, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)
Data = namedtuple('Data', 'matrix model dictionary')

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='\xbe\xf5`\xd7\xb0\xab\x93K;<\xccW\xb7q+\xbd\x1f\xfb\xd7\x95\x8e\xcb\x1e\xb3',
    USERNAME='admin',
    PASSWORD='default',
    MATRIX=os.path.join(app.root_path, 'data/lsi.matrix'),
    MODEL=os.path.join(app.root_path, 'data/lsi.model'),
    DICTIONARY=os.path.join(app.root_path, 'data/dictionary.dict')
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def load_data():
    dictionary = corpora.Dictionary.load(app.config['DICTIONARY'])
    matrix = similarities.MatrixSimilarity.load(app.config['MATRIX'])
    model = models.LsiModel.load(app.config['MODEL'])
    return Data(matrix=matrix, model=model, dictionary=dictionary)


def get_data():
    if not hasattr(g, 'data'):
        g.data = load_data()
    return g.data


def parse_input(input_data, dictionary, model):
    vec_text = TextBlob(input_data).words.lower().lemmatize()
    vec_bow = dictionary.doc2bow(vec_text)
    return model[vec_bow]


def get_similar(vec_model, matrix):
    sims = matrix[vec_model]
    result = [[index, float(item)] for index, item in enumerate(sims)]
    return sorted(result, key=lambda x: -x[1])


@app.route('/query')
def user_query():
    data = get_data()
    user_input = request.args.get('q')
    vec_parsed = parse_input(user_input, data.dictionary, data.model)
    result = get_similar(vec_parsed, data.matrix)
    flash('successful query')
    return jsonify({'status': 0, 'result': result})


if __name__ == '__main__':
    app.run()
