from flask import Flask, render_template, url_for


#Create an instance of the Flask class

app = Flask(__name__)

#Create a route decorator
@app.route('/')
#def index():
#    return "<h1>Hello World!</h1>"

#safe
#capitalize
#lower
#upper
#title
#trim
#striptags


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

#localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)

#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/resetpwd')
def resetpwd():
    return render_template("resetpwd.html")