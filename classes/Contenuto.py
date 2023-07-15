import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Contenuto(Base):
    __tablename__ = 'contenuti'
    
    # attributes
    codAppello = Column(String, ForeignKey('appelli.codAppello'), primary_key = True)
    codEsame = Column(String, ForeignKey('esami.codEsame'), primary_key = True)
    
    # relationships
    appello = relationship('Appello', back_populates='contenuti')
    esame = relationship('Esame', back_populates='contenuti')

    def __init__(self, ca, ce):
        self.codAppello = ca
        self.codEsame = ce
    
    def __repr__(self):
        return "< (codAppello='%s' codEsame='%s')>" % (self.codAppello, self.codEsame)