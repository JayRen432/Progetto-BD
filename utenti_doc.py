from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import hashlib


'''
la funzione crea_esame_inserisci riceve come parametri la connessione al database, il corso, il nome dell'esame, il codice dell'esame, la data, il tipo e il valore
i dati vengono inseriti nella tabella esami attraverso la INSERT
@param mysql
@param corso
@param nome_esame
@param codice_esame
@param data
@param tipo
@param valore
@param cf_docente

'''
def crea_esame_inserisci(
    mysql, corso, nome_esame, codice_esame, data, tipo, valore, cf_docente
):
    cursor = mysql.cursor()
    query = "INSERT INTO esami (CodEsame, Docente, Corso, NomeEsame, Data, Tipo, Valore) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(
        query, (codice_esame, cf_docente, corso, nome_esame, data, tipo, valore)
    )
    mysql.commit()
    cursor.close()

'''
la funzione crea_esame_docenti riceve come parametri la connessione al database e il codice fiscale del docente
@param mysql
@param cf_docente
@return lista_corsi
attraverso una query seleziona i dati dei corsi insegnati dal docente attraverso la SELECT e li inserisce in una lista di dizionari

'''
def crea_esame_docenti(mysql, cf_docente):
    cursor = mysql.cursor()
    query = "SELECT c.CodiceCorso, c.NomeCorso  FROM corsi c JOIN insegna i ON c.CodiceCorso = i.CodCorso WHERE i.CodFiscale = %s"
    cursor.execute(query, (cf_docente,))
    course_data = cursor.fetchall()
    cursor.close()
    lista_corsi = [{"CodiceCorso": row[0], "NomeCorso": row[1]} for row in course_data]
    return lista_corsi

'''
la funzione assegna_voto_aux restituisce una lista di dizionari contenenti i dati degli studenti iscritti all'esame
riceve come parametri la connessione al database e il codice dell'esame
@param mysql
@param codiceEsame
@return studenti

'''
def assegna_voto_aux(mysql, codiceEsame):
    cursor = mysql.cursor()
    query = "SELECT s.matricola, s.Nome, s.Cognome, s.CodiceFiscale FROM iscrizione_appelli ia JOIN studenti s ON ia.Studente = s.CodiceFiscale WHERE ia.Esame = %s"
    cursor.execute(query, (codiceEsame,))
    student_data = cursor.fetchall()
    cursor.close()
    studenti = [
        {"matricola": row[0], "Nome": row[1], "Cognome": row[2]} for row in student_data
    ]
    session["matricola"] = studenti[0]["matricola"]
    return studenti

'''
la funzione elimina_esame_post riceve come parametri la connessione al database, il codice dell'esame e il codice fiscale del docente
i dati vengono eliminati dalla tabella esami attraverso la DELETE
@param mysql
@param esame
@param cf_docente

'''
def elimina_esame_post(mysql, esame, cf_docente):
    cursor = mysql.cursor()
    query = "DELETE FROM esami WHERE CodEsame = %s AND Docente = %s"
    cursor.execute(
        query,
        (
            esame,
            cf_docente,
        ),
    )
    mysql.commit()
    cursor.close()

'''
la funzione elimina_esame_get riceve come parametri la connessione al database e il codice fiscale del docente
attraverso una query seleziona i dati degli esami insegnati dal docente attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@param cf_docente
@return lista_esami

'''
def elimina_esame_get(mysql, cf_docente):
    cursor = mysql.cursor()
    query = "SELECT e.CodEsame, e.Corso, e.Data, e.Tipo, e.Valore FROM esami e WHERE e.Docente = %s"
    cursor.execute(query, (cf_docente,))
    exam_data = cursor.fetchall()
    cursor.close()
    lista_esami = [
        {
            "CodEsame": row[0],
            "Corso": row[1],
            "Data": row[2],
            "Tipo": row[3],
            "Valore": row[4],
        }
        for row in exam_data
    ]
    return lista_esami

'''
la funzione phone_number_aux riceve come parametri la connessione al database e il codice fiscale del docente
attraverso una query seleziona i dati dei numeri di telefono del docente attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@param cf_docente
@return phone_numbers

'''
def phone_number_aux(mysql, cf_docente):
    phone_numbers = []
    cursor = mysql.cursor()
    query = "SELECT NumTelefono FROM numeri_telefono WHERE CodFiscale = %s"
    cursor.execute(query, (cf_docente,))
    numbers_data = cursor.fetchall()
    cursor.close()
    phone_numbers = [row[0] for row in numbers_data]
    session["phone_numbers"] = phone_numbers
    return phone_numbers

'''
la funzione add_number_aux riceve come parametri la connessione al database, il numero di telefono e il codice fiscale del docente
i dati vengono inseriti nella tabella numeri_telefono attraverso la INSERT
@param mysql
@param number_to_add
@param cf_docente

'''
def add_number_aux(mysql, number_to_add, cf_docente):
    cursor = mysql.cursor()
    query = "INSERT INTO numeri_telefono(NumTelefono, CodFiscale) VALUES (%s, %s)"
    cursor.execute(query, (number_to_add, cf_docente))
    mysql.commit()
    cursor.close()

'''
la funzione delete_number_aux riceve come parametri la connessione al database, il numero di telefono e il codice fiscale del docente
i dati vengono eliminati dalla tabella numeri_telefono attraverso la DELETE
@param mysql
@param numero_telefono
@param cf_docente

'''
def delete_number_aux(mysql, numero_telefono, cf_docente):
    cursor = mysql.cursor()
    query = "DELETE FROM numeri_telefono WHERE NumTelefono = %s AND CodFiscale = %s"
    cursor.execute(query, (numero_telefono, cf_docente))
    mysql.commit()
    cursor.close()

'''
la funzione ricevi_dati_aux riceve come parametri la connessione al database, il codice fiscale dello studente, il codice dell'esame e il voto
@param mysql
@param cf
@param codiceEsame
@param voto
i dati vengono inseriti nella tabella sostenuti attraverso la INSERT
'''
def ricevi_dati_aux(mysql, cf, codiceEsame, voto):
    cursor = mysql.cursor()
    query = "INSERT INTO sostenuti(Esame, Studente, voto) VALUES(%s, %s, %s)"
    cursor.execute(query, (codiceEsame, cf, voto))
    mysql.commit()
    cursor.close()


'''
la funzione take_cf riceve come parametri la connessione al database e la matricola dello studente
@param mysql
@param matr
@return student

'''
def take_cf(mysql, matr):
    cursor = mysql.cursor()
    query = "SELECT CodiceFiscale FROM studenti WHERE matricola = %s"
    cursor.execute(query, (matr,))
    student = cursor.fetchone()
    cursor.close()
    return student

'''
la funzione tabella_esame riceve come parametri la connessione al database e attraverso 
una query seleziona i dati degli esami attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@return esami

'''
def tabella_esami(mysql):
    cf_docente = session.get("codicefiscale")
    cursor = mysql.cursor()

    query = "SELECT E.CodEsame, E.Corso, E.Data, E.Tipo FROM Esami E LEFT JOIN (SELECT Esame, COUNT(*) AS num_sostenuti FROM Sostenuti GROUP BY Esame) S ON E.CodEsame = S.Esame LEFT JOIN (SELECT Esame, COUNT(*) AS num_iscrizioni FROM Iscrizione_Appelli GROUP BY Esame) I ON E.CodEsame = I.Esame WHERE E.Docente = %s AND (S.num_sostenuti < I.num_iscrizioni OR (S.num_sostenuti IS NULL AND I.num_iscrizioni > 0) OR (S.num_sostenuti = 0 AND I.num_iscrizioni > 0))"
    cursor.execute(query, cf_docente)
    esami = []
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            esame = {
                "CodEsame": row[0],
                "Corso": row[1],
                "Data": str(row[2]),
                "Tipo": row[3],
            }
            esami.append(esame)
    cursor.close()
    return esami
