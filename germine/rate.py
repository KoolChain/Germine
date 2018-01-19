import time

from germine.api_base import WebApi


class Rate(object):
    def __init__(self):
        self.api = WebApi("https://api.coinmarketcap.com/v1")
        self.rate_epoch = 0
        self.rate_cache = None
        self.cache_fresh_period = 120

    def _now_epoch(self):
        return int(time.time())

    def _refresh(self):
        self.rate_cache = self.api.request("/ticker?limit=500")
        self.rate_epoch = self._now_epoch()

    # USD
    def get_rate(self, currency_name):
        if (self._now_epoch() - self.rate_epoch) > self.cache_fresh_period:
            self._refresh()
        return float(
            next(
                rate["price_usd"] for rate in self.rate_cache
                if rate["name"] == currency_name
            )
        )
