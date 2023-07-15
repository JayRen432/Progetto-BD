import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Appello(Base):
    __tablename__ = 'appelli'
    
    # attributes
    codAppello = Column(String, primary_key = True)
    dataAppello = Column(Date)
    
    # relationships
    iscritti = relationship("Iscritto", back_populates="appello")
    contenuti = relationship("Contenuto", back_populates="appello")

    def __init__(self, ca, date):
        self.codAppello = ca
        self.dataAppello = date
    
    def __repr__(self):
        return "<Corso(codAppello='%s' dataAppello='%s')>" % (self.codAppello, self.dataAppello)
