import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class NumeroTelefono(Base):
    __tablename__ = 'numeriTelefono'
    
    # attributes
    nTelefono = Column(String, primary_key = True)
    codFiscale = Column(String, ForeignKey('docenti.codFiscale'), primary_key = True)
    
    # relationships
    docente = relationship('Docente', back_populates='numeriTelefono')

    def __init__(self, tel, cf):
        self.nTelefono = tel
        self.codFiscale = cf
    
    def __repr__(self):
        return "< (nTelefono='%s' codFiscale='%s')>" % (self.nTelefono, self.codFiscale)
