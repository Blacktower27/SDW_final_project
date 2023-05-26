from sqlalchemy import Integer, Float, String, Column,Boolean
from app.models.base import Base, db
from app.models.uicer import Uicer

class Alumni(Uicer):
    id = Column(Integer, db.ForeignKey('uicer.id'), primary_key=True)
    status = Column(String(20))
    anonymousName = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'alumni',
    }

    def __init__(self, name, email, password, gender, gpa, status, anonymousName):
        super().__init__(name, email, password, gender, gpa)
        self.status = status
        self.anonymousName = anonymousName

    def update(self, name=None, gender=None, gpa=None, status=None, anonymousName=None):
        if name:
            self.name = name
        if gender:
            self.gender= gender
        if gpa:
            self.gpa = gpa
        if status:
            self.status=status
        if anonymousName:
            self.anonymousName = anonymousName

    def grade(self):
        letter=self.email[0]
        print(letter)
        return 2020+ord(letter)-ord('q')