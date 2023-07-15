import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Studente(Base):
    __tablename__ = 'studenti'

    # attributes
    codFiscale = Column(String, primary_key=True)
    nome = Column(String)
    cognome = Column(String)
    mail = Column(String, unique=True)
    annoNascita = Column(Integer)
    matricola = Column(String, unique=True)
    ruolo = Column(String)

    # relationships
    iscritti = relationship("Iscritto", back_populates="studente")
    sostenuti = relationship("Sostenente", back_populates="studente")

    def __init__(self, cf, name, surname, mail, year, code, role):
        self.codFiscale = cf
        self.nome = name
        self.cognome = surname
        self.mail = mail
        self.annoNascita = year
        self.matricola = code
        self.ruolo = role

    def __repr__(self):
        return "<Studente(codFiscale='%s' nome='%s' cognome='%s' mail='%s' annoNascita='%s' matricola='%s' ruolo='%s')>" % (self.codFiscale, self.nome, self.cognome, self.mail, self.annoNascita, self.matricola, self.ruolo)
