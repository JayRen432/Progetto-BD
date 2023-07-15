import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Corso(Base):
    __tablename__ = 'corsi'
    
    # attributes
    codCorso = Column(String, primary_key = True)
    nomeCorso = Column(String, unique=True)

    # relationships
    appartenenti = relationship('Appartenente', back_populates='corso')
    aperti = relationship('Aperto', back_populates='corso')
    esami = relationship('Esame', back_populates='corso')
    
    def __init__(self, cd, cname):
        self.codCorso = cd
        self.nomeCorso = cname

    def __repr__(self):
        return "<Corso(codCorso='%s' nomeCorso='%s')>" % (self.codCorso, self.nomeCorso)