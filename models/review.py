#!/usr/bin/python3
'''
    Putting the Review class into practice
'''
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    '''
        Application of the Review.
    '''
    __tablename__ = "reviews"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""
