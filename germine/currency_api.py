from germine.api_base import WebApi


# Following insigh API see: https://github.com/bitpay/insight-api
class InsightApi(WebApi):
    def get_balance(self, wallet):
        json = self.request("/addr/{}?noTxList=1".format(wallet.public_identifier))
        return {
            "balance": json["balance"],
            "unconfirmed": json["unconfirmedBalance"]
        }
