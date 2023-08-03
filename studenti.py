from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import hashlib
from classes import Studente

app = Flask(__name__)

app.debug = True

'''
la funzione sign_up_aux riceve come parametri la connessione al database, il codice fiscale dello studente, il nome, il cognome, la data di nascita, l'email, la password e il corso di laurea
i dati vengono inseriti nella tabella temporaryuser attraverso la INSERT
@param mysql
@param codicefiscale
@param name
@param surname
@param dateofbirth
@param email
@param password
@param corsolaurea

'''
def sign_up_aux(
    codicefiscale, name, surname, dateofbirth, email, password, corsolaurea, mysql
): 
    hash_password = hashlib.sha256(password.encode("utf-8"))
    hash_value = hash_password.hexdigest()

    if is_cf_present_in_studenti(codicefiscale, mysql):
        raise ValueError("Il Codice Fiscale è già presente nella tabella Docenti.")

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

'''
la funzione sign_up_corsolaurea riceve come parametri la connessione al database e la lista dei corsi di laurea
attraverso la SELECT seleziona i dati dei corsi di laurea e li visualizza a schermo
@param mysql
@param corsi

'''
def sign_up_corsolaurea(corsi, mysql):
    cursor = mysql.cursor()
    query = "SELECT NomeCorsoLaurea, CodCorsoLaurea FROM Corsi_di_Laurea"
    cursor.execute(query)

    rows = cursor.fetchall()
    i = 0
    for row in rows:
        insertResult(corsi, row[0], row[1])
        i += 1


def sign_up_control(
    codicefiscale, name, surname, dateofbirth, email, password, corsolaurea
):
    if not all(
        (codicefiscale, name, surname, dateofbirth, email, password, corsolaurea)
    ):
        return False
    else:
        return True


def insertResult(dictionaryL, rowSQL, string, number=None):
    # codicefiscale, nome, cognome, annoNascita, mail, matricola, password
    if number is not None:
        st = string + str(number)
    else:
        st = string

    dic = {st: rowSQL}

    dictionaryL.update(dic)


'''
la funzione is_cf_present_in_studenti riceve come parametro il codice fiscale del docente e restituisce True se il codice fiscale è presente tra gli studenti
@param cf_docente: codice fiscale del docente
@param mysql: connessione al database
@return count > 0: True se il codice fiscale è presente tra gli studenti, False altrimenti
'''
def is_cf_present_in_studenti(cf_docente, mysql):
    cursor = mysql.cursor()
    query = "SELECT COUNT(*) FROM Studenti WHERE CodiceFiscale = %s"
    cursor.execute(query, (cf_docente,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0


'''
la funzione bacheca_aux restituisce una lista di dizionari contenenti i dati degli esami effettuati dallo studente
riceve come parametri la connessione al database e il codice fiscale dello studente
@param mysql
@return righe_uniche
attraverso la SELECT seleziona i dati degli esami prenotati dallo studente e li inserisce in una lista di dizionari
'''
def bacheca_aux(mysql):
    cursor = mysql.cursor()
    cf = session.get("codicefiscale")
    query = "SELECT c.CodiceCorso, c.NomeCorso, e.Data, e.CodEsame FROM iscrizione_appelli ia JOIN esami e ON ia.Esame = e.CodEsame JOIN corsi c ON e.Corso = c.CodiceCorso JOIN studenti s ON ia.Studente = s.CodiceFiscale WHERE s.CodiceFiscale = %s"
    cursor.execute(query, (cf))
    effettuate_data = cursor.fetchall()
    cursor.close()
    righe_uniche = [
        {"CodiceCorso": row[0], "NomeCorso": row[1], "Data": row[2], "CodEsame": row[3]}
        for row in effettuate_data
    ]
    return righe_uniche

'''
la funzione prenotazioni_aux restituisce una lista di dizionari contenenti i dati degli esami prenotati dallo studente
riceve come parametri la connessione al database e il codice fiscale dello studente
@param mysql
@param cf
@return righe_iniziali
attraverso la SELECT seleziona i dati degli esami prenotabilo dallo studente e li inserisce in una lista di dizionari
'''
def prenotazioni_aux(mysql):
    corsolaurea = session.get("corsoLaurea")
    matricola = session.get("matricola")
    cursor = mysql.cursor()
    query = "SELECT c.CodiceCorso, c.NomeCorso, e.Data, e.CodEsame, e.Tipo  FROM studenti s JOIN corsi_di_laurea cl ON s.CorsoLaurea = cl.CodCorsoLaurea JOIN appartenenti a ON cl.CodCorsoLaurea = a.CorsoLaurea JOIN corsi c ON a.CodCorso = c.CodiceCorso JOIN esami e ON c.CodiceCorso = e.Corso WHERE s.CorsoLaurea = %s AND e.CodEsame NOT IN (SELECT Esame FROM sostenuti so JOIN studenti s ON so.Studente = s.CodiceFiscale WHERE matricola = %s)"
    cursor.execute(query, (corsolaurea, matricola))
    prenotazioni_data = cursor.fetchall()
    cursor.close()
    righe_iniziali = [
        {
            "CodiceCorso": row[0],
            "NomeCorso": row[1],
            "Data": row[2],
            "CodEsame": row[3],
            "Tipo": row[4],
        }
        for row in prenotazioni_data
    ]
    return righe_iniziali

'''
la funzione add_row_aux riceve come parametri la connessione al database, il codice dell'esame e il codice fiscale dello studente
i dati vengono inseriti nella tabella iscrizione_appelli attraverso la INSERT
@param mysql
@param esame
@param cf

'''
def add_row_aux(mysql, esame, cf):
    cursor = mysql.cursor()
    query = "INSERT INTO iscrizione_appelli(Studente, Esame) VALUES (%s, %s)"
    cursor.execute(query, (cf, esame))
    mysql.commit()
    cursor.close()

'''
la funzione delete_appello_aux riceve come parametri la connessione al database e il codice dell'esame
i dati vengono eliminati dalla tabella iscrizione_appelli attraverso la DELETE
@param mysql
@param esame

'''
def delete_appello_aux(mysql, esame):
    cursor = mysql.cursor()
    query = "DELETE FROM iscrizione_appelli WHERE Esame = %s"
    cursor.execute(query, (esame))
    print(query)
    mysql.commit()
    cursor.close()

'''
la funzione exam_details_aux restituisce una lista di dizionari contenenti i dati degli esami sostenuti dallo studente
riceve come parametri la connessione al database
@param mysql
@return exam_list
attraverso la SELECT seleziona i dati degli esami sostenuti dallo studente e li inserisce in una lista di dizionari
'''
def exam_details_aux(mysql):
    cursor = mysql.cursor()
    cf = session.get("codicefiscale")
    query = "SELECT c.CodiceCorso, c.NomeCorso, e.Data, so.voto FROM Studenti s JOIN Sostenuti so ON s.CodiceFiscale = so.Studente JOIN Esami e ON so.Esame = e.CodEsame JOIN Corsi c ON e.Corso = c.CodiceCorso WHERE s.CodiceFiscale = %s"
    cursor.execute(query, (cf))
    risultatiesami_data = cursor.fetchall()
    cursor.close()
    exam_list = [
        {
            "codice_corso": row[0],
            "nome_corso": row[1],
            "voto": row[2],
            "data_esame": row[3],
        }
        for row in risultatiesami_data
    ]
    return exam_list

def get_all_course(mysql):
    cursor = mysql.cursor()
    query = "SELECT * FROM Corsi c JOIN Appartenenti a ON c.CodiceCorso = a.CodCorso ORDER BY a.Anno"
    cursor.execute(query)

    rows = cursor.fetchall()
    mysql.commit()
    cursor.close()

    all_course = []
    for row in rows:
        data = {
            "codiceCorso": row[0],
            "nomeCorso": row[1],
            "codiceCorsoLaurea": row[2],
            "anno": row[4]
        }
        all_course.append(data)
    return all_course

def isNone(x):
    if x:
        return x
    else:
        return ""
    
'''
la funzione show_list_exam_aux restituisce una lista di dizionari contenenti i dati degli esami sostenuti dallo studente
riceve come parametri la connessione al database e il codice fiscale dello studente
@param mysql
@param cf
@return corsi
attraverso la SELECT seleziona i dati degli esami sostenuti dallo studente e li inserisce in una lista di dizionari
'''
def show_list_exam_aux(mysql, cf):
    cursor = mysql.cursor()
    query = "SELECT c.CodiceCorso, c.NomeCorso, s.data, s.voto, s.valore FROM Corsi c JOIN Appartenenti a ON c.CodiceCorso = a.CodCorso JOIN Studenti s ON a.CorsoLaurea = s.CorsoLaurea LEFT JOIN (SELECT e.Corso, e.data, s.voto, e.valore FROM Esami e JOIN Sostenuti s ON e.CodEsame = s.Esame WHERE s.Studente = %s) s ON c.CodiceCorso = s.Corso WHERE s.CodiceFiscale = %s"
    cursor.execute(query, (cf, cf))
    exam_data = cursor.fetchall()
    cursor.close()
    corsi = [
        {
            "CodiceCorso": row[0],
            "NomeCorso": row[1],
            "Data": isNone(row[2]),
            "Voto": isNone(row[3]),
            "Valore": isNone(row[4]),
        }
        for row in exam_data
    ]
    return corsi
