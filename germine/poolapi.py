import requests


class PoolApi(object):
    def __init__(self, url_base):
        self.url_base = url_base

    def _endpoint(self, path):
        return self.url_base + path

    def request(self, path):
        response = requests.get(self._endpoint(path))
        if response.status_code != 200:
            raise Exception(
                "Failed to talk to endpoint: {}".format(_endpoint(path))
            )
        return response.json()


class CryptonoteApi(PoolApi):
    def get_balance(self, wallet):
        json = self.request("/miner/{}/stats".format(wallet.public_identifier))
        return {
            "due": json["amtDue"],
            #"paid": json["totalPaid"],
        }
