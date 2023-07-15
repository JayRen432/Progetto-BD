import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Iscritto(Base):
    __tablename__ = 'iscritto'
    
    # attributes
    codAppello = Column(String, ForeignKey('appelli.codAppello'), primary_key = True)
    codFiscale = Column(String, ForeignKey('studenti.codFiscale'), primary_key = True)
    
    # relationships
    studente = relationship("Studente", back_populates="iscritti")
    appello = relationship("Appello", back_populates="iscritti")

    def __init__(self, ca, cf):
        self.codAppello = ca
        self.codFiscale = cf
    
    def __repr__(self):
        return "< (codAppello='%s' codFiscale='%s')>" % (self.codAppello, self.codFiscale)
