#!/usr/bin/env python3
"""SQLAlchemy model named User for a database table named users"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """class User a prototype of the users table"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    reset_token = Column(String, nullable=False)
