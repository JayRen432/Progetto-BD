from flask import Flask, render_template, request, redirect, session, jsonify
import pymysql
import json
import bcrypt

# Create Flask Instance
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sf35dkn@!'
app.config['MYSQL_DATABASE_DB'] = 'progettobasi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = pymysql.connect(
    host=app.config['MYSQL_DATABASE_HOST'],
    user=app.config['MYSQL_DATABASE_USER'],
    password=app.config['MYSQL_DATABASE_PASSWORD'],
    db=app.config['MYSQL_DATABASE_DB']
)

users = ['Utente 1', 'Utente 2', 'Utente 3']
righe_uniche = []
righe_iniziali = [
    {"codice_corso": "ABC123", "nome_corso": "Corso A", "data_esame": "2023-07-20", "aula": "Aula 1"},
    {"codice_corso": "DEF456", "nome_corso": "Corso B", "data_esame": "2023-07-25", "aula": "Aula 2"},
]
corsi_di_laurea = []
corsi = []
docenti = [
    {'codice_fiscale': 'ABC123', 'nome': 'Mario', 'cognome': 'Rossi', 'mail': 'mario.rossi@example.com',
     'anno_di_nascita': 1985},
    {'codice_fiscale': 'DEF456', 'nome': 'Paola', 'cognome': 'Verdi', 'mail': 'paola.verdi@example.com',
     'anno_di_nascita': 1990},
    {'codice_fiscale': 'GHI789', 'nome': 'Luigi', 'cognome': 'Bianchi', 'mail': 'luigi.bianchi@example.com',
     'anno_di_nascita': 1980}
]


@app.route('/')
def index():
    elenco_corsi_scientifici = ["Informatica", "Scienze Ambientali", "Chimica e tecnologie sostenibili",
                                "Ingegneria Fisica", "Scienze e tecnologie per i beni culturali"]
    elenco_corsi_umanistici = ["Lettere", "Filosofia", "Storia",
                               "Conservazione e gestione dei beni e delle attività culturali"]
    elenco_corsi_economici = ["Commercio estero e turismo", "Digital Management", "Economia aziendale",
                              "Economia e commercio"]
    elenco_corsi_lingua = ["Lingue, civiltà e scienze del linguaggio",
                           "Lingue, culture e società dell'Asia e dell'Africa mediterranea"]
    return render_template("index.html",
                           elenco_corsi_scientifici=elenco_corsi_scientifici,
                           elenco_corsi_economici=elenco_corsi_economici,
                           elenco_corsi_umanistici=elenco_corsi_umanistici,
                           elenco_corsi_lingua=elenco_corsi_lingua)


@app.route('/reset_pwd', methods=['GET', 'POST'])
def resetpwd():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        if password == confirm_password:
            hash_password = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt())
            cursor = mysql.cursor()
            query = 'UPDATE temporaryuser SET password = %s WHERE mail = %s'
            cursor.execute(query, (hash_password, email))
            mysql.commit()
            cursor.close()
            return redirect('/login')
    return render_template("reset_pwd.html")


# localhost:5000/sign_up
# localhost:5000/sign_up
@app.route('/sign_up', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        codicefiscale = request.form['Codicefiscale']
        name = request.form['Nome']
        surname = request.form['Cognome']
        dateofbirth = request.form['AnnoNascita']
        email = request.form['Email']
        password = request.form['password']

        hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = mysql.cursor()
        query = 'INSERT INTO temporaryuser(codicefiscale, nome, cognome, annoNascita, mail, matricola, password) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query, (codicefiscale, name, surname, dateofbirth, email, "000000", hash_password))
        mysql.commit()
        cursor.close()

        return redirect('/login')

    return render_template("sign_up.html")


# localhost:5000/login
@app.route('/login')
def login():
    return render_template("login.html")


# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


@app.route('/user_data')
def home():
    # Dati utente di esempio
    codice_fiscale = 'ABC123'
    nome = 'Mario'
    cognome = 'Rossi'
    email = 'mario@example.com'
    anno_nascita = '1990'
    ruolo = 'Studente'

    return render_template('info_utente.html', codice_fiscale=codice_fiscale, nome=nome, cognome=cognome, mail=email,
                           anno_nascita=anno_nascita, ruolo=ruolo)


@app.route('/esami', methods=['GET', 'POST'])
def esami():
    corso_di_laurea = request.form.get('corso_di_laurea')

    # Dati degli esami di esempio
    esami = {
        'informatica': {
            'Primo anno': ['Matematica', 'Programmazione e laboratorio', 'Architettura dei calcolatori'],
            'Secondo anno': ['Algoritmi e strutture dati', 'Basi di dati', 'Reti di calcolatori'],
            'Terzo anno': ['Intelligenza artificiale', 'Sistemi distribuiti', 'Sicurezza informatica']
        },
        'ingegneria': {
            'Primo anno': ['Matematica', 'Fisica', 'Chimica'],
            'Secondo anno': ['Meccanica', 'Elettrotecnica', 'Materiali'],
            'Terzo anno': ['Termodinamica', 'Ingegneria dei trasporti', 'Ingegneria ambientale']
        },
        'economia': {
            'Primo anno': ['Microeconomia', 'Macroeconomia', 'Statistica'],
            'Secondo anno': ['Economia aziendale', 'Finanza', 'Marketing'],
            'Terzo anno': ['Economia internazionale', 'Economia del lavoro', 'Economia dello sviluppo']
        }
    }

    if corso_di_laurea in esami:
        return render_template('elenco_esami.html', corso_di_laurea=corso_di_laurea, esami=esami[corso_di_laurea])
    else:
        return render_template('elenco_esami.html', corso_di_laurea=corso_di_laurea, esami={})


@app.route('/testiEsami')
def testi():
    # Dati degli esami di esempio
    corsi = {'informatica', 'ingegneria', 'economia'}
    esami = {
        'informatica': {
            'Primo anno': ['Matematica', 'Programmazione e laboratorio', 'Architettura dei calcolatori'],
            'Secondo anno': ['Algoritmi e strutture dati', 'Basi di dati', 'Reti di calcolatori'],
            'Terzo anno': ['Intelligenza artificiale', 'Sistemi distribuiti', 'Sicurezza informatica']
        },
        'ingegneria': {
            'Primo anno': ['Matematica', 'Fisica', 'Chimica'],
            'Secondo anno': ['Meccanica', 'Elettrotecnica', 'Materiali'],
            'Terzo anno': ['Termodinamica', 'Ingegneria dei trasporti', 'Ingegneria ambientale']
        },
        'economia': {
            'Primo anno': ['Microeconomia', 'Macroeconomia', 'Statistica'],
            'Secondo anno': ['Economia aziendale', 'Finanza', 'Marketing'],
            'Terzo anno': ['Economia internazionale', 'Economia del lavoro', 'Economia dello sviluppo']
        }
    }
    return render_template('testi_esami.html', esami=esami, corsiLaurea=corsi)


@app.route('/Admin/iscrittiAppelli')
def iscritti():
    corsi = {'informatica', 'ingegneria', 'economia'}
    return render_template('elenco_appelli_studenti.html', corsi)


@app.route('/Admin')
def administrator():
    return render_template('Admin.html')


@app.route('/Admin/delete_user')
def delete():
    return render_template('Delete_users.html', users=users)


@app.route('/Admin/add_user')
def add():
    return render_template('Add_users.html', users=users)


@app.route('/Admin/aggiungi_corso_laurea', methods=['GET', 'POST'])
def add_curse():
    if request.method == 'POST':
        codice = request.form['codice_corso']
        nome = request.form['nome_corso']
        specializzazione = request.form['specializzazione']
        indirizzo = request.form['indirizzo']

        corso_di_laurea = {'codice': codice, 'nome': nome, 'specializzazione': specializzazione, 'indirizzo': indirizzo}
        corsi_di_laurea.append(corso_di_laurea)

        return render_template('Crea_corso_di_laurea.html')
    else:
        return render_template('Crea_corso_di_laurea.html')


@app.route('/Admin/elimina_corso_laurea', methods=['GET'])
def elimina_corso_laurea_html():
    return render_template('Elimina_corso_di_laurea.html', corsi_di_laurea=corsi_di_laurea)


@app.route('/elimina_corso_laurea', methods=['POST'])
def elimina_corso_laurea():
    codice_corso = request.form['codice_corso']
    corso_da_elim = None
    # da rivedere
    for corso in corsi_di_laurea:
        if corso.codice == codice_corso:
            corso_da_elim = corso
            break
    if corso_da_elim:
        corsi_di_laurea.remove(corso_da_elim)

    return render_template('Elimina_corso_di_laurea.html', corsi_di_laurea=corsi_di_laurea)


@app.route('/Admin/aggiungi_corso', methods=['GET', 'POST'])
def aggiungi_corso():
    if request.method == 'POST':
        codice = request.form['codice_corso']
        nome = request.form['nome_corso']

        corso = {'codice': codice, 'nome': nome}
        corsi.append(corso)
        return render_template('Crea_corso.html')
    else:
        return render_template('Crea_corso.html')


@app.route('/Admin/elimina_corso', methods=['GET'])
def elimina_corso_html():
    return render_template('Elimina_corso.html', corsi=corsi)


@app.route('/Admin/assegnaCorso_CorsoLaurea', methods=['GET'])
def assegnaCorsoCorsoLaurea():
    listaCorsi1 = [
        {'codice': "01", 'nome': "Ingegneria"},
        {'codice': "02", 'nome': "Informatica"},
        {'codice': "03", 'nome': "Scienze Matematiche"}
    ]
    listaCorsi2 = [
        {'codice': "101", 'nome': "Storia dell'Arte"},
        {'codice': "102", 'nome': "Lettere Moderne"},
        {'codice': "103", 'nome': "Filosofia"}
    ]
    return render_template('Associazione_corso_corsolaurea.html', lista_corsi_laurea=listaCorsi1,
                           lista_corsi=listaCorsi2)


@app.route('/Admin/aggiungi_docente', methods=['GET', 'POST'])
def add_docente():
    if request.method == 'POST':
        data = request.get_json()
        codice_fiscale = data.get('codiceFiscale')
        nome = data.get('nome')
        cognome = data.get('cognome')
        mail = data.get('mail')
        anno_nascita = data.get('annoNascita')
        return render_template('Add_docente.html')
    else:
        return render_template('Add_docente.html')


@app.route('/elimina_corso', methods=['POST'])
def elimina_corso():
    codice_corso = request.form['codice_corso']
    corso_da_elim = None
    # da rivedere
    for corso in corsi_di_laurea:
        if corso.codice == codice_corso:
            corso_da_elim = corso
            break

    if corso_da_elim:
        corsi_di_laurea.remove(corso_da_elim)

    return render_template('Elimina_corso.html', corsi=corsi)


@app.route('/delete', methods=['POST'])
def delete_user():
    user_to_delete = request.form['user']
    if user_to_delete in users:
        users.remove(user_to_delete)
    return 'Utente eliminato con successo'


@app.route('/add', methods=['POST'])
def add_user():
    user_to_add = request.form['user']
    # aggiungere controllo se l'utente è gia presente nel db
    users.insert(len(users), user_to_add)
    return 'Utente aggiunto con successo'


@app.route('/associazioneCorso_CorsoLaurea', methods=['POST'])
def invia_dati():
    data = request.get_json()
    corso1 = data.get('corso1')
    corso2 = data.get('corso2')

    # Esegui qui la logica per elaborare i dati ricevuti dal client
    # Ad esempio, puoi salvare i dati nel database o fare altre operazioni

    # Ritorna una risposta al client (opzionale)
    response = {'messaggio': 'Dati ricevuti correttamente dal server'}
    return jsonify(response)


@app.route('/Admin/delete_docente')
def delete_docenti_html():
    return render_template('Delete_docenti.html', users = json.dumps(docenti))


@app.route('/delete_docente', methods=['POST'])
def delete_docenti():
    if request.method == 'POST':
        data = request.get_json()
        codice_fiscale_da_eliminare = data.get('codice_fiscale')

        global docenti
        docenti = [docente for docente in docenti if docente['codice_fiscale'] != codice_fiscale_da_eliminare]

        return jsonify("Docente eliminato")


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route('/stud')
def index_studenti():
    return render_template('menu_studenti.html')


@app.route('/stud/lista_esami_utente')
def show_list_exam():
    corsi = [
        {
            'codice': 'C001',
            'nome': 'Matematica',
            'data_esame': '2023-07-01',
            'voto': 28,
            'crediti': 6
        },
        {
            'codice': 'C002',
            'nome': 'Informatica',
            'data_esame': '2023-07-10',
            'voto': 30,
            'crediti': 9
        },
        {
            'codice': 'C003',
            'nome': 'Fisica',
            'data_esame': '2023-07-15',
            'voto': None,
            'crediti': 6
        },
        {
            'codice': 'C004',
            'nome': 'Programmazione',
            'data_esame': '2023-07-15',

            'crediti': 6
        }
    ]
    # Nel caso il voto sia None, oppure assente la cella corrispondente nella tabella html risulterà essere vuota
    return render_template('lista_esami_utente.html', corsi=corsi)


@app.route('/stud/prenotazioni_appelli')
def prenotazioni_appelli():
    return render_template('prenotazioni_appelli.html', righe=righe_iniziali)


@app.route('/stud/bacheca_prenotazione_appelli')
def bacheca_appelli():
    return render_template('bacheca_prenotazione_appelli.html', righe=righe_uniche)


@app.route('/aggiungi_riga', methods=['POST'])
def aggiungi_riga():
    riga = request.get_json()
    if riga not in righe_uniche:
        righe_uniche.append(riga)
    return jsonify({"message": "Riga aggiunta con successo"})


@app.route('/delete_appello', methods=['POST'])
def delete_appello():
    riga = request.get_json()
    if riga in righe_uniche:
        righe_uniche.remove(riga)
    return jsonify({"message": "Riga rimossa con successo"})


@app.route('/stud/bacheca_esiti')
def exam_details():
    # Esempio di lista di dettagli delle prove d'esame
    exam_list = [
        {'codice_corso': 'C001', 'nome_corso': 'Matematica', 'voto': 'insufficente', 'data_esame': '2023-07-15'},
        {'codice_corso': 'C002', 'nome_corso': 'Fisica', 'voto': 25, 'data_esame': '2023-07-14'},
        {'codice_corso': 'C001', 'nome_corso': 'Matematica', 'voto': 30, 'data_esame': '2023-07-10'},
        {'codice_corso': 'C003', 'nome_corso': 'Informatica', 'voto': 24, 'data_esame': '2023-07-12'}
    ]

    # Raggruppa gli elementi con lo stesso codice corso
    grouped_exam_list = {}
    for exam in exam_list:
        codice_corso = exam['codice_corso']
        if codice_corso not in grouped_exam_list:
            grouped_exam_list[codice_corso] = []
        grouped_exam_list[codice_corso].append(exam)

    return render_template('Bacheca_esiti.html', grouped_exam_list=grouped_exam_list)


if __name__ == '__main__':
    app.run()
