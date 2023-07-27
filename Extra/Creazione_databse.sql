CREATE DATABASE IF NOT EXISTS progettobasi;

-- Utilizzo del database
USE progettobasi;

-- Creazione della tabella Corsi_di_Laurea
CREATE TABLE Corsi_di_Laurea (
    CodCorsoLaurea VARCHAR(50) PRIMARY KEY,
    NomeCorsoLaurea VARCHAR(100) UNIQUE,
    Specializzazione VARCHAR(100),
    indirizzo VARCHAR(200)
);

-- Creazione della tabella Corsi
CREATE TABLE Corsi (
    CodiceCorso VARCHAR(50) PRIMARY KEY,
    NomeCorso VARCHAR(100) UNIQUE
);

-- Creazione della tabella Appartenenti
CREATE TABLE Appartenenti (
    CorsoLaurea VARCHAR(50),
    CodCorso VARCHAR(50),
    Anno VARCHAR(20),
    PRIMARY KEY (CorsoLaurea, CodCorso),
    FOREIGN KEY (CorsoLaurea) REFERENCES Corsi_di_Laurea(CodCorsoLaurea),
    FOREIGN KEY (CodCorso) REFERENCES Corsi(CodiceCorso)
);

-- Creazione della tabella Studenti
CREATE TABLE Studenti (
    CodiceFiscale VARCHAR(16) PRIMARY KEY,
    Nome VARCHAR(100),
    Cognome VARCHAR(100),
    mail VARCHAR(100),
    annoNascita VARCHAR(20),
    matricola VARCHAR(6) UNIQUE,
    password VARCHAR(520),
    CorsoLaurea VARCHAR(30),
	FOREIGN KEY (CorsoLaurea) REFERENCES Corsi_di_Laurea(CodCorsoLaurea)
);
CREATE TABLE temporaryuser (
    CodiceFiscale VARCHAR(16) PRIMARY KEY,
    Nome VARCHAR(100),
    Cognome VARCHAR(100),
    mail VARCHAR(100),
    annoNascita VARCHAR(20),
	matricola VARCHAR(6) DEFAULT '000000',
    password VARCHAR(520),
    CorsoLaurea VARCHAR(30),
	FOREIGN KEY (CorsoLaurea) REFERENCES Corsi_di_Laurea(CodCorsoLaurea)
);
-- Creazione della tabella Docenti
CREATE TABLE Docenti (
    CodiceFiscale VARCHAR(16) PRIMARY KEY,
    Nome VARCHAR(100),
    Cognome VARCHAR(100),
    mail VARCHAR(100),
    annoNascita VARCHAR(20),
    password VARCHAR(520)
);

-- Creazione della tabella Numeri_Telefono
CREATE TABLE Numeri_Telefono (
    NumTelefono VARCHAR(20) PRIMARY KEY,
    CodFiscale VARCHAR(16),
    FOREIGN KEY (CodFiscale) REFERENCES Docenti(CodiceFiscale)
);

-- Creazione della tabella Apero
CREATE TABLE Insegna (
    CodCorso VARCHAR(50),
    CodFiscale VARCHAR(16),
    PRIMARY KEY (CodCorso, CodFiscale),
    FOREIGN KEY (CodCorso) REFERENCES Corsi(CodiceCorso),
    FOREIGN KEY (CodFiscale) REFERENCES Docenti(CodiceFiscale)
);



-- Creazione della tabella Esami
CREATE TABLE Esami (
    CodEsame VARCHAR(50) PRIMARY KEY,
    Docente VARCHAR(16),
    Corso VARCHAR(50),
    NomeEsame VARCHAR(100),
    Data DATE,
    Tipo VARCHAR(50),
    Valore INT,
    FOREIGN KEY (Docente) REFERENCES Docenti(CodiceFiscale),
    FOREIGN KEY (Corso) REFERENCES Corsi(CodiceCorso)
);

-- Creazione della tabella Sostenuti
CREATE TABLE Sostenuti (
    Esame VARCHAR(50),
    Studente VARCHAR(16),
    voto VARCHAR(5),
    PRIMARY KEY (Esame, Studente),
    FOREIGN KEY (Esame) REFERENCES Esami(CodEsame),
    FOREIGN KEY (Studente) REFERENCES Studenti(CodiceFiscale)
);

-- Creazione tabella Iscrizione appello
CREATE TABLE Iscrizione_Appelli (
	Studente VARCHAR(16),
    Esame VARCHAR(50),
    PRIMARY KEY (Studente, Esame),
    FOREIGN KEY (Esame) REFERENCES Esami(CodEsame),
    FOREIGN KEY (Studente) REFERENCES Studenti(CodiceFiscale)
    )
    
