from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.sqltypes import DATE, Float
from app.models.base import Base,db
from app.models.offer import Offer

class Offer_com(Offer):

    __tablename__ = 'offer_com'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    companyName = Column(String(50), nullable=False)
    employmentExperience = Column(String(1024))
    __mapper_args__ = {
        'polymorphic_identity': 'offer_com',
        'concrete': True
    }

    def __init__(self, date,gpa,photoCopy,title, companyName,employmentExperience):
        super().__init__(date,gpa,photoCopy)
        self.title = title
        self.companyName = companyName
        self.employmentExperience  = employmentExperience