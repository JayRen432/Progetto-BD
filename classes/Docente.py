import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Docente(Base):
    __tablename__ = 'docenti'
    
    # attributes
    codFiscale = Column(String, primary_key = True)
    nome = Column(String)
    cognome = Column(String)
    mail = Column(String, unique=True)
    annoNascita = Column(Integer)
    ruolo = Column(String)
    
    # relationships
    aperti = relationship('Aperto', back_populates='docente')
    numeriTelefono = relationship('NumeroTelefono', back_populates='docente')
    esami = relationship('Esame', back_populates='docente')

    def __init__(self, cf, name, surname, mail, year, role):
        self.codFiscale = cf
        self.nome = name
        self.cognome = surname
        self.mail = mail
        self.annoNascita = year
        self.ruolo = role
    
    def __repr__(self):
        return "<Docente(codFiscale='%s' nome='%s' cognome='%s' mail='%s' annoNascita='%s' matricola='%s' ruolo='%s')>" % (self.codFiscale, self.nome, self.cognome, self.mail, self.annoNascita, self.matricola, self.ruolo) 
