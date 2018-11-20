from time import sleep
from json import dumps

import requests
import maya


def get_all_currencies(url='https://poloniex.com/public?command=return24hVolume'):
    r = requests.get(url)
    data = r.json()

    return [k for k in data.keys() if 'total' not in k]


def main():
    pairs = get_all_currencies()

    n = maya.now()
    start = n.subtract(minutes=5).epoch
    end = n.epoch

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
    d = main()

    with open('output.json', 'w') as f:
        form = dumps(d, indent=1)
        f.write(form)
