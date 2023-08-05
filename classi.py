from flask import *
from flask.sessions import SessionMixin
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

passwordDB = "Sf35dkn%40!"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:" + passwordDB + "@localhost/progettobasi"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.debug = True
db = SQLAlchemy(app)  # Initialize the db instance

#classi
class Corsi_di_Laurea(db.Model):
    __tablename__ = "corsi_di_laurea"
    CodCorsoLaurea = db.Column(db.String(50), primary_key=True)
    NomeCorsoLaurea = db.Column(db.String(100), unique=True)
    Specializzazione = db.Column(db.String(100))
    indirizzo = db.Column(db.String(200))

class Corsi(db.Model):
    __tablename__ = "corsi"
    CodiceCorso = db.Column(db.String(50), primary_key=True)
    NomeCorso = db.Column(db.String(100), unique=True)

class Appartenenti(db.Model):
    __tablename__ = "appartenenti"
    CorsoLaurea = db.Column(db.String(50), db.ForeignKey('corsi_di_laurea.CodCorsoLaurea'), primary_key=True)
    CodCorso = db.Column(db.String(50), db.ForeignKey('corsi.CodiceCorso'), primary_key=True)
    Anno = db.Column(db.String(20))

class Studenti(db.Model):
    __tablename__ = "studenti"
    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(100))
    Cognome = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    annoNascita = db.Column(db.String(20))
    matricola = db.Column(db.String(6), unique=True)
    password = db.Column(db.String(520))
    CorsoLaurea = db.Column(db.String(30), db.ForeignKey('corsi_di_laurea.CodCorsoLaurea'))

class TemporaryUser(db.Model):
    __tablename__ = "temporaryUser"
    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(100))
    Cognome = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    annoNascita = db.Column(db.String(20))
    matricola = db.Column(db.String(6), default='000000')
    password = db.Column(db.String(520))
    CorsoLaurea = db.Column(db.String(30), db.ForeignKey('corsi_di_laurea.CodCorsoLaurea'))

class Docenti(db.Model):
    __tablename__ = "docenti"
    CodiceFiscale = db.Column(db.String(16), primary_key=True)
    Nome = db.Column(db.String(100))
    Cognome = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    annoNascita = db.Column(db.String(20))
    password = db.Column(db.String(520))

class Numeri_Telefono(db.Model):
    __tablename__ = "numeri_telfono"
    NumTelefono = db.Column(db.String(20), primary_key=True)
    CodFiscale = db.Column(db.String(16), db.ForeignKey('docenti.CodiceFiscale'))

class Insegna(db.Model):
    __tablename__ = "insegna"
    CodCorso = db.Column(db.String(50), db.ForeignKey('corsi.CodiceCorso'), primary_key=True)
    CodFiscale = db.Column(db.String(16), db.ForeignKey('docenti.CodiceFiscale'), primary_key=True)

class Esami(db.Model):
    __tablename__ = "esami"
    CodEsame = db.Column(db.String(50), primary_key=True)
    Docente = db.Column(db.String(16), db.ForeignKey('docenti.CodiceFiscale'))
    Corso = db.Column(db.String(50), db.ForeignKey('corsi.CodiceCorso'))
    NomeEsame = db.Column(db.String(100))
    Data = db.Column(db.Date)
    Tipo = db.Column(db.String(50))
    Valore = db.Column(db.Integer)
    ValorePerc = db.Column(db.Integer)

class Sostenuti(db.Model):
    __tablename__ = "sostenuti"
    Esame = db.Column(db.String(50), db.ForeignKey('esami.CodEsame'), primary_key=True)
    Studente = db.Column(db.String(16), db.ForeignKey('studenti.CodiceFiscale'), primary_key=True)
    voto = db.Column(db.String(5))

class Iscrizione_Appelli(db.Model):
    __tablename__ = "iscrizione_appelli"
    Studente = db.Column(db.String(16), db.ForeignKey('studenti.CodiceFiscale'), primary_key=True)
    Esame = db.Column(db.String(50), db.ForeignKey('esami.CodEsame'), primary_key=True)
