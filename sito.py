from flask import Flask, render_template


# Create Flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

#def index():
#    return "<h1>Hello w!!!</h1>"

#FILTERS GINGER :D jinja
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags


def index():
    first_name= "John"
    stuff = "this is BOLD text"

    favourite_pizza=["Pepperoni","Cheese","Mushrooms",41]
    return render_template("index.html",
                            first_name = first_name,
                            stuff = stuff,
                            favourite_pizza = favourite_pizza)

#localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name = name)

#localhost:5000/sign_up
@app.route('/sign_up')

def signUp():
    return render_template("sign_up.html")

#localhost:5000/login
@app.route('/login')

def login():
    return render_template("login.html")

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
