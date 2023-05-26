from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.sqltypes import DATE, Float, LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB
from app.models.base import Base

class Offer(Base):
    __tablename__ = 'offers'
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DATE)
    gpa = Column(Float)
    photoCopy = Column(LargeBinary(length=(2**32)-1))
    __mapper_args__ = {
        'polymorphic_identity': 'offer'
    }

    def __init__(self, date, gpa, photoCopy):
        self.date = date
        self.gpa = gpa
        self.photoCopy=photoCopy
