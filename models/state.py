#!/usr/bin/python3
'''
    Application of the State class
'''
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    '''
        Execution on behalf of the State.
        Establish connection between class State and the City.
    '''
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            '''
                Return list city instances of City.state_id==current
                State.id
                FileStorage relationsp between State and City
            '''
            list_cities = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    list_cities.append(city)
            return list_cities
