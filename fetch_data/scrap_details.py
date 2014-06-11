import urllib2
import pickle
from bs4 import BeautifulSoup
import re


def get_statement(url):
    content = get_url_content(url)
    soup = BeautifulSoup(content)
    body = soup.find('div', id='body')
    lstatement = body.find('p', text=re.compile('Last Statement'))
    if lstatement:
        lstatement = lstatement.find_all_next('p')
        return lstatement


def parse_statement(value):
    return ' '.join((i.get_text() for i in value))


def get_url_content(url):
    f = urllib2.urlopen(url)
    content = f.read()
    f.close()
    return content


def get_table():
    return pickle.load(open('table.pkl'))


def parse_items():
    result = []
    table = get_table()
    for data in table:
        d = dict(data)
        stm = get_statement(data['stm_link'])
        d['stm'] = parse_statement(stm)
        result.append(d)
        print d
    return result


if __name__ == '__main__':
    items = parse_items()
    pickle.dump(items, open('../data/full_table.pkl', 'wb'))
    print '--- end'