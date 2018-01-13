from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def _class_name(self):
        return self.__class__.__name__


Base = declarative_base(cls=Base)


class IdMixin(object):
    id = Column(Integer, primary_key=True)


# So paradoxxxzero can choose the right type
Url = String
UrlPattern = String


class Algorithm(Base, IdMixin):
    name = Column(String)
    currencies = relationship("Currency", back_populates="algorithm")

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<{}({})>".format(self._class_name(), self.name)


class Currency(Base, IdMixin):
    name = Column(String, unique=True)
    symbol = Column(String, unique=True)

    algorithm_id = Column(Integer, ForeignKey('algorithm.id'))
    algorithm = relationship("Algorithm", back_populates="currencies")

    def __repr__(self):
        return "<{}({})>".format(self._class_name(), self.name)


class PoolAddress(Base, IdMixin):
    origin = Column(String)
    port = Column(Integer)
    note = Column(Text)
    
    pool_id = Column(Integer, ForeignKey('pool.id'))
    pool = relationship("Pool", back_populates="addresses")


class PoolApi(Base, IdMixin):
    name = Column(String, unique=True)
    classname = Column(String)
    pool = relationship("Pool", back_populates="api")

    def __str__(self):
        return self.name


class Pool(Base, IdMixin):
    name = Column(String, name=True)
    base_url = Column(Url)
    wallet_stat_url = Column(UrlPattern)

    api_base_url = Column(Url)

    api_id = Column(Integer, ForeignKey('poolapi.id'))
    api = relationship("PoolApi")

    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency")

    addresses = relationship("PoolAddress", back_populates="pool")

    def __str__(self):
        return self.name


class Wallet(Base, IdMixin):
    name = Column(String, unique=True)

    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency")

    public_identifier = Column(String)

    def __str__(self):
        return self.name


#https://github.com/bitpay/insight-api
#https://explorer.myhush.org/api/addr/t1LJWMM4pJ8L8RgWRmo2zF7HgU4CRfjWWkT

# support XMR
# https://cryptonote-pool-api.restlet.io/#general_information
