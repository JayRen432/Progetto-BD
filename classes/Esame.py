import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Esame(Base):
    __tablename__ = 'esami'   
     
    # attributes
    codEsame = Column(String, primary_key = True)
    docenteCreante = Column(String, ForeignKey('docenti.codFiscale'))
    corsoAvente = Column(String, ForeignKey('corsi.codCorso'))
    nomeEsame = Column(String)
    data = Column(Date)
    voto = Column(Integer)
    parziale = Column(Boolean)
    tipo = Column(String)
    valore = Column(Integer)
     
    # relationships
    docente = relationship('Docente', back_populates = 'esami')
    corso = relationship('Corso', back_populates='esami')
    contenuti = relationship('Contenuto', back_populates='esame')
    sostenuti = relationship('Sostenute', back_populates='esame')

    def __init__(self, ce, cf, cd, ename, data, voto, parziale, tipo, valore):
        self.codEsame = ce
        self.docenteCreante = cf
        self.corsoAvente = cd
        self.nomeEsame = ename
        self.data = data
        self.voto = voto
        self.parziale = parziale
        self.tipo = tipo
        self.valore = valore
    
    def __repr__(self):
        return "<Esame(codEsame='%s' docenteCreante='%s' corsoAvente='%s' nomeEsame='%s' data='%s' voto='%s' parziale='%s' tipo='%s' valore='%s')>" % (self.codEsame, self.docenteCreante, self.corsoAvente, self.nomeEsame, self.data, self.voto, self.parziale, self.tipo, self.valore) 
