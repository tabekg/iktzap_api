from sqlalchemy import Column, Integer, ForeignKey, Text, String

from utils.database import Base


class Category(Base):
    __tablename__ = 'categories'

    title = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    image_path = Column(String(255), nullable=True)
