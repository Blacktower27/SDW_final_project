from sqlalchemy import Column, String, Integer, orm
from sqlalchemy.sql.sqltypes import DATE, Float
from app.models.base import Base,db
from app.models.offer import Offer
from app.models.program import Program

class Offer_tac(Offer):

    __tablename__ = 'offer_tac'
    id = Column(Integer, primary_key=True, autoincrement=True)

    program_id = Column(Integer, db.ForeignKey(Program.id, ondelete='CASCADE'))
    program = db.relationship("Program", backref="offer_tac")

    __mapper_args__ = {
        'polymorphic_identity': 'offer_tac',
        'concrete' : True
    }

    def __init__(self, date,gpa,photoCopy):
        super().__init__(date,gpa,photoCopy)

