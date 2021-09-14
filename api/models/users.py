from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()
# from app import db, session, Base
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt

# class Costs(Base):
#     __tablename__ = 'costs'
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     category = db.Column(db.String(250), nullable=False)
#     amount = db.Column(db.Text(50), nullable=False)
#     description = db.Column(db.String(250), nullable=False)
#     type = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.TEXT(250), nullable=False)



class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __repr__(self):
        return "<User(name='{}', email='{}', password={}"\
            .format(self.name, self.email, self.password)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.email = kwargs.get('email')
    #     self.password = bcrypt.hash(kwargs.get('password'))
    #
    # def get_token(self, expire_time=24):
    #     expire_delta = timedelta(expire_time)
    #     token = create_access_token(
    #         identity=self.id, expires_delta=expire_delta)
    #     return token
    #
    # @classmethod
    # def authenticate(cls, email, password):
    #     user = cls.query.filter(cls.email == email).one()
    #     if not bcrypt.verify(password, user.password):
    #         raise Exception('No user with this password')
    #     return user
