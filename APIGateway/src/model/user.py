from sqlalchemy import Column, ForeignKey, Integer, String
from src.data.init import Base
from sqlalchemy.orm import relationship
from src.model.rider import Rider

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(int(10), index=True)
    password = Column(String, index=True)
    email = Column(String, index=True)
    rider_id = Column(Integer, ForeignKey('rider.id'))
    rider = relationship(Rider)