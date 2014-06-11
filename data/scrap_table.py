from datetime import datetime
from itertools import izip
import pickle
from bs4 import BeautifulSoup

BASE_URL = r'http://www.tdcj.state.tx.us/death_row/'
HREFS_URL = r'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'
DATE_FORMAT = '%m/%d/%Y'
FILE_PATHS = ('../fetched_data/dr_info.html', '../fetched_data/dr_info2.html')

parse_map = {
    'lp': lambda x: int(x.get_text()),
    'info_link': lambda x: BASE_URL + x.find('a')['href'].strip(),
    'stm_link': lambda x: BASE_URL + x.find('a')['href'].strip(),
    'surename': lambda x: x.get_text().strip(),
    'name': lambda x: x.get_text().strip(),
    'no': lambda x: int(x.get_text()),
    'age': lambda x: int(x.get_text()),
    'date': lambda x: datetime.strptime(x.get_text(), DATE_FORMAT),
    'race': lambda x: x.get_text().strip(),
    'county': lambda x: x.get_text().strip()
}

parse_keys = ('lp',
              'info_link',
              'stm_link',
              'surename',
              'name',
              'no',
              'age',
              'date',
              'race',
              'county')


def parse_statement(content):
    if content:
        return ' '.join((i.get_text() for i in content))
    return None


def get_file_content(path):
    with open(path, 'rb') as f:
        return f.read()


def parse_row_item(item):
    result = {}
    for i in izip(parse_keys, item):
        key, val = i
        fn = parse_map[key]
        result[key] = fn(val)
    return result


def get_rows():
    result = []
    for path in FILE_PATHS:
        soup = BeautifulSoup(open(path))
        table = soup.find('table')
        to_iterate = table.find_all('tr')
        for item in to_iterate:
            to_parse = (td_item for td_item in item.find_all('td'))
            result.append(parse_row_item(to_parse))
    return result

if __name__ == '__main__':
    pickle.dump(get_rows(), open('../fetched_data/table.pkl', 'wb'))
