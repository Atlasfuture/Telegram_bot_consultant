from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text)
    prices = Column(Integer)
    firmware_support = Column(Integer)
    service = Column(Integer)
    security = Column(Integer)

    def __repr__(self):
        return "<Brand(id='{}', name='{}')>".format(self.id, self.name)


class Smartphone(Base):
    __tablename__ = 'smartphone'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(Text)
    os = Column(Enum('Android', 'iOS'))
    price = Column(Float)


    """device parameters rating points"""
    photo = Column(Integer)
    video = Column(Integer)
    battery = Column(Integer)
    performance = Column(Integer)
    screen = Column(Integer)

    brand_id = Column(Integer, ForeignKey('brand.id'))


    def __repr__(self):
        return self.name


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    tele_id = Column(Integer)
    text_corpus = Column(String(200))



class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    smartphone_id = Column(Integer, ForeignKey('smartphone.id'))


if __name__ == '__main__':
    from orm.orm_engine import engine

    Base.metadata.create_all(engine)
