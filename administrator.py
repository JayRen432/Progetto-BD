import pymysql
import json
import bcrypt


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
    hash_password = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
    cursor = mysql.cursor()
    query = 'INSERT INTO docenti(CodiceFiscale, Nome, Cognome, mail, annoNascita, password) VALUES (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (doc['codice_fiscale'], doc['nome'],
                           doc['cognome'], doc['mail'], doc['anno_nascita'], hash_password))
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
    if (deg_course is not None) and (course is not None):
        query = 'DELETE FROM appartenenti WHERE CodCorso = %s AND CorsoLaurea = %s'
        cursor.execute(query, (deg_course, course))
    elif (deg_course is None) and (course is not None):
        query = 'DELETE FROM appartenenti WHERE CodCorso = %s'
        cursor.execute(query, course)
    elif (deg_course is not None) and (course is None):
        query = 'DELETE FROM appartenenti WHERE CorsoLaurea = %s'
        cursor.execute(query, deg_course)

    mysql.commit()
    cursor.close()
