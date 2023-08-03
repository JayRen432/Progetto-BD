from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import hashlib
from classes import Studente

app = Flask(__name__)

app.debug = True


'''
    Funzione che permette di effettuare il login
    @param mail: mail dell'utente
    @param password: password dell'utente
    @param mysql: connessione al database
    @return info_studente: informazioni dello studente
    @return info_docente: informazioni del docente
'''
def login_aux(mail, password, mysql):
    hash_password = hashlib.sha256(password.encode("utf-8"))
    hash_value = hash_password.hexdigest()
    cursor = mysql.cursor()
    query = "SELECT * FROM studenti WHERE mail = %s AND password = %s"
    cursor.execute(query, (mail, hash_value))
    studente = cursor.fetchone()
    cursor.close()

    if studente:
        info_studente = {
            "codicefiscale": studente[0],
            "nome": studente[1],
            "cognome": studente[2],
            "annoNascita": studente[3],
            "mail": studente[4],
            "matricola": studente[5],
            "password": studente[6],
            "CorsoLaurea": studente[7],
        }
        return info_studente, None
    else:
        cursor = mysql.cursor()
        query = "SELECT * FROM docenti WHERE mail = %s AND password = %s"
        cursor.execute(query, (mail, hash_value))
        docente = cursor.fetchone()
        cursor.close()

        if docente:
            info_docente = {
                "codicefiscale": docente[0],
                "nome": docente[1],
                "cognome": docente[2],
                "annoNascita": docente[3],
                "mail": docente[4],
                "password": docente[5],
            }
            return None, info_docente

    return None, None

'''
    Funzione che riceve come parametro la mail dello studente o del docente e restituisce il ruolo corrispondente alla terminazione della mail
    @param mail: mail dell'utente
    @return Studente : ruolo dello studente
    @return Docente : ruolo dello docente
    @return None : ruolo assente
'''
def checkMail(mail):
    if "@stud.unive.it" in mail:
        return "Studente"
    elif "@unive.it" in mail:
        return "Docente"
    return "None"

'''
    Funzione che permette di effettuare il reset password
    @param mysql: connessione al database
    @param email: mail dell'utente
    @param pwd: password dell'utente
    @param c_pwd: password di conferma dell'utente
    @param tab: stringa riguardo a che tabella riferirsi
    @return redirect: informazioni dello studente
'''
def reset_pwd_aux(mysql, email, pwd, c_pwd, tab):
    if pwd == c_pwd:
        hash_password = hashlib.sha256(c_pwd.encode("utf-8"))
        hash_value = hash_password.hexdigest()
        cursor = mysql.cursor()
        if tab == "Studente":
            query = "UPDATE studenti SET password = %s WHERE mail = %s"
            cursor.execute(query, (hash_value, email))
            mysql.commit()
            cursor.close()
        elif tab == "Docente":
            query = "UPDATE docenti SET password = %s WHERE mail = %s"
            cursor.execute(query, (hash_value, email))
            mysql.commit()
            cursor.close()
        else:
            return redirect("/")
        return redirect("/login")
    return redirect("/")