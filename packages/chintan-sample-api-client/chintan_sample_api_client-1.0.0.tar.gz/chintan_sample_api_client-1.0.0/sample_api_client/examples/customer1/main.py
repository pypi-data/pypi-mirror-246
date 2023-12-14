import logging

from ...api.default import get_list
from ...client import Client
from ...types import Response


def client_test():
    client = Client(base_url="http://localhost")
    with client as client:
        response: Response = get_list.sync_detailed(client=client)
        logging.info("response = {}".format(response))


if __name__ == '__main__':
    client_test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
