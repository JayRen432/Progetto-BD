-- Inserimento di 10 entry nella tabella Corsi_di_Laurea
INSERT INTO Corsi_di_Laurea (CodCorsoLaurea, NomeCorsoLaurea, Specializzazione, indirizzo)
VALUES
    ('CL001', 'Corso di Laurea 1', 'Specializzazione 1', 'Indirizzo 1'),
    ('CL002', 'Corso di Laurea 2', 'Specializzazione 2', 'Indirizzo 2'),
    ('CL003', 'Corso di Laurea 3', 'Specializzazione 3', 'Indirizzo 3');
    -- Aggiungi altre righe fino a 10 entry
-- Inserimento di 10 entry nella tabella Corsi
INSERT INTO Corsi (CodiceCorso, NomeCorso)
VALUES
    ('C001', 'Corso 1'),
    ('C002', 'Corso 2'),
    ('C003', 'Corso 3');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Appartenenti
INSERT INTO Appartenenti (CorsoLaurea, CodCorso, Anno)
VALUES
    ('CL001', 'C001', '2021'),
    ('CL001', 'C002', '2021'),
    ('CL002', 'C003', '2022');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Studenti
INSERT INTO Studenti (CodiceFiscale, Nome, Cognome, mail, annoNascita, matricola, password, CorsoLaurea)
VALUES
    ('ABC12345DEF67890', 'Mario', 'Rossi', 'mario.rossi@example.com', '1990', '202101', 'password1', 'CL001'),
    ('XYZ98765WVU43210', 'Laura', 'Bianchi', 'laura.bianchi@example.com', '1995', '202102', 'password2', 'CL002');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Docenti
INSERT INTO Docenti (CodiceFiscale, Nome, Cognome, mail, annoNascita, password)
VALUES
    ('FED12345CBA67890', 'Paolo', 'Verdi', 'paolo.verdi@example.com', '1985', 'password3'),
    ('LKJ98765HGF43210', 'Anna', 'Neri', 'anna.neri@example.com', '1978', 'password4');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Numeri_Telefono
INSERT INTO Numeri_Telefono (NumTelefono, CodFiscale)
VALUES
    ('1234567890', 'FED12345CBA67890'),
    ('0987654321', 'LKJ98765HGF43210');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Insegna
INSERT INTO Insegna (CodCorso, CodFiscale)
VALUES
    ('C001', 'FED12345CBA67890'),
    ('C002', 'LKJ98765HGF43210');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Esami
INSERT INTO Esami (CodEsame, Docente, Corso, NomeEsame, Data, Tipo, Valore)
VALUES
    ('E001', 'FED12345CBA67890', 'C001', 'Esame 1', '2023-07-28', 'Scritto', 30),
    ('E002', 'LKJ98765HGF43210', 'C002', 'Esame 2', '2023-07-29', 'Orale', 25);
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Sostenuti
INSERT INTO Sostenuti (Esame, Studente, voto)
VALUES
    ('E001', 'ABC12345DEF67890', '27'),
    ('E002', 'XYZ98765WVU43210', '22');
    -- Aggiungi altre righe fino a 10 entry

-- Inserimento di 10 entry nella tabella Iscrizione_Appelli
INSERT INTO Iscrizione_Appelli (Studente, Esame)
VALUES
    ('ABC12345DEF67890', 'E001'),
    ('XYZ98765WVU43210', 'E002');
    -- Aggiungi altre righe fino a 10 entry
