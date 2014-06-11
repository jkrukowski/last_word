import pickle
import requests
import urlparse
import os

BASE_URL = r'http://www.tdcj.state.tx.us/death_row/'


def save_file(url, fname):
    with open(fname, 'wb') as f:
        response = requests.get(url, stream=True)
        if not response.ok:
            print 'error for', url
        for block in response.iter_content(1024):
            if not block:
                break
            f.write(block)


def get_extension(url):
    path = urlparse.urlparse(url).path
    return os.path.splitext(path)[1]


def fetch_info(data):
    for item in data:
        fname = '../fetched_info/' + str(item['no']) + get_extension(item['info_link'])
        save_file(item['info_link'], fname)
        print 'fetched', item['info_link']


if __name__ == '__main__':
    data = pickle.load(open('../fetched_data/full_table.pkl'))
    fetch_info(data)
