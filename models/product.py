from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

from utils.database import Base


class Product(Base):
    __tablename__ = 'products'

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=True)
    image_path = Column(String(255), nullable=True)
    quantity = Column(mutable_json_type(dbtype=JSONB, nested=True), nullable=False, default={}, server_default='{}')
    article = Column(String(255), nullable=True)
    code = Column(String(255), nullable=True)
    unit = Column(String(55), nullable=True)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
