import logging

from api_client.sample_api_client.api.default import get_list
from api_client.sample_api_client.client import Client
from api_client.sample_api_client.types import Response


def client_test():
    client = Client(base_url="http://localhost")
    with client as client:
        response: Response = get_list.sync_detailed(client=client)
        logging.info("response = {}".format(response))


if __name__ == '__main__':
    client_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
