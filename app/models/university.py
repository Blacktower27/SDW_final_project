from sqlalchemy import Integer, Float, String, Column
from app.models.base import Base, db

class University(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    universityName = Column(String(100), nullable=False, unique=True)

    def __init__(self, universityName):
        self.universityName = universityName
