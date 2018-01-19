from germine.api_base import WebApi


class CryptonoteApi(WebApi):
    def get_balance(self, wallet):
        json = self.request("/miner/{}/stats".format(wallet.public_identifier))
        return {
            "due": json["amtDue"],
            #"paid": json["totalPaid"],
        }
