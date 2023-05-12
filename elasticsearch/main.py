import json
from datetime import datetime

import requests

from elasticsearch import Elasticsearch

CA_CERTS: str = r".\http_ca.crt"


def get_data(n: int) -> list:
    url: str = "https://stream.wikimedia.org/v2/stream/recentchange"

    # create client connection
    client = requests.get(url, stream=True)

    # creating empty returned list
    ret_list: list = []

    # interacting over msgs
    for ind, message in enumerate(client.iter_lines()):
        if message:
            if message.decode('utf-8').startswith('data'):
                ret_list.append(message.decode('utf-8'))
        if ind == n:
            clean_list: list = [el.replace('data: ', '') for el in ret_list]
            return [json.loads(el) for el in clean_list]


def main() -> None:

    # conneting with es cluster
    es = Elasticsearch(
        "http://localhost:9200"
    )

    # printting cluster info
    print(es.info())

    # inserting data
    for int, _document in enumerate(get_data(n=10)):
        es.index(index='wikipedia', document=_document)
    else:
        print(f'[INFO] {int+1} document indexed')


if __name__ == '__main__':

    main()
