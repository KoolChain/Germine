from germine.models import Algorithm, Base, Currency, Pool, PoolAddress, PoolApi, Wallet


def populate(session):
    algos = {
        "cn": Algorithm(name="CrytpoNight"),
        "eh": Algorithm(name="Equihash"),
    }

    curr = {
        "HUSH":
            Currency(name="Hush", symbol="HUSH", algorithm=algos["eh"]),
        "XMR":
            Currency(name="Monero", symbol="XMR", algorithm=algos["cn"]),
        "ETN":
            Currency(name="Electroneum", symbol="ETN", algorithm=algos["cn"]),
    }

    pools = {
        "supportxmr":
            Pool(
                name="supportXMR",
                currency=curr["XMR"],
                base_url="https://supportxmr.com/",
                addresses=[
                    PoolAddress(origin="fr01.supportxmr.com", port=7777)
                ],
                wallet_stat_url="https://supportxmr.com/#/dashboard",
                api=PoolApi(name="Cryptonote-Pool", classname="CryptonoteApi"),
                api_base_url="https://supportxmr.com/api/",
            )
    }

    alls = [
        algos,
        curr,
        pools,
    ]

    session.add_all([value for mapping in alls for value in mapping.values()])
    session.commit()
