from sqlalchemy import Column, String

from utils.database import Base


class Slide(Base):
    __tablename__ = 'slides'

    title = Column(String(255), nullable=False)
    image_path = Column(String(255), nullable=False)
