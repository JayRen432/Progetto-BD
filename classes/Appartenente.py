import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Appartenente(Base):
    __tablename__ = 'appartenenti'
     
    # attributes
    codCorsoLaurea = Column(String, ForeignKey('corsiLaurea.codCorsoLaurea'), primary_key = True)
    codCorso = Column(String, ForeignKey('corsi.codCorso'), primary_key = True)
    
    # relationships
    corsoLaurea = relationship('CorsoLaurea', back_populates='appartenenti')
    corso = relationship('Corso', back_populates='appartenenti')

    def __init__(self, ccl, cc):
        self.codCorsoLaurea = ccl
        self.codCorso = cc

    def __repr__(self):
        return "< (codCorsoLaurea='%s' codCorso='%s')>" % (self.codCorsoLaurea, self.codCorso)