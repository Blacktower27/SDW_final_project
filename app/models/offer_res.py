from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.sqltypes import DATE, Float
from app.models.base import Base,db
from app.models.offer import Offer
from app.models.program import Program
from app.models.offer_tac import Offer_tac

class Offer_res(Offer_tac):

    __tablename__ = 'offer_res'
    id = Column(Integer, db.ForeignKey('offer_tac.id'), primary_key=True)
    name = Column(String(20))
    reseachtopic= Column(String(100))
    Nopaper= Column(Integer)
    Noreach= Column(Integer)
    __mapper_args__ = {
        'polymorphic_identity': 'offer_res'
    }

    def __init__(self, date,gpa,photoCopy, supervisor, name, reseachtopic, Nopaper, Noreach):
        super().__init__(date,gpa,photoCopy)
        self.supervisor=supervisor
        self.name=name
        self.reseachtopic = reseachtopic
        self.Nopaper=Nopaper
        self.Noreach=Noreach

