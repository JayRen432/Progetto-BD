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
