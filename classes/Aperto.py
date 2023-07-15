import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Aperto(Base):
    __tablename__ = 'aperti'
        
    # attributes
    codFiscale = Column(String, ForeignKey('docenti.codFiscale'), primary_key = True)
    codCorso = Column(String, ForeignKey('corsi.codCorso'), primary_key = True)
        
    # relationships
    corso = relationship('Corso', back_populates='aperti')
    docente = relationship('Docente', back_populates='aperti')

    def __init__(self, cf, cc):
        self.codFiscale = cf
        self.codCorso = cc
    
    def __repr__(self):
        return "< (codFiscale='%s' codCorso='%s')>" % (self.codFiscale, self.codCorso)