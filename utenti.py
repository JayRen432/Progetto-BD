from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import bcrypt
from classes import Studente

app = Flask(__name__)

app.debug = True

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sf35dkn@!'
app.config['MYSQL_DATABASE_DB'] = 'progettobasi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = pymysql.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    db=app.config['MYSQL_DATABASE_DB']
)

def login_aux(mail, password):#ritorna 1 se è uno studente, 2 se è un docente, 0 se è un amministratore
    # hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor = mysql.cursor()
    query = 'SELECT * FROM studenti WHERE mail = %s AND password = %s'
    cursor.execute(query, (mail, password)) 
    user = cursor.fetchone()
    cursor.close()
    if user: 
        return 1
    else:
        cursor = mysql.cursor()
        query = 'SELECT * FROM docenti WHERE mail = %s AND password = %s'
        cursor.execute(query, (mail, password)) 
        user = cursor.fetchone()
        cursor.close()
        if user:
            return 2

def insertResult(dictionaryL, rowSQL, string, number=None):
    #codicefiscale, nome, cognome, annoNascita, mail, matricola, password
    if number is not None:
        st = string + str(number)
    else:
        st = string
    
    dic = {st: rowSQL}

    dictionaryL.update(dic)


def sign_up_aux(codicefiscale, name, surname, dateofbirth, email, password, corsolaurea):#inserisce uno studente nella tabella temporaryuser e ritorna 1
    hash_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
    cursor = mysql.cursor()
    query = 'INSERT INTO temporaryuser(codicefiscale, nome, cognome, annoNascita, mail, matricola, password, CorsoLaurea) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (codicefiscale, name, surname,
                       dateofbirth, email, "000000", hash_password, corsolaurea))
    mysql.commit()
    cursor.close()
    return 1
    
def sign_up_corsolaurea(corsi):
    cursor = mysql.cursor()
    query = 'SELECT NomeCorsoLaurea, CodCorsoLaurea FROM Corsi_di_Laurea'
    cursor.execute(query)

    rows = cursor.fetchall()
    i = 0
    for row in rows:
        insertResult(corsi, row[0], row[1])
        i += 1

if __name__ == "__main__":
    app.run()
