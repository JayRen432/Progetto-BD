from flask import Flask, render_template, request, redirect, session, jsonify
import hashlib
from classi import *
from sqlalchemy import create_engine, Column, Integer, String, MetaData, ForeignKey, Date, Float, and_, select
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
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
def sign_up_aux(codicefiscale, name, surname, dateofbirth, email, password, corsolaurea): 
    hash_password = hashlib.sha256(password.encode("utf-8"))
    hash_value = hash_password.hexdigest()

    if is_cf_present_in_studenti(codicefiscale):
        raise ValueError("Il Codice Fiscale è già presente nella tabella Docenti.")

    temporary_user = TemporaryUser(
        CodiceFiscale=codicefiscale,
        Nome=name,
        Cognome=surname,
        annoNascita=dateofbirth,
        mail=email,
        matricola="000000",
        password=hash_value,
        CorsoLaurea=corsolaurea
    )

    # Add the temporary_user to the session and commit the changes
    db.session.add(temporary_user)
    db.session.commit()

    return 1

'''
la funzione sign_up_corsolaurea riceve come parametri la connessione al database e la lista dei corsi di laurea
attraverso la SELECT seleziona i dati dei corsi di laurea e li visualizza a schermo
@param mysql
@param corsi

'''
def sign_up_corsolaurea(corsi):
    rows = Corsi_di_Laurea.query.all()
    if rows:
        for row in rows:
            insertResult(corsi, row.NomeCorsoLaurea, row.CodCorsoLaurea)


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
def is_cf_present_in_studenti(cf_docente):
    count = Studenti.query.filter_by(CodiceFiscale = cf_docente).count()
    return count > 0


'''
la funzione bacheca_aux restituisce una lista di dizionari contenenti i dati degli esami effettuati dallo studente
riceve come parametri la connessione al database e il codice fiscale dello studente
@param mysql
@return righe_uniche
attraverso la SELECT seleziona i dati degli esami prenotati dallo studente e li inserisce in una lista di dizionari
'''
def bacheca_aux(cf):
    effettuate_data = Iscrizione_Appelli.query.join(Esami, Iscrizione_Appelli.Esame == Esami.CodEsame).join(Corsi, Esami.Corso == Corsi.CodiceCorso).join(Studenti, Iscrizione_Appelli.Studente == Studenti.CodiceFiscale).filter(Studenti.CodiceFiscale == cf, and_(func.current_date() < Esami.Data)).with_entities(Corsi.CodiceCorso, Corsi.NomeCorso, Esami.Data, Esami.CodEsame)
    righe_uniche = [
        {"CodiceCorso": row.CodiceCorso, "NomeCorso": row.NomeCorso, "Data": row.Data, "CodEsame": row.CodEsame}
        for row in effettuate_data
    ]
    return righe_uniche

'''
la funzione prenotazioni_aux restituisce una lista di dizionari contenenti i dati degli esami prenotati dallo studente
riceve come parametri la connessione al database e il codice fiscale dello studente
@param mysql
@param cf
@return righe_iniziali
attraverso la SELECT seleziona i dati degli esami prenotabili dallo studente e li inserisce in una lista di dizionari
'''
def prenotazioni_aux(corsolaurea, matricola):
    #subquery = Sostenuti.query.join(Studenti, Sostenuti.Studente == Studenti.CodiceFiscale).filter(Studenti.matricola == matricola, and_(Sostenuti.voto == 'INSUF' or (Sostenuti.voto).)).with_entities(Sostenuti.Esame)
   # subquery = subquery.subquery()
    esami_insufficienti = (
    Studenti.query
    .join(Corsi_di_Laurea, Studenti.CorsoLaurea == Corsi_di_Laurea.CodCorsoLaurea)
    .join(Appartenenti, Corsi_di_Laurea.CodCorsoLaurea == Appartenenti.CorsoLaurea)
    .join(Corsi, Appartenenti.CodCorso == Corsi.CodiceCorso)
    .join(Esami, Corsi.CodiceCorso == Esami.Corso)
    .outerjoin(Sostenuti, and_(Studenti.CodiceFiscale == Sostenuti.Studente, Esami.CodEsame == Sostenuti.Esame))
    .filter(and_(Studenti.matricola == matricola, Sostenuti.voto == 'INSUF'))
    .with_entities(Corsi.CodiceCorso, Corsi.NomeCorso, Esami.Data, Esami.CodEsame, Esami.Tipo)
    .distinct()
)

    esami_senza_voto = (
    Studenti.query
    .join(Corsi_di_Laurea, Studenti.CorsoLaurea == Corsi_di_Laurea.CodCorsoLaurea)
    .join(Appartenenti, Corsi_di_Laurea.CodCorsoLaurea == Appartenenti.CorsoLaurea)
    .join(Corsi, Appartenenti.CodCorso == Corsi.CodiceCorso)
    .join(Esami, Corsi.CodiceCorso == Esami.Corso)
    .outerjoin(Sostenuti, and_(Studenti.CodiceFiscale == Sostenuti.Studente, Esami.CodEsame == Sostenuti.Esame))
    .filter(and_(Studenti.matricola == matricola, Sostenuti.voto == None))
    .with_entities(Corsi.CodiceCorso, Corsi.NomeCorso, Esami.Data, Esami.CodEsame, Esami.Tipo)
    .distinct()
)
    prenotazioni_data = esami_insufficienti.union(esami_senza_voto)
    #prenotazioni_data = db.session.query(Esami).outerjoin(Iscrizione_Appelli, (Esami.CodEsame == Iscrizione_Appelli.Esame) & (Iscrizione_Appelli.Studente == Studenti.CodiceFiscale)).outerjoin(Sostenuti, (Esami.CodEsame == Sostenuti.Esame) & (Sostenuti.Studente == matricola)).filter((Iscrizione_Appelli.Studente == None) | ((Sostenuti.voto == 'INSUF') & (Sostenuti.Studente == matricola))).all()
    
    righe_iniziali = [
        {
            "CodiceCorso": row.CodiceCorso,
            "NomeCorso": row.NomeCorso,
            "Data": row.Data,
            "CodEsame": row.CodEsame,
            "Tipo": row.Tipo,
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
def add_row_aux(esame, cf):
    iscrizioni = Iscrizione_Appelli( Studente = cf, Esame = esame)
    db.session.add(iscrizioni)
    db.session.commit()

'''
la funzione delete_appello_aux riceve come parametri la connessione al database e il codice dell'esame
i dati vengono eliminati dalla tabella iscrizione_appelli attraverso la DELETE
@param mysql
@param esame

'''
def delete_appello_aux(esame):
    Iscrizione_Appelli.query.filter_by(Esame = esame).delete()
    db.session.commit()

def which_voto(voto):
    if voto is not None:
        if voto == 0:
            return 'INSUF'
        elif voto > 30: 
            return '30L'
        else:
            return voto
    else:
       return ""

'''
la funzione exam_details_aux restituisce una lista di dizionari contenenti i dati degli esami sostenuti dallo studente
riceve come parametri la connessione al database
@param mysql
@return exam_list
attraverso la SELECT seleziona i dati degli esami sostenuti dallo studente e li inserisce in una lista di dizionari
'''
def exam_details_aux(cf):
    cf = session.get("codicefiscale")
    max_data = Corsi.query.join(Appartenenti, Corsi.CodiceCorso == Appartenenti.CodCorso).join(Esami, Corsi.CodiceCorso == Esami.Corso).filter(Studenti.CodiceFiscale == cf).with_entities(Corsi.CodiceCorso, func.max(Esami.Data).label('max_data')).group_by(Corsi.CodiceCorso).subquery()
    risultatiesami_data = Studenti.query.join(Sostenuti, Studenti.CodiceFiscale == Sostenuti.Studente).join(Esami, Sostenuti.Esame == Esami.CodEsame).join(Corsi, Esami.Corso == Corsi.CodiceCorso).join(max_data, Corsi.CodiceCorso == max_data.c.CodiceCorso).filter(Sostenuti.Studente == cf).with_entities(Corsi.CodiceCorso, Corsi.NomeCorso,func.sum(((Sostenuti.voto)* (Esami.ValorePerc/100)).cast(Integer)).label('sommavoti'), max_data.c.max_data).group_by(Corsi.CodiceCorso, Corsi.NomeCorso, max_data.c.max_data)
    exam_list = [
        {
            "codice_corso": row.CodiceCorso,
            "nome_corso": row.NomeCorso,
            "voto": which_voto(row.sommavoti),
            "data_esame": row.max_data,   
        }
        for row in risultatiesami_data
    ]
    return exam_list

def get_all_course():
    query = db.session.query(Corsi,Appartenenti).join(Appartenenti,Corsi.CodiceCorso==Appartenenti.CodCorso).order_by(Appartenenti.Anno)
    results = query.all()
    all_course = []
    for row in results:
        dataC = {
            "codiceCorso": row[0].CodiceCorso,
            "nomeCorso": row[0].NomeCorso,
            "codiceCorsoLaurea": row[1].CorsoLaurea,
            "anno": row[1].Anno
        }
        all_course.append(dataC)
    
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
def checkdata(voto, data):
    print(voto)
    if voto == "" or voto == 'INSUF':
        return ""
    else: 
        return data

def show_list_exam_aux(cf):
    max_data = Corsi.query.join(Appartenenti, Corsi.CodiceCorso == Appartenenti.CodCorso).join(Esami, Corsi.CodiceCorso == Esami.Corso).filter(Studenti.CodiceFiscale == cf).with_entities(Corsi.CodiceCorso, func.max(Esami.Data).label('max_data')).group_by(Corsi.CodiceCorso).subquery()
    subquery = Esami.query.join(Sostenuti, Esami.CodEsame == Sostenuti.Esame).filter(and_(Sostenuti.Studente == cf, Sostenuti.voto != 'INSUF')).with_entities(Esami.Corso, Esami.Data, func.sum(((Sostenuti.voto)* (Esami.ValorePerc/100)).cast(Integer)).label('sommavoti')).group_by(Esami.Corso, Esami.Data)
    sub = subquery.subquery()

    exam_data = (db.session.query(Corsi, sub, max_data.c.max_data).join(Appartenenti, Corsi.CodiceCorso == Appartenenti.CodCorso).join(Studenti, Appartenenti.CorsoLaurea == Studenti.CorsoLaurea).outerjoin(sub, sub.c.Corso == Corsi.CodiceCorso).outerjoin(max_data, Corsi.CodiceCorso == max_data.c.CodiceCorso).filter(Studenti.CodiceFiscale == cf).with_entities(Corsi.CodiceCorso, Corsi.NomeCorso, max_data.c.max_data, func.sum(sub.c.sommavoti), Corsi.Valore).group_by(Corsi.CodiceCorso, Corsi.NomeCorso, max_data.c.max_data, Corsi.Valore))
    
    corsi = []
    for row in exam_data:
        data = {
            "CodiceCorso": row.CodiceCorso,
            "NomeCorso": row.NomeCorso,
            "Data": (row.max_data),
            "Voto": isNone(which_voto(row[3])),
            "Valore": isNone(row.Valore),
        }
        data["Data"] = checkdata(data["Voto"], data["Data"])
        corsi.append(data)
    return corsi

def accetta_get(cf):
    da_accettare = []
    dati = Sostenuti.query.join(Esami, Sostenuti.Esame == Esami.CodEsame).join(Corsi, Esami.Corso == Corsi.CodiceCorso).filter(Sostenuti.stato == 'DA RIVEDERE', Sostenuti.voto != 'INSUF', Sostenuti.Studente == cf).with_entities(Esami.CodEsame, Corsi.NomeCorso, Esami.Data, Sostenuti.voto)
    for row in dati:
        data = {
            "CodEsame": row.CodEsame,
            "NomeCorso": row.NomeCorso,
            "Data": row.Data,
            "voto": row.voto
        }
        da_accettare.append(data)
    return da_accettare

def accetta_post(data, cf):
    
    for item in data:
        #Studenti.query.filter_by(mail=email).update({"password": hash_value})
        Sostenuti.query.filter_by(Studente=cf, Esame=item["CodEsame"]).update({"stato": item["Azione"]})
    db.session.commit()

