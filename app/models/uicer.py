from sqlalchemy import Integer, Float, String, Column
from app.models.base import Base, db

class Uicer(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    gpa = Column(Float)
    gender = Column(String(10), default='helicopter')
    def __init__(self, name, email, password, gpa, gender):
        self.name =name
        self.email = email
        self.password = password
        self.gpa = gpa
        self.gender = gender

    def check_password(self, password):
        if password==self.password:
            return True
        else:
            return False

    def change_password(self, password):
        self.password=password

    def grade(self):
        letter = self.email[0].lower()
        year = 2020+(ord(letter)-ord('q'))
        return year
