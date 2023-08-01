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

def is_cf_present_in_studenti(cf_docente, mysql):
    cursor = mysql.cursor()
    query = "SELECT COUNT(*) FROM Studenti WHERE CodiceFiscale = %s"
    cursor.execute(query, (cf_docente,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def add_docente_aux(doc, mysql):
    pwd = doc['password']
    hash_password = hashlib.sha256(pwd.encode('utf-8'))
    hash_value=hash_password.hexdigest()
    cursor = mysql.cursor()
    codicefiscale = doc['codice_fiscale']
    if not doc['mail'].lower().endswith("@unive.it"):
        cursor.close()
        raise ValueError("L'email del docente deve terminare con '@unive.it'.")

    if is_cf_present_in_studenti(codicefiscale, mysql):
        cursor.close()
        raise ValueError("Codice fiscale già presente tra gli studenti")

    if not is_valid_codicefiscale(codicefiscale) or len(codicefiscale) != 16:
        raise ValueError("Il Codice Fiscale non è del formato giusto.")

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


def delete_corso_crosoLaurea_aux_post(deg_course, course, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM appartenenti WHERE CodCorso = %s AND CorsoLaurea = %s'
    cursor.execute(query, (deg_course, course))
    mysql.commit()
    cursor.close()


def assegna_Corso_Docente_aux(docente, corso, mysql):
    cursor = mysql.cursor()
    query = 'INSERT INTO insegna(CodCorso, CodFiscale) VALUES (%s, %s)'
    cursor.execute(query, (corso, docente))
    mysql.commit()
    cursor.close()


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


def delete_tempuser(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM temporaryuser WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()


def add_user(stud, mysql):
    cursor = mysql.cursor()
    if not is_valid_mail(stud['matricola'], stud['mail']):
        cursor.close()
        raise Exception("Mail non valida")

    matricola = stud['matricola']
    if not matricola.isdigit() or len(matricola) != 6:
        cursor.close()
        raise ValueError("La matricola deve contenere esattamente 6 cifre.")
    
    last_matricola_query = 'SELECT matricola FROM Studenti ORDER BY matricola DESC LIMIT 1'
    cursor.execute(last_matricola_query)
    last_matricola_row = cursor.fetchone()
    if last_matricola_row:
        last_matricola = last_matricola_row[0]
        current_matricola = stud['matricola']
        if current_matricola != last_matricola+str(1):
            cursor.close()
            raise ValueError("La matricola non è inserita in ordine. Assicurarsi che la matricola sia maggiore dell'ultima matricola inserita.")

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


def delete_aux(cf, mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM studenti WHERE CodiceFiscale = %s '
    cursor.execute(query, cf)
    mysql.commit()
    cursor.close()


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


def delete_corso_Docente_aux(doc_cf, code_course,mysql):
    cursor = mysql.cursor()
    query = 'DELETE FROM insegna WHERE CodCorso = %s AND CodFiscale = %s'
    cursor.execute(query, (code_course, doc_cf))
    mysql.commit()
    cursor.close()
