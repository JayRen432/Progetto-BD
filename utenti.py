from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import bcrypt
from classes import Studente

app = Flask(__name__)

app.debug = True


def login_aux(mail, password, mysql):
    cursor = mysql.cursor()
    query = 'SELECT * FROM studenti WHERE mail = %s AND password = %s'
    cursor.execute(query, (mail, password)) 
    studente = cursor.fetchone()
    cursor.close()

    if studente:
        return True, False
    else:
        cursor = mysql.cursor()
        query = 'SELECT * FROM docenti WHERE mail = %s AND password = %s'
        cursor.execute(query, (mail, password)) 
        docente = cursor.fetchone()
        cursor.close()

        if docente:
            return False, True 

    return False, False

def insertResult(dictionaryL, rowSQL, string, number=None):
    #codicefiscale, nome, cognome, annoNascita, mail, matricola, password
    if number is not None:
        st = string + str(number)
    else:
        st = string
    
    dic = {st: rowSQL}

    dictionaryL.update(dic)


def sign_up_aux(codicefiscale, name, surname, dateofbirth, email, password, corsolaurea, mysql):#inserisce uno studente nella tabella temporaryuser e ritorna 1
    hash_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
    cursor = mysql.cursor()
    query = 'INSERT INTO temporaryuser(codicefiscale, nome, cognome, annoNascita, mail, matricola, password, CorsoLaurea) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (codicefiscale, name, surname,
                       dateofbirth, email, "000000", hash_password, corsolaurea))
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


