from sqlalchemy import Column, Text, String

from utils.database import Base


class News(Base):
    __tablename__ = 'news'

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    image_path = Column(String(255), nullable=True)
