import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CorsoLaurea(Base):
    __tablename__ = 'corsiLaurea'
    
    # attributes
    codCorsoLaurea = Column(String, primary_key = True)
    nomeCorsoLaurea = Column(String, unique=True)
    specializzazione = Column(String)
    indirizzo = Column(String)

    # relationships
    appartenenti= relationship('Appartenente', back_populates='corsoLaurea')

    def __init__(self, ccl, namecl, special, address):
        self.codCorsoLaurea = ccl
        self.nomeCorsoLaurea = namecl
        self.specializzazione = special
        self.indirizzo = address

    def __repr__(self):
        return "<CorsoLaurea(codCorsoLaurea='%s' nomeCorsoLaurea='%s' specializzazione='%s' indirizzo='%s')>" % (self.codCorsoLaurea, self.nomeCorsoLaurea, self.specializzazione, self.indirizzo)
