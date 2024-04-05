from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship

from utils.database import Base


class Category(Base):
    __tablename__ = 'categories'

    title = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    image_path = Column(String(255), nullable=True)

    parent = relationship('Category', foreign_keys=[parent_id], back_populates='children')
    children = relationship(back_populates="parent")
