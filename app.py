from flask import *

from administrator import *
from utenti import *

# Create Flask Instance
app = Flask(__name__)
# Set debug mode to True
app.debug = True

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

righe_uniche = []
righe_iniziali = [
    {"codice_corso": "ABC123", "nome_corso": "Corso A", "data_esame": "2023-07-20", "aula": "Aula 1"},
    {"codice_corso": "DEF456", "nome_corso": "Corso B", "data_esame": "2023-07-25", "aula": "Aula 2"},
]
esami = []

lista_corsi = [
    {"codice": "Corso A", "nome": "informatica"},
    {"codice": "Corso B", "nome": "matematica"},
]
lista_esami = [
    {"id": 1, "corso": "Corso A", "nome_esame": "Esame 1", "data": "2023-07-19", "tipo": "Scritto", "valore": "6"},
    {"id": 2, "corso": "Corso B", "nome_esame": "Esame 2", "data": "2023-07-20", "tipo": "Orale", "valore": "3"},
    {"id": 3, "corso": "Corso C", "nome_esame": "Esame 3", "data": "2023-07-21", "tipo": "Progetto", "valore": "12"},
]
phone_numbers = ['1234567890', '9876543210', '5555555555']
data_esami = [
    {'codiceEsame': "E001", 'corso': "Matematica", 'data': "2023-07-25", 'tipo': "Scritto"},
    {'codiceEsame': "E002", 'corso': "Fisica", 'data': "2023-08-10", 'tipo': "Orale"},
    {'codiceEsame': "E003", 'corso': "Informatica", 'data': "2023-08-15", 'tipo': "Pratico"}
]
studenti = [
    {'matricola': 'ABC123', 'nome': 'Mario', 'cognome': 'Rossi'},
    {'matricola': 'DEF456', 'nome': 'Paola', 'cognome': 'Verdi'},
    {'matricola': 'GHI789', 'nome': 'Luigi', 'cognome': 'Bianchi'}
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


@app.route("/reset_pwd", methods=["GET", "POST"])
def resetpwd():
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        if password == confirm_password:
            hash_password = hashlib.sha256(confirm_password.encode('utf-8'))
            hash_value=hash_password.hexdigest()
            cursor = mysql.cursor()
            query = "UPDATE temporaryuser SET password = %s WHERE mail = %s"
            cursor.execute(query, (hash_value, email))
            mysql.commit()
            cursor.close()
            return redirect("/login")
    return render_template("reset_pwd.html")


# localhost:5000/sign_up
@app.route(
    "/sign_up", methods=["GET", "POST"]
)  # se number è 1 l'utente si è registrato e deve attendere che la segreteria lo accetti
def signUp():
    corsi = {}
    if request.method == "POST":
        num_items = len(request.form)
        if num_items > 6:
            codicefiscale = request.form["Codicefiscale"]
            name = request.form["Nome"]
            surname = request.form["Cognome"]
            dateofbirth = request.form["AnnoNascita"]
            email = request.form["Email"]
            password = request.form["password"]
            corsolaurea = request.form["corsoLaurea"]

            if sign_up_control(
                codicefiscale, name, surname, dateofbirth, email, password, corsolaurea
            ):
                number = sign_up_aux(
                    codicefiscale,
                    name,
                    surname,
                    dateofbirth,
                    email,
                    password,
                    corsolaurea,
                    mysql,
                )
                if number == 1:
                    return redirect("/login")
    sign_up_corsolaurea(corsi, mysql)
    return render_template("sign_up.html", corsiLaurea=corsi)


# localhost:5000/login
@app.route('/login', methods=['GET', 'POST'])#se number è 1 accedo a menù studente, se è 2 a menù docente, se la mail e la password corrispondono alle credenziali dell'amministratore entro nel menù amministratore 
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        studente, docente = login_aux(mail, password, mysql)
        if studente is not None and docente is None:
            session['codicefiscale']=studente['codicefiscale']
            session['nome']=studente['nome']    
            session['cognome']=studente['cognome']
            session['annoNascita']=studente['annoNascita']
            session['mail']=studente['mail']
            session['ruolo']='Studente'
            return redirect('/menu_studenti')
        elif docente is not None and studente is None:
            session['codicefiscale']=docente['codicefiscale']
            session['nome']=docente['nome']
            session['cognome']=docente['cognome']
            session['annoNascita']=docente['annoNascita']
            session['mail']=docente['mail']
            session['ruolo']='Docente'
            #return redirect(f'/user_data?ruolo=Docente')
            return redirect('/menu_docenti')
        elif mail=="admin@administrator.com" and password=="admin":
            return redirect('/menu_amministratore')
                
    return render_template("login.html")

@app.route('/menu_studenti')
def menu_studenti():
    ruolo = 'Studente'
    return render_template("menu_studenti.html", ruolo=ruolo)

@app.route('/menu_docenti')
def menu_docenti():
    ruolo = 'Docente'
    return render_template("menu_docenti.html", ruolo=ruolo)

@app.route('/menu_amministratore')
def menu_amminsitratore():
    return render_template("menu_amministratore.html")

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


@app.route('/user_data')
def home():
    # Dati utente di esempio
    cf= session.get('codicefiscale')
    nome = session.get('nome')
    cognome = session.get('cognome')
    anno_nascita = session.get('annoNascita')
    email = session.get('mail')
    ruolo = session.get('ruolo')
    return render_template('info_utente.html', codice_fiscale=cf, nome=nome, cognome=cognome, mail=email,
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


@app.route('/Admin')
def administrator():
    return render_template('menu_amministatore.html')


@app.route('/Admin/delete_user', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        data = request.get_json()
        cf = data.get('cod_fiscale')
        delete_aux(cf, mysql)
        return 'Utente eliminato con successo'
    else:
        users = get_studenti(mysql)
        return render_template('Delete_users.html', users=users)


# Administator
@app.route('/Admin/add_user', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.get_json()
        stud = {
            'codice_fiscale': data.get('cod_fiscale'),
            'nome': data.get('nome'),
            'cognome': data.get('cognome'),
            'matricola': data.get('matricola'),
            'mail': data.get('mail'),
            'annoNascita': data.get('anno_nascita'),
            'password': data.get('pwd'),
            'corso_laurea': data.get('corso_di_laurea')
        }
        delete_tempuser(stud['codice_fiscale'], mysql)
        add_user(stud, mysql)
        return "Operation Complete"
    else:
        users_info = get_temporaryuser(mysql)
        return render_template('Add_users.html', users=users_info)


@app.route('/Admin/aggiungi_corso_laurea', methods=['GET', 'POST'])
def add_degree_course():
    if request.method == 'POST':
        cod_corso = request.form['codice_corso']
        nome_corso = request.form['nome_corso']
        spec = request.form['specializzazione']
        indirizzo = request.form['indirizzo']

        add_degree_course_aux(cod_corso, nome_corso, spec, indirizzo, mysql)
    else:
        return render_template('Crea_corso_di_laurea.html')


@app.route('/Admin/elimina_corso_laurea', methods=['GET', 'POST'])
def delete_degree_course():
    if request.method == 'POST':
        codice_corso = request.form['codice_corso']
        delete_degree_course_aux_post(codice_corso, mysql)
        return redirect(url_for('index_admin'))
    else:
        corsi_di_laurea = get_degree_course(mysql)
        return render_template('Elimina_corso_di_laurea.html', corsi_di_laurea=corsi_di_laurea)


@app.route('/Admin/aggiungi_corso', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        codice = request.form['codice_corso']
        nome = request.form['nome_corso']

        add_course_aux(codice, nome, mysql)

        return redirect(url_for('add_course'))
    else:
        return render_template('Crea_corso.html')


@app.route('/Admin/elimina_corso', methods=['GET', 'POST'])
def delete_course():
    if request.method == 'POST':
        codice_corso = request.form['codice_corso']
        delete_course_aux_post(codice_corso, mysql)

        return redirect(url_for('delete_course'))
    else:
        corsi = get_couse(mysql)
        return render_template('Elimina_corso.html', corsi=corsi)


@app.route('/Admin/assegnaCorso_CorsoLaurea', methods=['GET', 'POST'])
def assegnaCorsoCorsoLaurea():
    if request.method == 'POST':
        data = request.get_json()
        corso_laurea = data.get('corso1')
        corso = data.get('corso2')
        anno = data.get('anno')
        assegnaCorsoCorsoLaurea_aux(corso_laurea, corso, anno, mysql)
        return "Operation Complete"
    else:
        corsi_laurea = get_degree_course(mysql)
        corsi = get_couse(mysql)
        return render_template('Associazione_corso_corsolaurea.html', lista_corsi_laurea=corsi_laurea,
                               lista_corsi=corsi)


@app.route('/Admin/delete_docente', methods=['GET', 'POST'])
def delete_docenti():
    if request.method == 'POST':
        data = request.get_json()
        codice_fiscale_da_eliminare = data.get('codice_fiscale')

        delete_docenti_aux(codice_fiscale_da_eliminare, mysql)
    else:
        docenti = get_docenti(mysql)
        return render_template('Delete_docenti.html', users=json.dumps(docenti))


@app.route('/Admin/aggiungi_docente', methods=['GET', 'POST'])
def add_docente():
    if request.method == 'POST':
        data = request.get_json()
        docente = {
            'codice_fiscale': data.get('codiceFiscale'),
            'nome': data.get('nome'),
            'cognome': data.get('cognome'),
            'mail': data.get('mail'),
            'anno_nascita': data.get('annoNascita'),
            'password': data.get('password')
        }
        add_docente_aux(docente, mysql)

        return render_template('Add_docente.html')
    else:
        return render_template('Add_docente.html')


@app.route('/Admin/delete_corso_corsoLaurea', methods=['GET', 'POST'])
def delete_corso_crosoLaurea():
    if request.method == 'POST':
        data = request.get_json()
        deg_course = data.get('codiceCorsoLaurea')
        course = data.get('codiceCourse')
        delete_corso_crosoLaurea_aux_post(deg_course, course, mysql)
        return "Operation Complete"
    else:
        corsiLaurea = get_degree_course(mysql)
        cors = get_couse(mysql)
        corsi_corsiLaurea = get_couse_degree_course(mysql)
        return render_template('Delete_corsi_CorsiLaurea.html',
                               corsi_Laurea=corsiLaurea,
                               corsi=json.dumps(cors),
                               deg_course=json.dumps(corsi_corsiLaurea))


@app.route('/Admin/associazioneCorso_Docente', methods=['GET', 'POST'])
def assegna_Corso_Docente():
    if request.method == 'POST':
        data = request.get_json()
        docente = data.get('cod_Docente')
        corso = data.get('cod_Corso')
        # none rappresenta dataApertura
        assegna_Corso_Docente_aux(docente, corso, None, mysql)
        return "Operation Complete"
    else:
        docenti = get_docenti(mysql)
        corsi = get_couse(mysql)
        return render_template('Assegnazione_corso_docente.html', docenti=docenti, corsi=corsi)


@app.route('/Admin/delete_corso_Docente', methods=['GET', 'POST'])
def delete_corso_Docente():
    if request.method == 'POST':
        data = request.get_json().get('dataToSend')
        doc_cf = data.get('doc_code')
        code_course = data.get('course_code')
        delete_corso_Docente_aux(doc_cf, code_course,mysql)
        return "Operation Complete"
    else:
        docenti = get_docenti(mysql)
        cors = get_couse(mysql)
        corsi_docenti = get_couse_docenti(mysql)
        return render_template('Delete_corsi_docenti.html', docenti=docenti,
                               corsi=json.dumps(cors),
                               corsi_doc=json.dumps(corsi_docenti))


@app.route('/Docenti/<codiceEsame>/Assegna_voti', methods=['GET', 'POST'])
def assegna_voti(codiceEsame):
    if request.method == 'POST':
        return json.dumps(studenti)
    else:
        studenti = assegna_voto_aux(mysql,codiceEsame)
        return render_template('Inserimento_voti.html', studenti=json.dumps(studenti))


@app.route('/Docenti/ricevi-voti', methods=['POST'])
def ricevi_dati():
    dati = request.get_json()
    tableData = dati.get('tableData', [])
    mat = tableData[0]['matricola']
    return jsonify(mat)


@app.route('/Docenti/Elenco_esami', methods=['GET', 'POST'])
def table_esami():
    if request.method=='GET':
        esami = tabella_esami(mysql)
        return render_template('Tabella_esami.html', esami=json.dumps(esami))


# Endpoint per la gestione della richiesta del pulsante "Assegna voti"
def exam_get_datas():
    cursor = mysql.cursor()
    query = 'SELECT * FROM esami'
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


@app.route('/Docenti/Crea_Esame', methods=['GET', 'POST'])
def crea_esame():
    cf_docente = session.get('codicefiscale')
    lista_corsi = []
    if (request.method == 'POST'):
        corso = request.form['corso']
        nome_esame = request.form['nome_esame']
        codice_esame = request.form['codice_esame']
        data = request.form['data']
        tipo = request.form['tipo']
        valore = request.form['valore']
        crea_esame_inserisci(mysql,corso, nome_esame, codice_esame, data, tipo, valore, cf_docente)

    lista_corsi = crea_esame_docenti(mysql,cf_docente)
    print(lista_corsi)
    if request.method=='POST':
        return render_template('Crea_esame.html', corsi=lista_corsi)
    else:
        return render_template('Crea_esame.html', corsi=lista_corsi)


@app.route('/Docenti/Elimina_Esame', methods=['GET', 'POST'])
def elimina_Esame():
    cf_docente = session.get('codicefiscale')
    if request.method == 'POST':
        esame = request.form['esame']
        elimina_esame_post(mysql,esame,cf_docente)
    lista_esami =elimina_esame_get(mysql,cf_docente)
    return render_template('Delete_esame.html', esami=lista_esami)


@app.route('/delete/<int:esame_id>', methods=['POST'])
def delete_esame(esame_id):
    global lista_esami
    lista_esami = [esame for esame in lista_esami if esame['id'] != esame_id]
    return render_template('Delete_esame.html', esami=lista_esami)


@app.route('/Docenti/Numeri_di_telefono')
def phone_number():
    cf_docente = session.get('codicefiscale')
    phone_numbers = session.get('phone_numbers', [])
    phone_numbers = phone_number_aux(mysql,cf_docente)
    return render_template('Numeri_telefono.html', phone_numbers=phone_numbers)



@app.route('/add_phone', methods=['POST'])
def add_phone_number():
    cf_docente = session.get('codicefiscale')
    data = request.get_json()
    number_to_add = data.get('number')
    try:
        add_number_aux(mysql, number_to_add, cf_docente)
        return jsonify(message="Numero di telefono aggiunto correttamente.")
    except Exception as e:
        return jsonify(message="Errore durante l'aggiunta del numero di telefono. Dettagli: " + str(e))



@app.route('/delete_phone', methods=['POST'])
def delete_phone_number():
    cf_docente = session.get('codicefiscale')
    data = request.get_json()
    numero_telefono = data.get('number')
    try:
        delete_number_aux(mysql,numero_telefono, cf_docente)
        return jsonify(message="Numero di telefono eliminato correttamente.")
    except Exception as e:
        return jsonify(message="Errore durante l'eliminazione del numero di telefono. Dettagli: " + str(e))


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


@app.route('/Docenti')
def index_docenti():
    return render_template('menu_docenti.html')


@app.route('/Admin')
def index_admin():
    return render_template('menu_amministatore.html')


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
