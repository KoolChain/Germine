from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.inspection import inspect

import bcrypt

import enum


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def _class_name(self):
        return self.__class__.__name__

    def as_dict(self):
        results = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        # We identify which relations are many_to_one, and dump the remote side (the one)
        inspector = inspect(type(self))
        for r in inspector.relationships:
            ls = list(r.remote_side)
            if ls[0].primary_key:
                name = r.class_attribute.key
                results[name] = getattr(self, name).as_dict()
        return results



Base = declarative_base(cls=Base)

# Because Alembic want named constraint or it does not apply migrations
# see: http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
# see: https://stackoverflow.com/a/46785675/1027706
convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

Base.metadata.naming_convention=convention



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

    api = relationship("CurrencyApi", back_populates="currency")

    def __repr__(self):
        return "<{}({})>".format(self._class_name(), self.name)


class CurrencyApi(Base, IdMixin):
    currency_id = Column(Integer, ForeignKey('currency.id'), unique=True)
    currency = relationship("Currency", back_populates="api")

    classname = Column(String)
    base_url = Column(Url)

    def __repr__(self):
        return "<{}({}, {})>".format(self._class_name(), self.currency, self.classname)


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

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="wallets")

    public_identifier = Column(String)

    def __str__(self):
        return self.name


class User(Base, IdMixin):
    login = Column(String, unique=True)
    password_hash = Column(String)

    wallets = relationship("Wallet", back_populates="user")

    systems = relationship("System", back_populates="owner")

    def __str__(self):
        return self.login

    def __init__(self, login, password):
        self.login = login
        self.password_hash = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

    def authenticate(self, challenged_password):
        return bcrypt.checkpw(challenged_password.encode("utf8"), self.password_hash)

    # Required by Flask-Login
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    # /Flask-Login


class OperatingSystem(Base, IdMixin):
    name = Column(String, unique=True)
    version = Column(String)

    system = relationship("System", back_populates="os")

    __table_args__ = (UniqueConstraint("name",
                                       "version",
                                       ),
                     )

    def __str__(self):
        return "{} {}".format(self.name, self.version)


class HardwareNatureEnum(enum.Enum):
    CPU = 1,
    GPU = 2,
    
    def __str__(self):
        return self.name


class MiningHardware(Base, IdMixin):
    nature = Column(Enum(HardwareNatureEnum))
    name = Column(String)

    system_id = Column(Integer, ForeignKey('system.id'))
    system = relationship("System", back_populates="mining_hardwares")

    id_on_system = Column(String)

    __table_args__ = (UniqueConstraint("system_id",
                                       "id_on_system",
                                       ),
                     )

    def __str__(self):
        return "{} {} on {}(#{})".format(self.nature,
                                         self.name,
                                         self.system.name,
                                         self.id_on_system)


class System(Base, IdMixin):
    name = Column(String, unique=True)

    os_id = Column(Integer, ForeignKey('operatingsystem.id'))
    os = relationship("OperatingSystem", back_populates="system")

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates="systems")

    mining_hardwares = relationship("MiningHardware", back_populates="system")

    def __str__(self):
        return "{}'s system '{}'".format(self.owner.login, self.name)


class MiningApp(Base, IdMixin):
    name = Column(String, unique=True)
    miners = relationship("Miner", back_populates="mining_app")
    
    def __repr__(self):
        return "<{}({})>".format(self._class_name(), self.name)


class Miner(Base, IdMixin):
    mining_app_id = Column(Integer, ForeignKey('miningapp.id'))
    mining_app = relationship("MiningApp", back_populates="miners")
    compatible_app_versions = Column(String)

    currency_id = Column(Integer, ForeignKey('currency.id'))
    currency = relationship("Currency")

    arguments_template = Column(String)

    mining_operations = relationship("MiningOperation", back_populates="miner")

    __table_args__ = (UniqueConstraint("mining_app_id",
                                       "compatible_app_versions",
                                       "currency_id",
                                       "arguments_template",
                                       ),
                     )

class MiningOperation(Base, IdMixin):
    miner_id = Column(Integer, ForeignKey('miner.id'))
    miner = relationship("Miner", back_populates="mining_operations")

    mining_hardware_id = Column(Integer, ForeignKey('mininghardware.id'))
    mining_hardware = relationship("MiningHardware")

    pool_id = Column(Integer, ForeignKey('pool.id')) 
    pool = relationship("Pool")

    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    wallet = relationship("Wallet")

    __table_args__ = (UniqueConstraint("miner_id",
                                       "mining_hardware_id",
                                       "pool_id",
                                       "wallet_id",
                                       ),
                     )


# support XMR
# https://cryptonote-pool-api.restlet.io/#general_information
