from sqlalchemy import Integer, Float, String, Column
from app.models.base import Base, db
from app.models.university import University

class Program(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    programName = Column(String(50), nullable=False)
    gpaLow = Column(Float)
    gpaHigh = Column(Float)
    major = Column(String(100))
    #添加大学的外键
    university_id = Column(Integer, db.ForeignKey(University.id, ondelete='CASCADE'))
    university = db.relationship("University", backref="programs")

    def __init__(self, programName, gpaLow, gpaHigh, major):
        self.programName = programName
        self.gpaLow = gpaLow
        self.gpaHigh = gpaHigh
        self.major = major

    def update(self,programName = None, gpaLow = None, gpaHigh = None):
        if programName:
            self.programName = programName
        if gpaLow:
            self.gpaLow = gpaLow
        if gpaHigh:
            self.gpaHigh = gpaHigh