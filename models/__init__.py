from sqlalchemy import event as sa_event, func, Column, String, Text, DateTime

# DO NOT REMOVE THIS UNUSED IMPORT
from utils.database import Base

from . import user, category, product, news, slide


@sa_event.listens_for(user.User, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()


@sa_event.listens_for(category.Category, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()


@sa_event.listens_for(product.Product, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()


@sa_event.listens_for(news.News, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()


class Bi(Base):
    __tablename__ = 'bi'

    name = Column(String(55), nullable=False)
    value = Column(Text, nullable=False)
    expired_at = Column(DateTime, default=None)


@sa_event.listens_for(Bi, 'before_update')
def update_version(mapper, connection, target):
    target.updated_at = func.now()
