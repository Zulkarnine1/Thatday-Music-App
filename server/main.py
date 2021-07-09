from flask import Flask, render_template, redirect, url_for, flash,request, abort

app = Flask(__name__)

# Temp Constants

Cards = [
    {
        "id":0,
        "name":"james Birthday",
        "date":"14 March 2015",
        "by":"Toby Flenderson",
        "quote":"The Random Quotes API allows you to access an extensive collection of more than 60,000 quotes and display them on your application. API features: The API comes with endpoints for getting random quotes and getting a list of all the available quotes categories.",
        "img":"https://images.unsplash.com/photo-1624081185839-d41129ed7df2?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max",
        "playlist":"http://www.google.com"
    },
{
        "id":1,
        "name":"Alises Wedding",
        "date":"19 October 2015",
        "by":"Alison Brie",
        "quote":"The Random Quotes API allows you to access an extensive collection of more than 60,000 quotes and display them on your application. API features: The API comes with endpoints for getting random quotes and getting a list of all the available quotes categories.",
        "img":"https://phillipbrande.files.wordpress.com/2013/10/random-pic-14.jpg",
        "playlist":"http://www.google.com"
    },

]

@app.route("/")
def home():
    return render_template("home.html",loggedin=True, all_cards=Cards)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000,debug=True)
