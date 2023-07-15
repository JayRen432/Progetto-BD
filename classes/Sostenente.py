import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sostenente(Base):
    __tablename__ = 'sostenenti'
    
    # attributes
    codFiscale = Column(String, ForeignKey('studenti.codFiscale'), primary_key = True)
    codEsame = Column(String, ForeignKey('esami.codEsame'), primary_key = True)

    # relationships
    studente = relationship('Studente', back_populates='sostenenti')
    esame = relationship('Esame', back_populates='sostenenti')

    def __init__(self, cf, ce):
        self.codFiscale = cf
        self.codEsame = ce
    
    def __repr__(self):
        return "< (codFiscale='%s' codEsame='%s')>" % (self.codFiscale, self.codEsame)