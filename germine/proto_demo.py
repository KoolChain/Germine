#!/usr/bin/env python

import sqlalchemy
from models import Algorithm, Base, Currency, Wallet

if __name__ == "__main__":
    engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)

    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker(bind=engine)

    algo = Algorithm(name="crytponight")
    session = Session()
    session.add(algo)
    session.commit()
