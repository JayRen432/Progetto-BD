import hashlib
from studenti import *
from classi import *

"""
la funzione add_degree_course_aux riceve come parametro il codice del corso di laurea, il nome del corso di laurea, 
la specializzazione e l'indirizzo e aggiunge il corso di laurea attraverso la INSERT
@param cod_corso: codice del corso di laurea
@param nome_corso: nome del corso di laurea
@param spec: specializzazione del corso di laurea
@param indirizzo: indirizzo del corso di laurea
@param mysql: connessione al database
"""


def add_degree_course_aux(cod_corso, nome_corso, spec, indirizzo):
    corso_laurea = Corsi_di_Laurea(
        CodCorsoLaurea=cod_corso,
        NomeCorsoLaurea=nome_corso,
        Specializzazione=spec,
        indirizzo=indirizzo,
    )
    db.session.add(corso_laurea)
    db.session.commit()


"""
la funzione get_degree_course riceve come parametro la connessione al database e restituisce tutti i corsi di laurea
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return corsi: lista dei corsi di laurea
"""


def get_degree_course():
    corsi = []
    rows = Corsi_di_Laurea.query.all()
    if rows:
        for row in rows:
            codice = row.CodCorsoLaurea
            nome = row.NomeCorsoLaurea
            specializzazione = row.Specializzazione
            indirizzo = row.indirizzo
            corso_info = {
                "codice": codice,
                "nome": nome,
                "specializzazione": specializzazione,
                "indirizzo": indirizzo,
            }
            corsi.append(corso_info)

    return corsi


"""
la funzione delete_degree_course_aux_post riceve come parametro il codice del corso di laurea da eliminare
e lo elimina attraverso la DELETE
@param codice_corso: codice del corso di laurea da eliminare
@param mysql: connessione al database
vedere delete_corso_corsoLaurea_aux_post per ulteriori dettagli
"""


def delete_degree_course_aux_post(codice_corso):
    delete_corso_corsoLaurea_aux_post(codice_corso, None)
    Corsi_di_Laurea.query.filter_by(CodCorsoLaurea=codice_corso).delete()
    db.session.commit()


"""
la funzione add_course_aux riceve come parametro il codice del corso, il nome del corso e aggiunge il corso attraverso la INSERT
@param codice: codice del corso
@param nome: nome del corso
@param mysql: connessione al database
"""


def add_course_aux(codice, nome):
    corso = Corsi(CodiceCorso=codice, NomeCorso=nome)
    db.session.add(corso)
    db.session.commit()


"""
la funzione delete_course_aux_post riceve come parametro il codice del corso da eliminare
e lo elimina attraverso la DELETE
@param codice_corso: codice del corso da eliminare
@param mysql: connessione al database
vedere delete_corso_corsoLaurea_aux_post per ulteriori dettagli
"""


def delete_course_aux_post(codice_corso):
    delete_corso_corsoLaurea_aux_post(None, codice_corso)
    Corsi.query.filter_by(CodiceCorso=codice_corso).delete()
    db.session.commit()


"""
la funzione get_course riceve come parametro la connessione al database e restituisce tutti i corsi
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return corsi: lista dei corsi
"""


def get_course():
    corsi = []
    rows = Corsi.query.all()
    if rows:
        for row in rows:
            corso_info = {
                "codice": row.CodiceCorso,
                "nome": row.NomeCorso,
            }
            corsi.append(corso_info)

    return corsi


"""
la funzione add_corso_corsoLaurea_aux riceve come parametro il codice del corso di laurea, il codice del corso e l'anno di insegnamento
e aggiunge il corso attraverso la INSERT
@param corso_laurea: codice del corso di laurea
@param corso: codice del corso
@param anno: anno di insegnamento
@param mysql: connessione al database

"""


def assegnaCorsoCorsoLaurea_aux(corso_laurea, corso, anno):
    appart = Appartenenti(CorsoLaurea=corso_laurea, CodCorso=corso, Anno=anno)
    db.session.add(appart)
    db.session.commit()


"""
la funzione add_docente_aux riceve come parametro i dati del docente contenuti in doc e aggiunge il docente attraverso la INSERT
@param doc: dati del docente
@param mysql: connessione al database
si controlla che il codice fiscale non sia già presente tra gli studenti

"""


def add_docente_aux(doc):
    pwd = doc["password"]
    hash_password = hashlib.sha256(pwd.encode("utf-8"))
    hash_value = hash_password.hexdigest()

    codicefiscale = doc["codice_fiscale"]

    if is_cf_present_in_studenti(codicefiscale):
        raise ValueError("Codice fiscale già presente tra gli studenti")

    docente = Docenti(
        CodiceFiscale=doc["codice_fiscale"],
        Nome=doc["nome"],
        Cognome=doc["cognome"],
        mail=doc["mail"],
        annoNascita=doc["anno_nascita"],
        password=hash_value,
    )

    db.session.add(docente)
    db.session.commit()


"""
la funzione delete_docenti_aux riceve come parametro il codice fiscale del docente da eliminare
e lo elimina attraverso la DELETE
@param codice_fiscale: codice fiscale del docente da eliminare
@param mysql: connessione al database

"""


def delete_docenti_aux(codice_fiscale):
    Docenti.query.filter_by(CodiceFiscale=codice_fiscale).delete()
    db.session.commit()


"""
la funzione get_docenti riceve come parametro la connessione al database e restituisce tutti i docenti  
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return docenti: lista dei docenti

"""


def get_docenti():
    docenti = []
    rows = Docenti.query.with_entities(
        Docenti.CodiceFiscale,
        Docenti.Nome,
        Docenti.Cognome,
        Docenti.mail,
        Docenti.annoNascita,
    )
    if rows:
        for row in rows:
            doc_info = {
                "codice_fiscale": row.CodiceFiscale,
                "nome": row.Nome,
                "cognome": row.Cognome,
                "mail": row.mail,
                "anno_di_nascita": row.annoNascita,
            }
            docenti.append(doc_info)
    return docenti


def is_valid_mail(matricola, mail):
    valid_mail = matricola + "@stud.unive.it"
    return mail == valid_mail


"""
la funzione get_course_degree_course riceve come parametro la connessione al database e restituisce tutti i corsi di laurea e i corsi
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return dettagli: lista dei corsi di laurea e dei corsi

"""


def get_course_degree_course():
    dettagli = []
    rows = Appartenenti.query.all()
    if rows:
        for row in rows:
            info = {
                "CorsoLaurea": row.CorsoLaurea,
                "CodCorso": row.CodCorso,
            }
            dettagli.append(info)
    return dettagli


"""
la funzione delete_corso_corsoLaurea_aux_post riceve come parametro il codice del corso di laurea e il codice del corso
e li elimina attraverso la DELETE
@param deg_course: codice del corso di laurea
@param course: codice del corso
@param mysql: connessione al database

"""


def delete_corso_corsoLaurea_aux_post(deg_course, course):
    Appartenenti.query.filter_by(CorsoLaurea=deg_course, CodCorso=course).delete()
    db.session.commit()


"""
la funzione assegna_Corso_Docente_aux riceve come parametro il codice fiscale del docente e il codice del corso
e li aggiunge attraverso la INSERT
@param docente: codice fiscale del docente
@param corso: codice del corso
@param mysql: connessione al database

"""


def assegna_Corso_Docente_aux(docente, corso):
    doc_ins = Insegna(CodCorso=corso, CodFiscale=docente)
    db.session.add(doc_ins)
    db.session.commit()


"""
la funzione get_temporaryuser riceve come parametro la connessione al database e restituisce tutti gli studenti
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return user: lista degli studenti

"""


def get_temporaryuser():
    users = []
    rows = TemporaryUser.query.all()

    # Retrieve the results

    if rows:
        for row in rows:
            info = {
                "codiceFiscale": row.CodiceFiscale,
                "nome": row.Nome,
                "cognome": row.Cognome,
                "mail": row.mail,
                "annoNascita": row.annoNascita,
                "matricola": row.matricola,
                "password": row.password,
                "CorsoLaurea": row.CorsoLaurea,
            }
            users.append(info)
    return users


"""
la funzione delete_tempuser riceve come parametro il codice fiscale dello studente da eliminare
e lo elimina attraverso la DELETE
@param cf: codice fiscale dello studente da eliminare
@param mysql: connessione al database

"""


def delete_tempuser(cf):
    TemporaryUser.query.filter_by(CodiceFiscale=cf).delete()
    db.session.commit()


"""
la funzione add_user riceve come parametro lo studente da aggiungere e lo aggiunge attraverso la INSERT
@param stud: studente da aggiungere
@param mysql: connessione al database
vengono fatti dei controlli sulla matricola, sulla mail e sul codice fiscale
se i controlli sono corretti viene eseguita la INSERT

"""


def add_user(stud):
    studente = Studenti(
        CodiceFiscale=stud["codice_fiscale"],
        Nome=stud["nome"],
        Cognome=stud["cognome"],
        annoNascita=stud["annoNascita"],
        mail=stud["mail"],
        matricola=stud["matricola"],
        password=stud["password"],
        CorsoLaurea=stud["corso_laurea"],
    )
    db.session.add(studente)
    db.session.commit()


"""
la funzione get_studenti riceve come parametro la connessione al database e restituisce tutti gli studenti
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return users: lista degli studenti

"""


def get_studenti():
    users = []
    rows = Studenti.query.all()
    if rows:
        for row in rows:
            info = {
                "codiceFiscale": row.CodiceFiscale,
                "nome": row.Nome,
                "cognome": row.Cognome,
                "mail": row.mail,
                "annoNascita": row.annoNascita,
                "matricola": row.matricola,
                "password": row.password,
                "CorsoLaurea": row.CorsoLaurea,
            }
            users.append(info)
    return users


"""
la funzione delete_aux riceve come parametro il codice fiscale dello studente da eliminare 
e lo elimina attraverso la DELETE
@param cf: codice fiscale dello studente da eliminare
@param mysql: connessione al database

"""


def delete_aux(cf):
    Studenti.query.filter_by(CodiceFiscale=cf).delete()
    db.session.commit()


"""
la funzione get_course_docenti riceve come parametro la connessione al database e restituisce tutti i corsi e i docenti
che insegnano quel corso attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return data: lista dei corsi e dei docenti

"""


def get_course_docenti():
    data = []
    rows = Insegna.query.all()
    if rows:
        for row in rows:
            info = {"Corso": row.CodCorso, "Docente": row.CodFiscale}
            data.append(info)
    return data


"""
la funzione delete_corso_Docente_aux riceve come parametro il codice fiscale del docente e il codice del corso da eliminare
e li elimina attraverso la DELETE
@param doc_cf: codice fiscale del docente
@param code_course: codice del corso da eliminare
@param mysql: connessione al database

"""


def delete_corso_Docente_aux(doc_cf, code_course):
    Insegna.query.filter_by(CodCorso=code_course, CodFiscale=doc_cf).delete()
    db.session.commit()
