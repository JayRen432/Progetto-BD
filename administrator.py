import pymysql
import json
import hashlib


def add_degree_course_aux(cod_corso, nome_corso, spec, indirizzo, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO corsi_di_laurea(CodCorsoLaurea, NomeCorsoLaurea,Specializzazione,indirizzo) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (cod_corso, nome_corso, spec, indirizzo))
    mysql.commit()
    cursor.close()


def get_degree_course(mysql):
    corsi = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM Corsi_di_Laurea'
    cursor.execute(query)
    rows = cursor.fetchall()

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


def delete_degree_course_aux_post(codice_corso, mysql):
    delete_corso_crosoLaurea_aux_post(codice_corso, None, mysql)
    cursor = mysql.cursor()
    query = 'DELETE FROM Corsi_di_laurea WHERE CodCorsoLaurea = %s'
    cursor.execute(query, (codice_corso,))
    mysql.commit()
    cursor.close()


def add_course_aux(codice, nome, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO corsi(CodiceCorso, NomeCorso) VALUES (%s, %s)'
    cursor.execute(query, (codice, nome))
    mysql.commit()
    cursor.close()


def delete_course_aux_post(codice_corso, mysql):
    delete_corso_crosoLaurea_aux_post(None, codice_corso, mysql)
    cursor = mysql.cursor()
    query = 'DELETE FROM corsi WHERE CodiceCorso = %s'
    cursor.execute(query, (codice_corso,))
    mysql.commit()
    cursor.close()


def get_couse(mysql):
    corsi = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM corsi'
    cursor.execute(query)
    rows = cursor.fetchall()

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


def assegnaCorsoCorsoLaurea_aux(corso_laurea, corso, anno, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO appartenenti(CorsoLaurea, CodCorso, Anno) VALUES (%s, %s, %s)'
    cursor.execute(query, (corso_laurea, corso, anno))
    mysql.commit()
    cursor.close()


def add_docente_aux(doc, mysql):
    pwd = doc['password']
    hash_password = hashlib.sha256(pwd.encode('utf-8'))
    hash_value=hash_password.hexdigest()
    cursor = mysql.cursor()
    query = 'INSERT INTO docenti(CodiceFiscale, Nome, Cognome, mail, annoNascita, password) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (doc['codice_fiscale'], doc['nome'],
                           doc['cognome'], doc['mail'], doc['anno_nascita'], hash_value))
    mysql.commit()
    cursor.close()


def delete_docenti_aux(codice_fiscale, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM docenti WHERE CodiceFiscale = %s'
    cursor.execute(query, codice_fiscale)
    mysql.commit()
    cursor.close()


def get_docenti(mysql):
    docenti = []
    cursor = mysql.cursor()
    query = 'SELECT CodiceFiscale, Nome, Cognome, mail, annoNascita FROM docenti'
    cursor.execute(query)
    rows = cursor.fetchall()

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


def get_couse_degree_course(mysql):
    dettagli = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM appartenenti'
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        info = {
            'CorsoLaurea': row[0],
            'CodCorso': row[1],
        }
        dettagli.append(info)
    mysql.commit()
    cursor.close()
    return dettagli


def delete_corso_crosoLaurea_aux_post(deg_course, course, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM appartenenti WHERE CodCorso = %s AND CorsoLaurea = %s'
    cursor.execute(query, (deg_course, course))
    mysql.commit()
    cursor.close()


def assegna_Corso_Docente_aux(docente, corso, data, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO aperto(CodCorso, CodFiscale, DataApertura) VALUES (%s, %s, %s)'
    cursor.execute(query, (corso, docente, data))
    mysql.commit()
    cursor.close()


def get_temporaryuser(mysql):
    user = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM temporaryuser'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
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


def delete_tempuser(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM temporaryuser WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()


def add_user(stud, mysql):
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


def get_studenti(mysql):
    users = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM studenti'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
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


def delete_aux(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM studenti WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()


def get_couse_docenti(mysql):
    data = []
    cursor = mysql.cursor()
    query = 'SELECT * FROM aperto'
    cursor.execute(query)

    # Retrieve the results
    rows = cursor.fetchall()
    for row in rows:
        info = {
            'Corso': row[0],
            'Docente': row[1]
        }
        data.append(info)
    mysql.commit()
    cursor.close()
    return data


def delete_corso_Docente_aux(doc_cf, code_course,mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM aperto WHERE CodCorso = %s AND CodFiscale = %s'
    cursor.execute(query, (code_course, doc_cf))
    mysql.commit()
    cursor.close()