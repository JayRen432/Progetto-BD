from flask import Flask, render_template, request, redirect, session, jsonify
import hashlib
from classi import *

'''
    Funzione che permette di effettuare il login
    @param mail: mail dell'utente
    @param password: password dell'utente
    @param mysql: connessione al database
    @return info_studente: informazioni dello studente
    @return info_docente: informazioni del docente
'''
def login_aux(mail, password):
    hash_password = hashlib.sha256(password.encode("utf-8"))
    hash_value = hash_password.hexdigest()
    
    studente = Studenti.query.filter_by(mail=mail, password=hash_value).first()

    if studente:
        info_studente = {
            "codicefiscale": studente.CodiceFiscale,
            "nome": studente.Nome,
            "cognome": studente.Cognome,
            "annoNascita": studente.annoNascita,
            "mail": studente.mail,
            "matricola": studente.matricola,
            "password": studente.password,
            "CorsoLaurea": studente.CorsoLaurea,
        }
        return info_studente, None
    else:
        docente = Docenti.query.filter_by(mail=mail, password=hash_value).first()
        if docente:
            info_docente = {
                "codicefiscale": docente.CodiceFiscale,
                "nome": docente.Nome,
                "cognome": docente.Cognome,
                "annoNascita": docente.annoNascita,
                "mail": docente.mail,
                "password": docente.password,
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
def reset_pwd_aux(email, pwd, c_pwd, tab):
    if pwd == c_pwd:
        hash_password = hashlib.sha256(c_pwd.encode("utf-8"))
        hash_value = hash_password.hexdigest()
        if tab == "Studente":
            Studenti.query.filter_by(mail=email).update({"password": hash_value})
            db.session.commit()
        elif tab == "Docente":
            Docenti.query.filter_by(mail=email).update({"password": hash_value})
            db.session.commit()
        else:
            return redirect("/")
        session.clear()
        return redirect("/login")
    else:
        return redirect("/")