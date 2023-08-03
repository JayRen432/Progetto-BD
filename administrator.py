import pymysql
import json
import hashlib
from studenti import *

'''
la funzione add_degree_course_aux riceve come parametro il codice del corso di laurea, il nome del corso di laurea, 
la specializzazione e l'indirizzo e aggiunge il corso di laurea attraverso la INSERT
@param cod_corso: codice del corso di laurea
@param nome_corso: nome del corso di laurea
@param spec: specializzazione del corso di laurea
@param indirizzo: indirizzo del corso di laurea
@param mysql: connessione al database
'''
def add_degree_course_aux(cod_corso, nome_corso, spec, indirizzo, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO corsi_di_laurea(CodCorsoLaurea, NomeCorsoLaurea,Specializzazione,indirizzo) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (cod_corso, nome_corso, spec, indirizzo))
    mysql.commit()
    cursor.close()

'''
la funzione get_degree_course riceve come parametro la connessione al database e restituisce tutti i corsi di laurea
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return corsi: lista dei corsi di laurea
'''
def get_degree_course(mysql):
    corsi = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM Corsi_di_Laurea'
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            codice = row[0]
            nome = row[1]
            specializzazione = row[2]
            indirizzo = row[3]
            corso_info = {
                'codice': codice,
                'nome': nome,
                'specializzazione': specializzazione,
                'indirizzo': indirizzo
            }
            corsi.append(corso_info)
    mysql.commit()
    cursor.close()
    return corsi

'''
la funzione delete_degree_course_aux_post riceve come parametro il codice del corso di laurea da eliminare
e lo elimina attraverso la DELETE
@param codice_corso: codice del corso di laurea da eliminare
@param mysql: connessione al database
vedere delete_corso_corsoLaurea_aux_post per ulteriori dettagli
'''
def delete_degree_course_aux_post(codice_corso, mysql):
    delete_corso_corsoLaurea_aux_post(codice_corso, None, mysql)
    cursor = mysql.cursor()
    query = 'DELETE FROM Corsi_di_laurea WHERE CodCorsoLaurea = %s'
    cursor.execute(query, (codice_corso,))
    mysql.commit()
    cursor.close()

'''
la funzione add_course_aux riceve come parametro il codice del corso, il nome del corso e aggiunge il corso attraverso la INSERT
@param codice: codice del corso
@param nome: nome del corso
@param mysql: connessione al database

'''
def add_course_aux(codice, nome, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO corsi(CodiceCorso, NomeCorso) VALUES (%s, %s)'
    cursor.execute(query, (codice, nome))
    mysql.commit()
    cursor.close()

'''
la funzione delete_course_aux_post riceve come parametro il codice del corso da eliminare
e lo elimina attraverso la DELETE
@param codice_corso: codice del corso da eliminare
@param mysql: connessione al database
vedere delete_corso_corsoLaurea_aux_post per ulteriori dettagli
'''
def delete_course_aux_post(codice_corso, mysql):
    delete_corso_corsoLaurea_aux_post(None, codice_corso, mysql)
    cursor = mysql.cursor()
    query = 'DELETE FROM corsi WHERE CodiceCorso = %s'
    cursor.execute(query, (codice_corso,))
    mysql.commit()
    cursor.close()

'''
la funzione get_couse riceve come parametro la connessione al database e restituisce tutti i corsi
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return corsi: lista dei corsi

'''
def get_couse(mysql):
    corsi = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM corsi'
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            codice = row[0]
            nome = row[1]
            corso_info = {
                'codice': codice,
                'nome': nome,
            }
            corsi.append(corso_info)
    mysql.commit()
    cursor.close()
    return corsi

'''
la funzione add_corso_corsoLaurea_aux riceve come parametro il codice del corso di laurea, il codice del corso e l'anno di insegnamento
e aggiunge il corso attraverso la INSERT
@param corso_laurea: codice del corso di laurea
@param corso: codice del corso
@param anno: anno di insegnamento
@param mysql: connessione al database

'''
def assegnaCorsoCorsoLaurea_aux(corso_laurea, corso, anno, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO appartenenti(CorsoLaurea, CodCorso, Anno) VALUES (%s, %s, %s)'
    cursor.execute(query, (corso_laurea, corso, anno))
    mysql.commit()
    cursor.close()

'''
la funzione add_docente_aux riceve come parametro i dati del docente contenuti in doc e aggiunge il docente attraverso la INSERT
@param doc: dati del docente
@param mysql: connessione al database
si controlla che il codice fiscale non sia già presente tra gli studenti
'''
def add_docente_aux(doc, mysql):
    pwd = doc['password']
    hash_password = hashlib.sha256(pwd.encode('utf-8'))
    hash_value=hash_password.hexdigest()
    cursor = mysql.cursor()
    codicefiscale = doc['codice_fiscale']

    if is_cf_present_in_studenti(codicefiscale, mysql):
        cursor.close()
        raise ValueError("Codice fiscale già presente tra gli studenti")

    query = 'INSERT INTO docenti(CodiceFiscale, Nome, Cognome, mail, annoNascita, password) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (doc['codice_fiscale'], doc['nome'],
                           doc['cognome'], doc['mail'], doc['anno_nascita'], hash_value))
    mysql.commit()
    cursor.close()

'''
la funzione delete_docenti_aux riceve come parametro il codice fiscale del docente da eliminare
e lo elimina attraverso la DELETE
@param codice_fiscale: codice fiscale del docente da eliminare
@param mysql: connessione al database

'''
def delete_docenti_aux(codice_fiscale, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM docenti WHERE CodiceFiscale = %s'
    cursor.execute(query, codice_fiscale)
    mysql.commit()
    cursor.close()

'''
la funzione get_docenti riceve come parametro la connessione al database e restituisce tutti i docenti  
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return docenti: lista dei docenti

'''
def get_docenti(mysql):
    docenti = []
    cursor = mysql.cursor()
    query = 'SELECT CodiceFiscale, Nome, Cognome, mail, annoNascita FROM docenti'
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            doc_info = {
                'codice_fiscale': row[0],
                'nome': row[1],
                'cognome': row[2],
                'mail': row[3],
                'anno_di_nascita': row[4]
            }
            docenti.append(doc_info)
    mysql.commit()
    cursor.close()
    return docenti


def is_valid_mail(matricola, mail):
    valid_mail = matricola + "@stud.unive.it"
    return mail == valid_mail

'''
la funzione get_couse_degree_course riceve come parametro la connessione al database e restituisce tutti i corsi di laurea e i corsi
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return dettagli: lista dei corsi di laurea e dei corsi

'''
def get_couse_degree_course(mysql):
    dettagli = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM appartenenti'
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            info = {
                'CorsoLaurea': row[0],
                'CodCorso': row[1],
            }
            dettagli.append(info)
    mysql.commit()
    cursor.close()
    return dettagli

'''
la funzione delete_corso_corsoLaurea_aux_post riceve come parametro il codice del corso di laurea e il codice del corso
e li elimina attraverso la DELETE
@param deg_course: codice del corso di laurea
@param course: codice del corso
@param mysql: connessione al database

'''
def delete_corso_corsoLaurea_aux_post(deg_course, course, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM appartenenti WHERE CorsoLaurea = %s AND CodCorso = %s'
    cursor.execute(query, (deg_course, course))
    mysql.commit()
    cursor.close()

'''
la funzione assegna_Corso_Docente_aux riceve come parametro il codice fiscale del docente e il codice del corso
e li aggiunge attraverso la INSERT
@param docente: codice fiscale del docente
@param corso: codice del corso
@param mysql: connessione al database

'''
def assegna_Corso_Docente_aux(docente, corso, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO insegna(CodCorso, CodFiscale) VALUES (%s, %s)'
    cursor.execute(query, (corso, docente))
    mysql.commit()
    cursor.close()


'''
la funzione get_temporaryuser riceve come parametro la connessione al database e restituisce tutti gli studenti
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return user: lista degli studenti
'''
def get_temporaryuser(mysql):
    user = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM temporaryuser'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            info = {
                'codiceFiscale': row[0],
                'nome': row[1],
                'cognome': row[2],
                'mail': row[3],
                'annoNascita': row[4],
                'matricola': row[5],
                'password': row[6],
                'CorsoLaurea': row[7]
            }
            user.append(info)
    mysql.commit()
    cursor.close()
    return user

'''
la funzione delete_tempuser riceve come parametro il codice fiscale dello studente da eliminare
e lo elimina attraverso la DELETE
@param cf: codice fiscale dello studente da eliminare
@param mysql: connessione al database

'''
def delete_tempuser(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM temporaryuser WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()

'''
la funzione add_user riceve come parametro lo studente da aggiungere e lo aggiunge attraverso la INSERT
@param stud: studente da aggiungere
@param mysql: connessione al database
vengono fatti dei controlli sulla matricola, sulla mail e sul codice fiscale
se i controlli sono corretti viene eseguita la INSERT
'''
def add_user(stud, mysql):
    cursor = mysql.cursor()
    cursor = mysql.cursor()
    query = 'INSERT INTO Studenti VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (stud['codice_fiscale'],
                        stud['nome'],
                        stud['cognome'],
                        stud['mail'],
                        stud['annoNascita'],
                        stud['matricola'],
                        stud['password'],
                        stud['corso_laurea']
                        ))
    mysql.commit()
    cursor.close()


'''
la funzione get_studenti riceve come parametro la connessione al database e restituisce tutti gli studenti
attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return users: lista degli studenti

'''
def get_studenti(mysql):
    users = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM studenti'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            info = {
                'codiceFiscale': row[0],
                'nome': row[1],
                'cognome': row[2],
                'mail': row[3],
                'annoNascita': row[4],
                'matricola': row[5],
                'password': row[6],
                'CorsoLaurea': row[7]
            }
            users.append(info)
    mysql.commit()
    cursor.close()
    return users

'''
la funzione delete_aux riceve come parametro il codice fiscale dello studente da eliminare 
e lo elimina attraverso la DELETE
@param cf: codice fiscale dello studente da eliminare
@param mysql: connessione al database
'''
def delete_aux(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM studenti WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()

'''
la funzione get_couse_docenti riceve come parametro la connessione al database e restituisce tutti i corsi e i docenti
che insegnano quel corso attraverso un ciclo for che scorre tutte le righe della tabella
@param mysql: connessione al database
@return data: lista dei corsi e dei docenti

'''
def get_couse_docenti(mysql):
    data = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM insegna'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            info = {
                'Corso': row[0],
                'Docente': row[1]
            }
            data.append(info)
    mysql.commit()
    cursor.close()
    return data

'''
la funzione delete_corso_Docente_aux riceve come parametro il codice fiscale del docente e il codice del corso da eliminare
e li elimina attraverso la DELETE
@param doc_cf: codice fiscale del docente
@param code_course: codice del corso da eliminare
@param mysql: connessione al database

'''
def delete_corso_Docente_aux(doc_cf, code_course,mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM insegna WHERE CodCorso = %s AND CodFiscale = %s'
    cursor.execute(query, (code_course, doc_cf))
    mysql.commit()
    cursor.close()
