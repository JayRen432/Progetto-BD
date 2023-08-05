from flask import Flask, render_template, request, redirect, session, jsonify
from classi import *


"""
la funzione is_cf_present_in_docenti riceve come parametro il codice fiscale dello studente e restituisce True se il codice fiscale è presente tra i docenti
@param cf_studente: codice fiscale dello studente
@param mysql: connessione al database
@return count > 0: True se il codice fiscale è presente tra i docenti, False altrimenti

"""


def is_cf_present_in_docenti(cf_studente, mysql):
    count = Docenti.query.filter_by(CodiceFiscale=cf_studente).count()
    return count > 0


"""
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

"""


def crea_esame_inserisci(
    corso, nome_esame, codice_esame, data, tipo, valore, cf_docente
):
    esami = Esami(
        Corso=corso,
        CodEsame=codice_esame,
        NomeEsame=nome_esame,
        Data=data,
        Tipo=tipo,
        Valore=valore,
        Docente=cf_docente,
    )
    db.session.add(esami)
    db.session.commit()


"""
la funzione crea_esame_docenti riceve come parametri la connessione al database e il codice fiscale del docente
@param mysql
@param cf_docente
@return lista_corsi
attraverso una query seleziona i dati dei corsi insegnati dal docente attraverso la SELECT e li inserisce in una lista di dizionari

"""


def crea_esame_docenti(cf_docente):
    query = (
        db.session.query(Insegna, Corsi)
        .join(Corsi, Insegna.CodCorso == Corsi.CodiceCorso)
        .filter(Insegna.CodFiscale == cf_docente)
    )
    course_data = query.all()
    lista_corsi = [
        {"CodiceCorso": row[1].CodiceCorso, "NomeCorso": row[1].NomeCorso}
        for row in course_data
    ]
    return lista_corsi


"""
la funzione assegna_voto_aux restituisce una lista di dizionari contenenti i dati degli studenti iscritti all'esame
riceve come parametri la connessione al database e il codice dell'esame
@param mysql
@param codiceEsame
@return studenti

"""


def assegna_voto_aux(codiceEsame):
    query = (
        db.session.query(Iscrizione_Appelli, Studenti)
        .join(Studenti, Iscrizione_Appelli.Studente == Studenti.CodiceFiscale)
        .filter_by(Iscrizione_Appelli.Esame == codiceEsame)
    )
    student_data = query.all()
    studenti = [
        {"matricola": row[1].matricola, "Nome": row[1].Nome, "Cognome": row[1].Cognome}
        for row in student_data
    ]
    session["matricola"] = studenti[0]["matricola"]
    return studenti


"""
la funzione elimina_esame_post riceve come parametri la connessione al database, il codice dell'esame e il codice fiscale del docente
i dati vengono eliminati dalla tabella esami attraverso la DELETE
@param mysql
@param esame
@param cf_docente

"""


def elimina_esame_post(esame, cf_docente):
    Esami.query.filter_by(CodEsame=esame, Docente=cf_docente).delete()
    db.session.commit()


"""
la funzione elimina_esame_get riceve come parametri la connessione al database e il codice fiscale del docente
attraverso una query seleziona i dati degli esami insegnati dal docente attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@param cf_docente
@return lista_esami

"""


def elimina_esame_get(cf_docente):
    exam_data = Esami.query.with_entities(
        Esami.CodEsame, Esami.Corso, Esami.Data, Esami.Tipo, Esami.Valore
    ).filter_by(Docente=cf_docente)

    lista_esami = [
        {
            "CodEsame": row.CodEsame,
            "Corso": row.Corso,
            "Data": row.Data,
            "Tipo": row.Tipo,
            "Valore": row.Valore,
        }
        for row in exam_data
    ]
    return lista_esami


"""
la funzione phone_number_aux riceve come parametri la connessione al database e il codice fiscale del docente
attraverso una query seleziona i dati dei numeri di telefono del docente attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@param cf_docente
@return phone_numbers

"""


def phone_number_aux(cf_docente):
    phone_numbers = []
    numbers_data = Numeri_Telefono.query.with_entities(
        Numeri_Telefono.NumTelefono
    ).filter_by(CodFiscale=cf_docente)
    phone_numbers = [row.NumTelefono for row in numbers_data]
    session["phone_numbers"] = phone_numbers
    return phone_numbers


"""
la funzione add_number_aux riceve come parametri la connessione al database, il numero di telefono e il codice fiscale del docente
i dati vengono inseriti nella tabella numeri_telefono attraverso la INSERT
@param mysql
@param number_to_add
@param cf_docente

"""


def add_number_aux(number_to_add, cf_docente):
    telefono = Numeri_Telefono(NumTelefono=number_to_add, CodFiscale=cf_docente)
    db.session.add(telefono)
    db.session.commit()


"""
la funzione delete_number_aux riceve come parametri la connessione al database, il numero di telefono e il codice fiscale del docente
i dati vengono eliminati dalla tabella numeri_telefono attraverso la DELETE
@param mysql
@param numero_telefono
@param cf_docente

"""


def delete_number_aux(numero_telefono, cf_docente):
    Numeri_Telefono.query.filter_by(
        NumTelefono=numero_telefono, CodFiscale=cf_docente
    ).delete()
    db.session.commit()


"""
la funzione ricevi_dati_aux riceve come parametri la connessione al database, il codice fiscale dello studente, il codice dell'esame e il voto
@param mysql
@param cf
@param codiceEsame
@param voto
i dati vengono inseriti nella tabella sostenuti attraverso la INSERT
"""


def ricevi_dati_aux(cf, codiceEsame, voto):
    sostenuti = Sostenuti(Esame=codiceEsame, Studente=cf, voto=voto)
    db.session.add(sostenuti)
    db.session.commit()


"""
la funzione take_cf riceve come parametri la connessione al database e la matricola dello studente
@param mysql
@param matr
@return student

"""


def take_cf(matr):
    student = Studenti.query.with_entities(Studenti.CodiceFiscale).filter_by(
        matricola=matr
    )
    return student


"""
la funzione tabella_esame riceve come parametri la connessione al database e attraverso 
una query seleziona i dati degli esami attraverso la SELECT e li inserisce in una lista di dizionari
@param mysql
@return esami

"""


def tabella_esami():
    cf_docente = session.get("codicefiscale")

    subquery_sostenuti = (
        db.session.query(Sostenuti.Esame, db.func.count("*").label("num_sostenuti"))
        .group_by(Sostenuti.Esame)
        .subquery()
    )
    subquery_iscrizioni = (
        db.session.query(
            Iscrizione_Appelli.Esame, db.func.count("*").label("num_iscrizioni")
        )
        .group_by(Iscrizione_Appelli.Esame)
        .subquery()
    )

    rows = (
        db.session.query(Esami.CodEsame, Esami.Corso, Esami.Data, Esami.Tipo)
        .outerjoin(subquery_sostenuti, Esami.CodEsame == subquery_sostenuti.c.Esame)
        .outerjoin(subquery_iscrizioni, Esami.CodEsame == subquery_iscrizioni.c.Esame)
        .filter(
            Esami.Docente == cf_docente,
            subquery_sostenuti.c.num_sostenuti < subquery_iscrizioni.c.num_iscrizioni,
            db.or_(
                subquery_sostenuti.c.num_sostenuti == None,
                subquery_iscrizioni.c.num_iscrizioni > 0,
            ),
            db.and_(
                subquery_sostenuti.c.num_sostenuti == 0,
                subquery_iscrizioni.c.num_iscrizioni > 0,
            ),
        )
    )
    esami = []

    if rows:
        for row in rows:
            esame = {
                "CodEsame": row.CodEsame,
                "Corso": row.Corso,
                "Data": str(row.Data),
                "Tipo": row.Tipo,
            }
            esami.append(esame)

    return esami
