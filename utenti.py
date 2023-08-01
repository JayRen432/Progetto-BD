from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import hashlib
from classes import Studente

app = Flask(__name__)

app.debug = True


def login_aux(mail, password, mysql):
    hash_password = hashlib.sha256(password.encode('utf-8'))
    hash_value=hash_password.hexdigest()
    cursor = mysql.cursor()
    query = 'SELECT * FROM studenti WHERE mail = %s AND password = %s'
    cursor.execute(query, (mail, hash_value)) 
    studente = cursor.fetchone()
    cursor.close()

    if studente:
        info_studente = {'codicefiscale': studente[0],
                        'nome': studente[1],
                        'cognome': studente[2],
                        'annoNascita': studente[3],
                        'mail': studente[4],
                        'matricola': studente[5],
                        'password': studente[6],
                        'CorsoLaurea': studente[7]}
        return info_studente, None
    else:
        cursor = mysql.cursor()
        query = 'SELECT * FROM docenti WHERE mail = %s AND password = %s'
        cursor.execute(query, (mail, password)) 
        docente = cursor.fetchone()
        cursor.close()

        if docente:
            info_docente = {'codicefiscale': docente[0],
                            'nome': docente[1],
                            'cognome': docente[2],
                            'annoNascita': docente[3],
                            'mail': docente[4],
                            'password': docente[5]}
            return None, info_docente

    return None, None

def insertResult(dictionaryL, rowSQL, string, number=None):
    #codicefiscale, nome, cognome, annoNascita, mail, matricola, password
    if number is not None:
        st = string + str(number)
    else:
        st = string
    
    dic = {st: rowSQL}

    dictionaryL.update(dic)

def is_cf_present_in_docenti(cf_studente, mysql):
    cursor = mysql.cursor()
    query = "SELECT COUNT(*) FROM Docenti WHERE CodiceFiscale = %s"
    cursor.execute(query, (cf_studente,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def is_valid_codicefiscale(codicefiscale):

    if not codicefiscale[:6].isalpha():
        return False

    if not codicefiscale[6:8].isalnum() or not codicefiscale[9:11].isalnum() or not codicefiscale[12:15].isalnum():
        return False

    if not codicefiscale[8].isalpha() or not codicefiscale[11].isalpha() or not codicefiscale[15].isalpha():
        return False

    return True

def sign_up_aux(codicefiscale, name, surname, dateofbirth, email, password, corsolaurea, mysql):#inserisce uno studente nella tabella temporaryuser e ritorna 1
    hash_password = hashlib.sha256(password.encode('utf-8'))
    hash_value=hash_password.hexdigest()
    domini_consentiti = ["gmail.com", "outlook.com", "libero.it", "yahoo.com", "virgilio.it"]
    dominio = email.split("@")[-1].lower()
    if dominio not in domini_consentiti:
        raise ValueError("Email non valida. Utilizzare un'email con uno dei seguenti domini: @gmail.com, @outlook.com, @libero.it, @yahoo.com, @virgilio.it")
    
    if is_cf_present_in_docenti(codicefiscale, mysql):
        raise ValueError("Il Codice Fiscale è già presente nella tabella Docenti.")
    
    if not is_valid_codicefiscale(codicefiscale) or len(codicefiscale) != 16:
        raise ValueError("Il Codice Fiscale non è del formato giusto.")
    
    cursor = mysql.cursor()
    query = "INSERT INTO temporaryuser(codicefiscale, nome, cognome, annoNascita, mail, matricola, password, CorsoLaurea) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(
        query,
        (
            codicefiscale,
            name,
            surname,
            dateofbirth,
            email,
            "000000",
            hash_value,
            corsolaurea,
        ),
    )
    mysql.commit()
    cursor.close()
    return 1
    
def sign_up_corsolaurea(corsi, mysql):
    cursor = mysql.cursor()
    query = 'SELECT NomeCorsoLaurea, CodCorsoLaurea FROM Corsi_di_Laurea'
    cursor.execute(query)

    rows = cursor.fetchall()
    i = 0
    for row in rows:
        insertResult(corsi, row[0], row[1])
        i += 1

def crea_esame_inserisci(mysql, corso, nome_esame, codice_esame, data, tipo, valore, cf_docente):
    cursor = mysql.cursor()
    query = 'INSERT INTO esami (CodEsame, Docente, Corso, NomeEsame, Data, Tipo, Valore) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query,(codice_esame, cf_docente, corso, nome_esame, data, tipo, valore))
    mysql.commit()
    cursor.close()

def crea_esame_docenti(mysql,cf_docente):
    cursor = mysql.cursor()
    query = 'SELECT c.CodiceCorso  FROM corsi c JOIN insegna i ON c.CodiceCorso = i.CodCorso WHERE i.CodFiscale = %s'
    cursor.execute(query,(cf_docente,))
    course_data = cursor.fetchall()
    cursor.close()
    lista_corsi = [{'CodiceCorso': row[0]} for row in course_data]
    return lista_corsi

def take_cf(mysql, matr):
    cursor = mysql.cursor()
    query = 'SELECT CodiceFiscale FROM studenti WHERE matricola = %s'
    cursor.execute(query,(matr,))
    student = cursor.fetchone()
    cursor.close()
    return student
    
    
def assegna_voto_aux(mysql, codiceEsame):
    cursor = mysql.cursor()
    query = 'SELECT s.matricola, s.Nome, s.Cognome, s.CodiceFiscale FROM iscrizione_appelli ia JOIN studenti s ON ia.Studente = s.CodiceFiscale WHERE ia.Esame = %s'
    cursor.execute(query,(codiceEsame,))
    student_data = cursor.fetchall()
    cursor.close()
    studenti = [{'matricola': row[0], 'Nome': row[1], 'Cognome' : row[2]} for row in student_data]
    session['matricola'] = studenti[0]['matricola']
    return studenti

def tabella_esami(mysql):
    cf_docente = session.get('codicefiscale')
    cursor = mysql.cursor()
    query = 'SELECT e.CodEsame, e.Corso, e.Data, e.Tipo FROM esami e WHERE e.Docente = %s'
    cursor.execute(query,(cf_docente,))
    esami = []
    for row in cursor.fetchall():
        esame = {
            "CodEsame": row[0],
            "Corso": row[1],
            "Data": str(row[2]), 
            "Tipo": row[3]
        }
        esami.append(esame)
    cursor.close()
    return esami

def elimina_esame_post(mysql, esame, cf_docente):
    cursor = mysql.cursor()
    query = 'DELETE FROM esami WHERE CodEsame = %s AND Docente = %s'
    cursor.execute(query, (esame, cf_docente,))
    mysql.commit()
    cursor.close()

def elimina_esame_get(mysql, cf_docente):
    cursor = mysql.cursor()
    query = 'SELECT e.CodEsame, e.Corso, e.Data, e.Tipo, e.Valore FROM esami e WHERE e.Docente = %s'
    cursor.execute(query, (cf_docente,))
    exam_data = cursor.fetchall()
    cursor.close()
    lista_esami = [{'CodEsame': row[0], 'Corso': row[1], 'Data': row[2], 'Tipo': row[3], 'Valore': row[4]} for row in exam_data]
    return lista_esami

def phone_number_aux(mysql, cf_docente):
    phone_numbers = []
    cursor = mysql.cursor()
    query = 'SELECT NumTelefono FROM numeri_telefono WHERE CodFiscale = %s'
    cursor.execute(query, (cf_docente,))
    numbers_data = cursor.fetchall()
    cursor.close()
    phone_numbers = [row[0] for row in numbers_data]
    session['phone_numbers'] = phone_numbers 
    return phone_numbers 

def add_number_aux(mysql, number_to_add, cf_docente):
    if not number_to_add.isdigit() or len(number_to_add) != 10:
        raise ValueError("Il numero di telefono deve contenere esattamente 10 cifre.")
    cursor = mysql.cursor()
    query = 'INSERT INTO numeri_telefono(NumTelefono, CodFiscale) VALUES (%s, %s)'
    cursor.execute(query, (number_to_add, cf_docente))
    mysql.commit()
    cursor.close()

def delete_number_aux(mysql, numero_telefono, cf_docente):
    cursor = mysql.cursor()
    query = 'DELETE FROM numeri_telefono WHERE NumTelefono = %s AND CodFiscale = %s'
    cursor.execute(query, (numero_telefono, cf_docente))
    mysql.commit()
    cursor.close() 
    
def sign_up_control(
    codicefiscale, name, surname, dateofbirth, email, password, corsolaurea
):
    if not all(
        (codicefiscale, name, surname, dateofbirth, email, password, corsolaurea)
    ):
        return False
    else:
        return True

def bacheca_aux(mysql):
    cursor = mysql.cursor()
    cf = session.get('codicefiscale')
    query = 'SELECT c.CodiceCorso, c.NomeCorso, e.Data, e.CodEsame FROM iscrizione_appelli ia JOIN esami e ON ia.Esame = e.CodEsame JOIN corsi c ON e.Corso = c.CodiceCorso JOIN studenti s ON ia.Studente = s.CodiceFiscale WHERE s.CodiceFiscale = %s'
    cursor.execute(query, (cf))
    effettuate_data = cursor.fetchall()
    cursor.close()
    righe_uniche = [{'CodiceCorso': row[0], 'NomeCorso': row[1], 'Data': row[2], 'CodEsame': row[3]} for row in effettuate_data]
    return righe_uniche

def prenotazioni_aux(mysql):
    corsolaurea = session.get('corsoLaurea')
    matricola = session.get('matricola')
    cursor = mysql.cursor()
    query = 'SELECT c.CodiceCorso, c.NomeCorso, e.Data, e.CodEsame  FROM studenti s JOIN corsi_di_laurea cl ON s.CorsoLaurea = cl.CodCorsoLaurea JOIN appartenenti a ON cl.CodCorsoLaurea = a.CorsoLaurea JOIN corsi c ON a.CodCorso = c.CodiceCorso JOIN esami e ON c.CodiceCorso = e.Corso WHERE s.CorsoLaurea = %sAND e.CodEsame NOT IN (SELECT Esame FROM sostenuti so JOIN studenti s ON so.Studente = s.CodiceFiscale WHERE matricola = %s)'
    cursor.execute(query,(corsolaurea, matricola))
    prenotazioni_data = cursor.fetchall()
    cursor.close()
    righe_iniziali = [{'CodiceCorso': row[0], 'NomeCorso': row[1], 'Data': row[2], 'CodEsame': row[3]} for row in prenotazioni_data]
    return righe_iniziali

def add_row_aux(mysql, esame, cf):
    cursor = mysql.cursor()
    query = 'INSERT INTO iscrizione_appelli(Studente, Esame) VALUES (%s, %s)'
    cursor.execute(query, (cf, esame))
    mysql.commit()
    cursor.close()


def delete_appello_aux(mysql, esame):
    cursor = mysql.cursor()
    query = 'DELETE FROM iscrizione_appelli WHERE Esame = %s'
    cursor.execute(query, (esame))
    print(query)
    mysql.commit()
    cursor.close()


def exam_details_aux(mysql):
    cursor = mysql.cursor()
    cf = session.get('codicefiscale')
    query = 'SELECT c.CodiceCorso, c.NomeCorso, e.Data, so.voto FROM Studenti s JOIN Sostenuti so ON s.CodiceFiscale = so.Studente JOIN Esami e ON so.Esame = e.CodEsame JOIN Corsi c ON e.Corso = c.CodiceCorso WHERE s.CodiceFiscale = %s'
    cursor.execute(query, (cf))
    risultatiesami_data = cursor.fetchall()
    cursor.close()
    exam_list = [{'codice_corso': row[0], 'nome_corso': row[1], 'voto': row[2], 'data_esame': row[3]} for row in risultatiesami_data]
    return exam_list
