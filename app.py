from flask import *
from flask.sessions import SessionMixin
from administrator import *
from classi import *
from studenti import *
from docenti import *
from auxiliary import *

"""
la funzione index() permette di accedere alla pagina iniziale del sito
la funzione get_degree_course restituisce la lista dei corsi di laurea 
la funzion get_all_course restituisce la liste dei corsi appartenenti ad un corso di laurea
"""


@app.route("/")
def index():
    session.clear()
    session["ruolo"] = None
    corsi_Laurea = get_degree_course()
    corsi = get_all_course()
    return render_template("index.html", corsi=corsi, corsi_Laurea=corsi_Laurea)


"""
la funzione resetpwd() permette di resettare la password dell'utente
essa prende in input la nuova password e la conferma della nuova password
se le due password coincidono allora la password viene aggiornata nel database all'intero della tabella Studenti
in corrispondenza della mail inserita 
"""


@app.route("/reset_pwd", methods=["GET", "POST"])
def resetpwd():
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        email = request.form["email"]
        tab = checkMail(email)
        return reset_pwd_aux(email, password, confirm_password, tab)
    return render_template("reset_pwd.html")


"""
la funzione signUp() permette di registrare un nuovo utente
essa prende in input i dati inseriti dall'utente e controlla
che l'utente abbia inserito tutti i dati richiesti
successivamente se il numero ricevuto dalla funzione sign_up_aux() è 1 allora l'utente è stato registrato correttamente
altrimenti l'utente è già registrato e deve attendere che la segreteria accetti la sua richiesta
la funzione sign_up_corsolaurea serve a visualizzare nel menù a tendina i corsi di laurea disponibili
"""


@app.route("/sign_up", methods=["GET", "POST"])
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
                )
                if number == 1:
                    return redirect("/login")
    sign_up_corsolaurea(corsi)
    return render_template("sign_up.html", corsiLaurea=corsi)


"""
la funzione login() permette di effettuare il login
essa prende in input la mail e la password inserite dall'utente
se l'utente è un docente allora viene reindirizzato alla pagina docenti
se l'utente è uno studente allora viene reindirizzato alla pagina studenti
se l'utente è l'amministratore allora viene reindirizzato alla pagina amministratore
inoltre vengono salvati nella sessione i dati dell'utente che ha effettuato il login
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        studente, docente = login_aux(mail, password)
        if studente is not None and docente is None:
            session["codicefiscale"] = studente["codicefiscale"]
            session["nome"] = studente["nome"]
            session["cognome"] = studente["cognome"]
            session["annoNascita"] = studente["annoNascita"]
            session["mail"] = studente["mail"]
            session["corsoLaurea"] = studente["CorsoLaurea"]
            session["matricola"] = studente["matricola"]
            session["ruolo"] = "Studente"
            return redirect("/stud")
        elif docente is not None and studente is None:
            session["codicefiscale"] = docente["codicefiscale"]
            session["nome"] = docente["nome"]
            session["cognome"] = docente["cognome"]
            session["annoNascita"] = docente["annoNascita"]
            session["mail"] = docente["mail"]
            session["ruolo"] = "Docente"
            return redirect("/Docenti")
        elif mail == "admin@administrator.com" and password == "admin":
            session["ruolo"] = "Admin"
            return redirect("/Admin")
    return render_template("login.html")


"""
la funzione index_studenti() permette di visualizzare il menù degli studenti
"""


@app.route("/stud")
def index_studenti():
    if "ruolo" in session and session["ruolo"] == "Studente":
        return render_template("menu_studenti.html")
    else:
        abort(403)


"""
la funzione index_docenti() permette di visualizzare il menù dei docenti
"""


@app.route("/Docenti")
def index_docenti():
    if "ruolo" in session and session["ruolo"] == "Docente":
        return render_template("menu_docenti.html")
    else:
        abort(403)


"""
la funzione home_stud() permette di visualizzare le informazioni dello studente
"""


@app.route("/stud/user_data")
def home_stud():
    # Dati utente di esempio
    cf = session.get("codicefiscale")
    nome = session.get("nome")
    cognome = session.get("cognome")
    anno_nascita = session.get("annoNascita")
    email = session.get("mail")
    ruolo = session.get("ruolo")
    return render_template(
        "info_utente.html",
        codice_fiscale=cf,
        nome=nome,
        cognome=cognome,
        mail=email,
        anno_nascita=anno_nascita,
        ruolo=ruolo,
    )


"""
la funzione home_docenti() permette di visualizzare le informazioni del docente
"""


@app.route("/Docenti/user_data")
def home_docenti():
    # Dati utente di esempio
    cf = session.get("codicefiscale")
    nome = session.get("nome")
    cognome = session.get("cognome")
    anno_nascita = session.get("annoNascita")
    email = session.get("mail")
    ruolo = session.get("ruolo")
    return render_template(
        "info_utente.html",
        codice_fiscale=cf,
        nome=nome,
        cognome=cognome,
        mail=email,
        anno_nascita=anno_nascita,
        ruolo=ruolo,
    )


"""
la funzione administrator() permette di visualizzare il menù dell'amministratore
"""


@app.route("/Admin")
def administrator():
    if "ruolo" in session and session["ruolo"] == "Admin":
        return render_template("menu_amministratore.html")
    else:
        abort(403)


"""
la funzione delete permette di eliminare un utente dal database, essa prende in input il codice fiscale dell'utente da eliminare
"""


@app.route("/Admin/delete_user", methods=["GET", "POST"])
def delete():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            cf = data.get("cod_fiscale")
            delete_aux(cf)
            return "Utente eliminato con successo"
        else:
            users = get_studenti()
            return render_template("Delete_users.html", users=users)
    else:
        abort(403)


"""
la funzione add() permette di aggiungere un utente al database
in stud si trovano i dati dello studente da aggiungere
"""


@app.route("/Admin/add_user", methods=["GET", "POST"])
def add():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            stud = {
                "codice_fiscale": data.get("cod_fiscale"),
                "nome": data.get("nome"),
                "cognome": data.get("cognome"),
                "matricola": data.get("matricola"),
                "mail": data.get("mail"),
                "annoNascita": data.get("anno_nascita"),
                "password": data.get("pwd"),
                "corso_laurea": data.get("corso_di_laurea"),
            }
            delete_tempuser(stud["codice_fiscale"])
            add_user(stud)
            return "Operation Complete"
        else:
            users_info = get_temporaryuser()
            return render_template("Add_users.html", users=users_info)
    else:
        abort(403)


"""
la funzione add_degree_course() permette di aggiungere un corso di laurea al database
attraverso il metodo POST si ricevono i dati del corso di laurea da aggiungere
successivamente si richiama la funzione add_degree_course_aux() che aggiunge il corso di laurea al database
"""


@app.route("/Admin/aggiungi_corso_laurea", methods=["GET", "POST"])
def add_degree_course():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            cod_corso = data.get("codiceCorso")
            nome_corso = data.get("nome")
            spec = data.get("specializzazione")
            indirizzo = data.get("indirizzo")
            add_degree_course_aux(cod_corso, nome_corso, spec, indirizzo)
            return "Operation complete"
        else:
            return render_template("Crea_corso_di_laurea.html")
    else:
        abort(403)


"""
la funzione delete_degree_course() permette di eliminare un corso di laurea al database
attraverso il metodo POST si riceve il codice del corso di laurea da eliminare
successivamente si richiama la funzione delete_degree_course_aux() che elimina il corso di laurea al database
il metodo GET allora si richiama la funzione get_degree_course() che restituisce la lista dei corsi di laurea
"""


@app.route("/Admin/elimina_corso_laurea", methods=["GET", "POST"])
def delete_degree_course():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            codice_corso = request.form["codice_corso"]
            delete_degree_course_aux_post(codice_corso)
            return redirect(url_for("administrator"))
        else:
            corsi_di_laurea = get_degree_course()
            return render_template(
                "Elimina_corso_di_laurea.html", corsi_di_laurea=corsi_di_laurea
            )
    else:
        abort(403)


"""
la funzione add_course() permette di aggiungere un corso al database
attraverso il metodo POST si ricevono i dati del corso da aggiungere
successivamente si richiama la funzione add_course_aux() che aggiunge il corso al database  
il metodo GET richiama la funzione get_course() che restituisce la lista dei corsi
"""


@app.route("/Admin/aggiungi_corso", methods=["GET", "POST"])
def add_course():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            cod_corso = data.get("codiceCorso")
            nome_corso = data.get("nome")
            valore = data.get("cfu")
            add_course_aux(cod_corso, nome_corso, valore)
            return redirect(url_for("administrator"))
        else:
            return render_template("Crea_corso.html")
    else:
        abort(403)


"""
la funzione delete_course() permette di eliminare un corso al database
attraverso il metodo POST si riceve il codice del corso da eliminare
successivamente si richiama la funzione delete_course_aux() che elimina il corso al database
il metodo GET richiama la funzione get_course() che restituisce la lista dei corsi

"""


@app.route("/Admin/elimina_corso", methods=["GET", "POST"])
def delete_course():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            codice_corso = request.form["codice_corso"]
            delete_course_aux_post(codice_corso)

            return redirect(url_for("administrator"))
        else:
            corsi = get_course()
            return render_template("Elimina_corso.html", corsi=corsi)
    else:
        abort(403)


"""
la funzione assegnaCorsoCorsoLaurea() permette di associare un corso di laurea ad un corso
attraverso il metodo POST si ricevono i dati del corso di laurea del corso da associare e l'anno di insegnamento
"""


@app.route("/Admin/assegnaCorso_CorsoLaurea", methods=["GET", "POST"])
def assegnaCorsoCorsoLaurea():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            corso_laurea = data.get("corso1")
            corso = data.get("corso2")
            anno = data.get("anno")

            assegnaCorsoCorsoLaurea_aux(corso_laurea, corso, anno)
            return "Operation Complete"
        else:
            corsi_laurea = get_degree_course()
            corsi = get_course()
            return render_template(
                "Associazione_corso_corsolaurea.html",
                lista_corsi_laurea=corsi_laurea,
                lista_corsi=corsi,
            )
    else:
        abort(403)


"""
la funzione delete_docenti() permette di eliminare un docente dal database
attraverso il metodo POST si riceve il codice fiscale del docente da eliminare
successivamente si richiama la funzione delete_docenti_aux() che elimina il docente dal database
il metodo GET richiama la funzione get_docenti() che restituisce la lista dei docenti
"""


@app.route("/Admin/delete_docente", methods=["GET", "POST"])
def delete_docenti():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            codice_fiscale_da_eliminare = data.get("codice_fiscale")

            delete_docenti_aux(codice_fiscale_da_eliminare)
        else:
            docenti = get_docenti()
            return render_template("Delete_docenti.html", users=json.dumps(docenti))
    else:
        abort(403)


"""
la funzione add_docente() permette di aggiungere un docente al database
attraverso il metodo POST si ricevono i dati del docente da aggiungere
successivamente si richiama la funzione add_docente_aux() che aggiunge il docente al database

"""


@app.route("/Admin/aggiungi_docente", methods=["GET", "POST"])
def add_docente():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            docente = {
                "codice_fiscale": data.get("codiceFiscale"),
                "nome": data.get("nome"),
                "cognome": data.get("cognome"),
                "mail": data.get("mail"),
                "anno_nascita": data.get("annoNascita"),
                "password": data.get("password"),
            }
            add_docente_aux(docente)

            return redirect(url_for("administrator"))
        else:
            return render_template("Add_docente.html")
    else:
        abort(403)


"""
la funzione delete_corso_corsoLaurea() permette di eliminare un corso di laurea da un corso
attraverso il metodo POST si ricevono i dati del corso di laurea del corso da eliminare
successivamente si richiama la funzione delete_corso_corsoLaurea_aux() che elimina il corso di laurea dal corso
il metodo GET richiama la funzione get_degree_course() che restituisce la lista dei corsi di laurea e la funzione get_course() che restituisce la lista dei corsi
e la funzione get_course_degree_course() che restituisce la lista dei corsi di laurea associati ad un corso
"""


@app.route("/Admin/delete_corso_corsoLaurea", methods=["GET", "POST"])
def delete_corso_crosoLaurea():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            deg_course = data.get("codiceCorsoLaurea")
            course = data.get("codiceCourse")
            delete_corso_corsoLaurea_aux_post(deg_course, course)
            return "Operation Complete"
        else:
            corsiLaurea = get_degree_course()
            cors = get_course()
            corsi_corsiLaurea = get_course_degree_course()
            return render_template(
                "Delete_corsi_CorsiLaurea.html",
                corsi_Laurea=corsiLaurea,
                corsi=json.dumps(cors),
                deg_course=json.dumps(corsi_corsiLaurea),
            )
    else:
        abort(403)


"""
la funzione assegna_Corso_Docente() permette di associare un corso ad un docente
attraverso il metodo POST si ricevono i dati del corso del docente da associare
successivamente si richiama la funzione assegna_Corso_Docente_aux() che associa il corso al docente
il metodo GET richiama la funzione get_docenti() che restituisce la lista dei docenti e la funzione get_course() che restituisce la lista dei corsi
"""


@app.route("/Admin/associazioneCorso_Docente", methods=["GET", "POST"])
def assegna_Corso_Docente():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            docente = data.get("cod_Docente")
            corso = data.get("cod_Corso")
            assegna_Corso_Docente_aux(docente, corso)
            return "Operation Complete"
        else:
            docenti = get_docenti()
            corsi = get_course()
            return render_template(
                "Assegnazione_corso_docente.html", docenti=docenti, corsi=corsi
            )
    else:
        abort(403)


"""
la funzione delete_corso_Docente() permette di eliminare un corso da un docente
attraverso il metodo POST si ricevono i dati del corso del docente da eliminare
successivamente si richiama la funzione delete_corso_Docente_aux() che elimina il corso dal docente
il metodo GET richiama la funzione get_docenti() che restituisce la lista dei docenti e la funzione get_course() che restituisce la lista dei corsi
e la funzione get_course_docenti() che restituisce la lista dei corsi associati ad un docente
"""


@app.route("/Admin/delete_corso_Docente", methods=["GET", "POST"])
def delete_corso_Docente():
    if "ruolo" in session and session["ruolo"] == "Admin":
        if request.method == "POST":
            data = request.get_json()
            doc_cf = data.get("doc_code")
            code_course = data.get("course_code")
            delete_corso_Docente_aux(doc_cf, code_course)
            return "Operation Complete"
        else:
            docenti = get_docenti()
            cors = get_course()
            corsi_docenti = get_course_docenti()
            return render_template(
                "Delete_corsi_docenti.html",
                docenti=docenti,
                corsi=json.dumps(cors),
                corsi_doc=json.dumps(corsi_docenti),
            )
    else:
        abort(403)


"""
la funzione assegna_voti() permette di assegnare un voto ad uno studente
ha come parametro il codice dell'esame
nel metodo GET si richiama la funzione assegna_voto_aux() che restituisce la lista degli studenti che hanno sostenuto l'esame
@codiceEsame: codice dell'esame

"""


@app.route("/Docenti/<codiceEsame>/Assegna_voti", methods=["GET", "POST"])
def assegna_voti(codiceEsame):
    if "ruolo" in session and session["ruolo"] == "Docente":
        if request.method == "POST":
            return "ok"
        else:
            studenti = assegna_voto_aux(codiceEsame)
            session["CodiceEsame"] = codiceEsame
            return render_template(
                "Inserimento_voti.html", studenti=json.dumps(studenti)
            )
    else:
        abort(403)


"""
la funzione ricevi_dati() permette di ricevere i dati dello studente e il voto da assegnare
la funzione take_cf() restituisce il codice fiscale dello studente
la funzione ricevi_dati_aux() permette di inserire il voto dello studente nel database
"""


@app.route("/Docenti/ricevi-voti", methods=["POST"])
def ricevi_dati():
    dati = request.get_json()
    tableData = dati.get("tableData", [])
    mat = tableData[0]["matricola"]
    voto = tableData[0]["voto"]
    codiceEsame = session.get("CodiceEsame")
    cf = take_cf(mat)
    ricevi_dati_aux(cf, codiceEsame, voto)
    return jsonify(mat)


"""
la funzione lista_esami() permette di visualizzare la lista degli esami
viene richiamata la funzione lista_esami_aux() che restituisce la lista degli esami
"""


@app.route("/Docenti/Elenco_esami", methods=["GET", "POST"])
def table_esami():
    if "ruolo" in session and session["ruolo"] == "Docente":
        if request.method == "GET":
            esami = tabella_esami()
            return render_template("Tabella_esami.html", esami=json.dumps(esami))
    else:
        abort(403)


"""
la funzione crea_esame() permette di creare un esame
attraverso il metodo POST si ricevono i dati dell'esame da creare
successivamente si richiama la funzione crea_esame_inserisci() che crea l'esame
il metodo GET richiama la funzione crea_esame_docenti() che restituisce la lista dei corsi

"""


@app.route("/Docenti/Crea_Esame", methods=["GET", "POST"])
def crea_esame():
    if "ruolo" in session and session["ruolo"] == "Docente":
        cf_docente = session.get("codicefiscale")
        lista_corsi = []
        if request.method == "POST":
            corso = request.form["corso"]
            nome_esame = request.form["nome_esame"]
            codice_esame = request.form["codice_esame"]
            data = request.form["data"]
            tipo = request.form["tipo"]
            valorePerc = request.form["valorePerc"]
            crea_esame_inserisci(
                corso, nome_esame, codice_esame, data, tipo,cf_docente, valorePerc
            )

        lista_corsi = crea_esame_docenti(cf_docente)
        if request.method == "POST":
            return render_template("Crea_esame.html", corsi=lista_corsi)
        else:
            return render_template("Crea_esame.html", corsi=lista_corsi)
    else:
        abort(403)


"""
la funzione elimina_esame() permette di eliminare un esame
attraverso il metodo POST si riceve il codice dell'esame da eliminare
successivamente si richiama la funzione elimina_esame_post() che elimina l'esame
il metodo GET richiama la funzione elimina_esame_get() che restituisce la lista degli esami

"""


@app.route("/Docenti/Elimina_Esame", methods=["GET", "POST"])
def elimina_Esame():
    if "ruolo" in session and session["ruolo"] == "Docente":
        cf_docente = session.get("codicefiscale")
        if request.method == "POST":
            esame = request.form.get("codEsame")
            elimina_esame_post(esame, cf_docente)
        lista_esami = elimina_esame_get(cf_docente)
        return render_template("Delete_esame.html", esami=lista_esami)
    else:
        abort(403)


"""
la funzione phone_number() permette di visualizzare i numeri di telefono del docente
viene richiamata la funzione phone_number_aux() che restituisce la lista dei numeri di telefono del docente

"""


@app.route("/Docenti/Numeri_di_telefono")
def phone_number():
    if "ruolo" in session and session["ruolo"] == "Docente":
        cf_docente = session.get("codicefiscale")
        phone_numbers = session.get("phone_numbers", [])
        phone_numbers = phone_number_aux(cf_docente)
        return render_template("Numeri_telefono.html", phone_numbers=phone_numbers)
    else:
        abort(403)


"""
la funzione add_phone_number() permette di aggiungere un numero di telefono al docente
attraverso il metodo POST si riceve il numero di telefono da aggiungere
successivamente si richiama la funzione add_number_aux() che aggiunge il numero di telefono al docente

"""


@app.route("/add_phone", methods=["POST"])
def add_phone_number():
    cf_docente = session.get("codicefiscale")
    data = request.get_json()
    number_to_add = data.get("number")
    try:
        add_number_aux(number_to_add, cf_docente)
        return jsonify(message="Numero di telefono aggiunto correttamente.")
    except Exception as e:
        return jsonify(
            message="Errore durante l'aggiunta del numero di telefono. Dettagli: "
            + str(e)
        )


"""
la funzione delete_phone_number() permette di eliminare un numero di telefono del docente
attraverso il metodo POST si riceve il numero di telefono da eliminare
successivamente si richiama la funzione delete_number_aux() che elimina il numero di telefono del docente

"""


@app.route("/delete_phone", methods=["POST"])
def delete_phone_number():
    cf_docente = session.get("codicefiscale")
    data = request.get_json()
    numero_telefono = data.get("number")
    try:
        delete_number_aux(numero_telefono, cf_docente)
        return jsonify(message="Numero di telefono eliminato correttamente.")
    except Exception as e:
        return jsonify(
            message="Errore durante l'eliminazione del numero di telefono. Dettagli: "
            + str(e)
        )


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Permission
@app.errorhandler(403)
def page_not_found(e):
    return render_template("403.html"), 403


"""
la funzione show_list_exam() permette di visualizzare la lista degli esami sostenuti dallo studente
viene richiamata la funzione show_list_exam_aux() che restituisce la lista degli esami sostenuti dallo studente
"""


@app.route("/stud/lista_esami_utente")
def show_list_exam():
    if "ruolo" in session and session["ruolo"] == "Studente":
        cf = session.get("codicefiscale")
        corsi = show_list_exam_aux(cf)
        # Nel caso il voto sia None, oppure assente la cella corrispondente nella tabella html risulterà essere vuota
        return render_template("lista_esami_utente.html", corsi=corsi)
    else:
        abort(403)


"""
la funzione prenotazioni_appelli() permette di visualizzare la lista degli appelli che lo studente può prenotare
viene richiamata la funzione prenotazioni_aux() che restituisce la lista degli appelli che lo studente può prenotare

"""


@app.route("/stud/prenotazioni_appelli", methods=["GET"])
def prenotazioni_appelli():
    if "ruolo" in session and session["ruolo"] == "Studente":
        if request.method == "GET":
            corsolaurea = session.get("corsoLaurea")
            matricola = session.get("matricola")
            righe_iniziali = prenotazioni_aux(corsolaurea, matricola)
            if righe_iniziali.__len__() != 0:
                session["Esame"] = righe_iniziali[0]["CodEsame"]
            else:
                return render_template(
                    "prenotazioni_appelli.html", righe=righe_iniziali
                )
        return render_template("prenotazioni_appelli.html", righe=righe_iniziali)
    else:
        abort(403)


"""
la funzione bacheca_appelli permette di visualizzare la lista degli appelli che lo studente può prenotare
viene richiamata la funzione bacheca_aux() che restituisce la lista degli appelli che lo studente ha prenotato

"""


@app.route("/stud/bacheca_prenotazione_appelli", methods=["GET"])
def bacheca_appelli():
    if "ruolo" in session and session["ruolo"] == "Studente":
        if request.method == "GET":
            codicefiscale = session.get("codicefiscale")
            righe_uniche = bacheca_aux(codicefiscale)
        return render_template("bacheca_prenotazione_appelli.html", righe=righe_uniche)
    else:
        abort(403)


"""
la funzione aggiungi_riga() permette di aggiungere un appello alla lista degli appelli che lo studente può prenotare
viene richiamata la funzione add_row_aux() che aggiunge un appello alla lista degli appelli che lo studente può prenotare
"""


@app.route("/aggiungi_riga", methods=["POST"])
def aggiungi_riga():
    riga = request.get_json()
    esame = riga.get("CodEsame")
    cf = session.get("codicefiscale")
    add_row_aux(esame, cf)
    return jsonify({"message": "Riga aggiunta con successo"})


"""
la funzione delete_appello() permette di eliminare un appello dalla lista degli appelli che lo studente può prenotare   
viene richiamata la funzione delete_appello_aux() che elimina un appello dalla lista degli appelli che lo studente può prenotare

"""


@app.route("/delete_appello", methods=["POST"])
def delete_appello():
    riga = request.get_json()
    esame = riga.get("CodEsame")
    delete_appello_aux(esame)
    return jsonify({"message": "Riga rimossa con successo"})


"""
la funzione exam_details() permette di visualizzare la lista degli esami sostenuti dallo studente
viene richiamata la funzione exam_details_aux() che restituisce la lista degli esami sostenuti dallo studente

"""


@app.route("/stud/bacheca_esiti", methods=["GET"])
def exam_details():
    if "ruolo" in session and session["ruolo"] == "Studente":
        if request.method == "GET":
            codicefiscale = session.get("codicefiscale")
            exam_list = exam_details_aux(codicefiscale)
        grouped_exam_list = {}
        for exam in exam_list:
            codice_corso = exam["codice_corso"]
            if codice_corso not in grouped_exam_list:
                grouped_exam_list[codice_corso] = []
            grouped_exam_list[codice_corso].append(exam)
        return render_template(
            "Bacheca_esiti.html", grouped_exam_list=grouped_exam_list
        )
    else:
        abort(403)


"""
la funzione home() permette di visualizzare il menù dello studente o del docente o dell'admin in base al ruolo
"""


@app.route("/home")
def home():
    if "ruolo" in session:
        if session["ruolo"] == "Studente":
            return redirect(url_for("index_studenti"))
        elif session["ruolo"] == "Docente":
            return redirect(url_for("index_docenti"))
        else:
            return redirect(url_for("administrator"))
    else:
        abort(404)


"""
la funzione log_out() permette di effettuare il logout
"""


@app.route("/log_out")
def log_out():
    session.clear()
    session["ruolo"] = None
    return redirect(url_for("index"))


"""
la funzione reset permette di resettare la password rimanendo in sessione,
se invece il ruolo è None o si è fuori sessione rediretta il sito a index
"""


@app.route("/reset")
def reset():
    if "ruolo" in session:
        if session["ruolo"] == None:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("resetpwd"))
    else:
        session.clear()
        return redirect(url_for("index"))


"""
la funzione ret, nel caso in cui venga visualizzata una pagina di errore (404 403 500),
tramite link "Return" l'utente torna all'index corrispondente al ruolo presente in sessione
"""


@app.route("/return")
def ret():
    if "ruolo" in session:
        if session["ruolo"] == "Studente":
            return redirect(url_for("index_studenti"))
        elif session["ruolo"] == "Docente":
            return redirect(url_for("index_docenti"))
        elif session["ruolo"] == "Admin":
            return redirect(url_for("administrator"))
        else:
            return redirect(url_for("index"))
    else:
        session.clear()
        return redirect(url_for("index"))

@app.route("/stud/accetta_voti", methods=["GET", "POST"])
def accetta():
    cf = session.get("codicefiscale")
    if "ruolo" in session and session["ruolo"] == "Studente":
        if request.method == "POST":
            data = request.get_json()
            print(data)    
            accetta_post(data, cf)
            return "ok"
        else:
            data_list = accetta_get(cf)

            return render_template('Accetta_rifiuta.html', data_list=data_list)
    else:
        abort(403)



if __name__ == "__main__":
    app.secret_key = "Dokkeabi"
    app.run()