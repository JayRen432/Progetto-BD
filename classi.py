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


# If you have more tables or relationships, you can continue adding them to this file.
'''
class Appartenente(db.Model):
    __tablename__ = "appartenenti"

    # attributes
    CorsoLaurea = db.Column(
        db.String,
        db.ForeignKey("corsiLaurea.codCorsoLaurea", ondelete="CASCADE"),
        primary_key=True,
    )
    Corso = db.Column(
        db.String, db.ForeignKey("corsi.codCorso", ondelete="CASCADE"), primary_key=True
    )
    Anno = db.Column(db.String)

    # db.relationships
    corsoLaurea = db.relationship("CorsoLaurea", back_populates="appartenenti")
    corso = db.relationship("Corso", back_populates="appartenenti")

    def __init__(self, ccl, cc, year):
        self.CorsoLaurea = ccl
        self.Corso = cc
        self.Anno = year

    def __repr__(self):
        return "< (CorsoLaurea='%s' Corso='%s' Anno='%s')>" % (
            self.CorsoLaurea,
            self.Corso,
            self.Anno,
        )


class Insegna(db.Model):
    __tablename__ = "insegnano"

    # attributes
    codFiscale = db.Column(
        db.String,
        db.ForeignKey("docenti.codFiscale", ondelete="CASCADE"),
        primary_key=True,
    )
    codCorso = db.Column(
        db.String, db.ForeignKey("corsi.codCorso", ondelete="CASCADE"), primary_key=True
    )

    # db.relationships
    corso = db.relationship("Corso", back_populates="insegnano")
    docente = db.relationship("Docente", back_populates="insegnano")

    def __init__(self, cf, cc):
        self.codFiscale = cf
        self.codCorso = cc

    def __repr__(self):
        return "< (codFiscale='%s' codCorso='%s')>" % (self.codFiscale, self.codCorso)


class Sostenuto(db.Model):
    __tablename__ = "sostenuti"

    # attributes
    codFiscale = db.Column(
        db.String, db.ForeignKey("studenti.codFiscale"), primary_key=True
    )
    codEsame = db.Column(db.String, db.ForeignKey("esami.codEsame"), primary_key=True)
    voto = db.Column(db.Integer)

    # db.relationships
    studente = db.relationship("Studente", back_populates="sostenuti")
    esame = db.relationship("Esame", back_populates="sostenuti")

    def __init__(self, cf, ce, v):
        self.codFiscale = cf
        self.codEsame = ce
        self.voto = v

    def __repr__(self):
        return "< (codFiscale='%s' codEsame='%s' voto='%s')>" % (
            self.codFiscale,
            self.codEsame,
            self.voto,
        )


class Iscrizione_Appello(db.Model):
    __tablename__ = "iscrizione_appelli"

    # attributes
    Studente = db.Column(
        db.String,
        db.ForeignKey("studenti.codFiscale", ondelete="CASCADE"),
        primary_key=True,
    )
    Esame = db.Column(
        db.String, db.ForeignKey("esami.codEsame", ondelete="CASCADE"), primary_key=True
    )

    # db.relationships
    studente = db.relationship("Studente", back_populates="iscrizione_appelli")
    esame = db.relationship("Esame", back_populates="iscrizione_appelli")

    def __init__(self, st, e):
        self.Studente = st
        self.Esame = e

    def __repr__(self):
        return "<Corso(Studente='%s' Esame='%s')>" % (self.Studente, self.Esame)


class CorsoLaurea(db.Model):
    __tablename__ = "corsiLaurea"

    # attributes
    codCorsoLaurea = db.Column(db.String, primary_key=True)
    nomeCorsoLaurea = db.Column(db.String, unique=True)
    specializzazione = db.Column(db.String)
    indirizzo = db.Column(db.String)

    # db.relationships
    appartenenti = db.relationship("Appartenente", back_populates="corsoLaurea")
    studenti = db.relationship("Studente", back_populates="corsoLaurea")
    temporaryUsers = db.relationship("TemporaryUser", back_populates="corsoLaurea")

    def __init__(self, ccl, namecl, special, address):
        self.codCorsoLaurea = ccl
        self.nomeCorsoLaurea = namecl
        self.specializzazione = special
        self.indirizzo = address

    def __repr__(self):
        return (
            "<CorsoLaurea(codCorsoLaurea='%s' nomeCorsoLaurea='%s' specializzazione='%s' indirizzo='%s')>"
            % (
                self.codCorsoLaurea,
                self.nomeCorsoLaurea,
                self.specializzazione,
                self.indirizzo,
            )
        )


class TemporaryUser(db.Model):
    __tablename__ = "temporaryUsers"

    # attributes
    codFiscale = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String)
    cognome = db.Column(db.String)
    mail = db.Column(db.String, unique=True)
    annoNascita = db.Column(db.Date)
    matricola = db.Column(db.String, default="000000")
    password = db.Column(db.String)
    corsoLaurea = db.Column(
        db.String, db.ForeignKey("corsiLaurea.codCorsoLaurea", ondelete="CASCADE")
    )

    # db.relationships
    corsoLaurea = db.relationship("CorsoLaurea", back_populates="temporaryUsers")

    def __init__(self, cf, name, surname, mail, year, code, pwd, cl):
        self.codFiscale = cf
        self.nome = name
        self.cognome = surname
        self.mail = mail
        self.annoNascita = year
        self.matricola = code
        self.password = pwd
        self.corsoLaurea = cl

    def __repr__(self):
        return (
            "<Studente(codFiscale='%s' nome='%s' cognome='%s' mail='%s' annoNascita='%s' matricola='%s' password='%s' corsoLaurea='%s')>"
            % (
                self.codFiscale,
                self.nome,
                self.cognome,
                self.mail,
                self.annoNascita,
                self.matricola,
                self.password,
                self.corsoLaurea,
            )
        )


class Studente(db.Model):
    __tablename__ = "studenti"

    # attributes
    codFiscale = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String)
    cognome = db.Column(db.String)
    mail = db.Column(db.String, unique=True)
    annoNascita = db.Column(db.Date)
    matricola = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    corsoLaurea = db.Column(
        db.String, db.ForeignKey("corsiLaurea.codCorsoLaurea", ondelete="CASCADE")
    )

    # db.relationships
    iscrizione_appelli = db.relationship(
        "Iscrizione_Appello", back_populates="studente"
    )
    sostenuti = db.relationship("Sostenuto", back_populates="studente")
    corsoLaurea = db.relationship("CorsoLaurea", back_populates="studenti")

    def __init__(self, cf, name, surname, mail, year, code, pwd, cl):
        self.codFiscale = cf
        self.nome = name
        self.cognome = surname
        self.mail = mail
        self.annoNascita = year
        self.matricola = code
        self.password = pwd
        self.corsoLaurea = cl

    def __repr__(self):
        return (
            "<Studente(codFiscale='%s' nome='%s' cognome='%s' mail='%s' annoNascita='%s' matricola='%s' password='%s' corsoLaurea='%s')>"
            % (
                self.codFiscale,
                self.nome,
                self.cognome,
                self.mail,
                self.annoNascita,
                self.matricola,
                self.password,
                self.corsoLaurea,
            )
        )


class NumeroTelefono(db.Model):
    __tablename__ = "numeriTelefono"

    # attributes
    nTelefono = db.Column(db.String, primary_key=True)
    codFiscale = db.Column(
        db.String,
        db.ForeignKey("docenti.codFiscale", ondelete="CASCADE"),
        primary_key=True,
    )

    # db.relationships
    docente = db.relationship("Docente", back_populates="numeriTelefono")

    def __init__(self, tel, cf):
        self.nTelefono = tel
        self.codFiscale = cf

    def __repr__(self):
        return "< (nTelefono='%s' codFiscale='%s')>" % (self.nTelefono, self.codFiscale)


class Esame(db.Model):
    __tablename__ = "esami"

    # attributes
    codEsame = db.Column(db.String, primary_key=True)
    docente = db.Column(
        db.String, db.ForeignKey("docenti.codFiscale", ondelete="CASCADE")
    )
    corso = db.Column(db.String, db.ForeignKey("corsi.codCorso", ondelete="CASCADE"))
    nomeEsame = db.Column(db.String)
    data = db.Column(db.Date)
    tipo = db.Column(db.String)
    valore = db.Column(db.Integer)

    # db.relationships
    docente = db.relationship("Docente", back_populates="esami")
    corso = db.relationship("Corso", back_populates="esami")
    iscrizione_appelli = db.relationship("Iscrizione_appello", back_populates="esame")
    sostenuti = db.relationship("Sostenuto", back_populates="esame")

    def __init__(self, ce, cf, cd, ename, data, tipo, valore):
        self.codEsame = ce
        self.docente = cf
        self.corso = cd
        self.nomeEsame = ename
        self.data = data
        self.tipo = tipo
        self.valore = valore

    def __repr__(self):
        return (
            "<Esame(codEsame='%s' docente='%s' corso='%s' nomeEsame='%s' data='%s' tipo='%s' valore='%s')>"
            % (
                self.codEsame,
                self.docente,
                self.corso,
                self.nomeEsame,
                self.data,
                self.tipo,
                self.valore,
            )
        )


class Docente(db.Model):
    __tablename__ = "docenti"

    # attributes
    codFiscale = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String)
    cognome = db.Column(db.String)
    mail = db.Column(db.String, unique=True)
    annoNascita = db.Column(db.Date)
    password = db.Column(db.String)

    # db.relationships
    insegnano = db.relationship("Insegna", back_populates="docente")
    numeriTelefono = db.relationship("NumeroTelefono", back_populates="docente")
    esami = db.relationship("Esame", back_populates="docente")

    def __init__(self, cf, name, surname, mail, year, pwd):
        self.codFiscale = cf
        self.nome = name
        self.cognome = surname
        self.mail = mail
        self.annoNascita = year
        self.password = pwd

    def __repr__(self):
        return (
            "<Docente(codFiscale='%s' nome='%s' cognome='%s' mail='%s' annoNascita='%s' password='%s')>"
            % (
                self.codFiscale,
                self.nome,
                self.cognome,
                self.mail,
                self.annoNascita,
                self.password,
            )
        )


class Corso(db.Model):
    __tablename__ = "corsi"

    # attributes
    codCorso = db.Column(db.String, primary_key=True)
    nomeCorso = db.Column(db.String, unique=True)

    # db.relationships
    appartenenti = db.relationship("Appartenente", back_populates="corso")
    insegnano = db.relationship("Insegna", back_populates="corso")
    esami = db.relationship("Esame", back_populates="corso")

    def __init__(self, cd, cname):
        self.codCorso = cd
        self.nomeCorso = cname

    def __repr__(self):
        return "<Corso(codCorso='%s' nomeCorso='%s')>" % (self.codCorso, self.nomeCorso)
'''