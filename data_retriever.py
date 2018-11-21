from time import sleep, time
from json import dumps
from pathlib import Path

import requests


def get_all_currencies(url='https://poloniex.com/public?command=return24hVolume'):
    r = requests.get(url)
    data = r.json()

    return [k for k in data.keys() if 'total' not in k]


def parse_data(start=None, end=None):

    t = time()
    if end is None:
        end = int(t)

    if start is None:
        start = int(t - 300)

    pairs = get_all_currencies()

    output = dict()

    for p in pairs:

        url = f'https://poloniex.com/public?command=returnChartData' \
              f'&currencyPair={p}&start={start}&end={end}&period=300'

        r = requests.get(url)
        incoming_json = r.json()[0]

        keys = ['open', 'high', 'low', 'close']
        data = dict()

        for k in keys:
            data[k] = incoming_json[k]

        output[p] = data

        sleep(0.05)  # not to overwhelm API

    return output


if __name__ == '__main__':

    output_file = Path('output.json')

    start_time = None

    if output_file.exists():
        start_time = int(output_file.stat().st_mtime)

    d = parse_data(start=start_time)
    form = dumps(d, indent=1)

    output_file.write_text(form)
