from flask import Flask, render_template, url_for, request


# Create Flask Instance
app = Flask(__name__)

#valori statici globali per test di add/delete
users = ['Utente 1', 'Utente 2', 'Utente 3']
@app.route('/')
def index():
    #first_name = "John"
    #stuff = "This is bold text"

    elenco_corsi_scientifici = ["Informatica", "Scienze Ambientali", "Chimica e tecnologie sostenibili", "Ingegneria Fisica", "Scienze e tecnologie per i beni culturali"]
    elenco_corsi_umanistici = ["Lettere", "Filosofia", "Storia", "Conservazione e gestione dei beni e delle attività culturali"]
    elenco_corsi_economici = ["Commercio estero e turismo", "Digital Management", "Economia aziendale", "Economia e commercio"]
    elenco_corsi_lingua = ["Lingue, civiltà e scienze del linguaggio", "Lingue, culture e società dell'Asia e dell'Africa mediterranea"]
    return render_template("index.html",
                            elenco_corsi_scientifici=elenco_corsi_scientifici,
                            elenco_corsi_economici=elenco_corsi_economici,
                            elenco_corsi_umanistici=elenco_corsi_umanistici,
                            elenco_corsi_lingua=elenco_corsi_lingua)

@app.route('/reset_pwd')
def resetpwd():
    return render_template("reset_pwd.html")

#localhost:5000/sign_up
@app.route('/sign_up')
def signUp():
    return render_template("sign_up.html")

#localhost:5000/login
@app.route('/login')
def login():
    return render_template("login.html")

#localhost:5000/user/John
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name = name)

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

@app.route('/Admin')
def administrator():
    return render_template('Admin.html')

@app.route('/Admin/delete_user')
def delete():
    return render_template('Delete_users.html', users=users)

@app.route('/Admin/add_user')
def add():
    return render_template('Add_users.html', users=users)

@app.route('/delete', methods=['POST'])
def delete_user():
    user_to_delete = request.form['user']
    if user_to_delete in users:
        users.remove(user_to_delete)
    return 'Utente eliminato con successo'

@app.route('/add', methods=['POST'])
def add_user():
    user_to_add = request.form['user']
    #aggiungere controllo se l'utente è gia presente nel db
    users.insert(len(users), user_to_add)
    return 'Utente aggiunto con successo'


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run()