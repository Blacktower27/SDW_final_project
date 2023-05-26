from sqlalchemy import Integer, Float, String, Column
from app.models.base import Base, db
from app.models.program import Program
from app.models.alumni import Alumni

class Knowledge_point(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    courseNameList = Column(String(1024), nullable=False)
    #添项目的外键
    program_id = Column(Integer, db.ForeignKey(Program.id, ondelete='CASCADE'))
    program = db.relationship("Program", backref="knowledge_points_program")

    alumni_id = Column(Integer, db.ForeignKey(Alumni.id, ondelete='CASCADE'))
    alumni = db.relationship("Alumni", backref="knowledge_points_alumni")

    def __init__(self, courseNameList):
        self.courseNameList = courseNameList

    def update(self, courseNameList):
        self.courseNameList = courseNameList