# Imports
from flask import Flask, render_template, redirect, url_for, flash,request, abort
from flask_login import LoginManager, UserMixin, login_required, current_user, logout_user, login_user
from configs.dbconfig import DBConfig
from env import DB_CONNECTION, SALT_ROUNDS, HASH_METHOD, SECRET_KEY, CLOUDINARY_API_SECRET,CLOUDINARY_API_KEY,CLOUDINARY_CLOUD_NAME
from models import load_class_User
from werkzeug.security import generate_password_hash, check_password_hash
from appconstants import SAMPLE_IMAGES_AVATAR
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os




app = Flask(__name__)

# Configurations

app.config['SECRET_KEY'] = SECRET_KEY

# DB configs
dbconfig = DBConfig(app)
db,app = dbconfig.connect(DB_CONNECTION)

# Login Manager configs
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Media Manager configs
cloudinary.config(cloud_name = CLOUDINARY_CLOUD_NAME,api_key = CLOUDINARY_API_KEY,
                  api_secret = CLOUDINARY_API_SECRET,secure = True)


# Load models

User = load_class_User(db)

db.create_all()



# Temp Constants

Cards = [
    {
        "id":0,
        "title":"James Birthday",
        "date":"14 March 2015",
        "by":"Toby Flenderson",
        "quote":"The Random Quotes API allows you to access an extensive collection of more than 60,000 quotes and display them on your application. API features: The API comes with endpoints for getting random quotes and getting a list of all the available quotes categories.",
        "img":"https://images.unsplash.com/photo-1624081185839-d41129ed7df2?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max",
        "playlist":"http://www.google.com"
    },
{
        "id":1,
        "title":"Alises Wedding",
        "date":"19 October 2015",
        "by":"Alison Brie",
        "quote":"The Random Quotes API allows you to access an extensive collection of more than 60,000 quotes and display them on your application. API features: The API comes with endpoints for getting random quotes and getting a list of all the available quotes categories.",
        "img":"https://phillipbrande.files.wordpress.com/2013/10/random-pic-14.jpg",
        "playlist":"http://www.google.com"
    },

]

@app.route("/")
def home():

    return render_template("home.html",loggedin=current_user.is_authenticated, all_cards=Cards, user_data=current_user)


@app.route("/login", methods=["GET","POST"])
def login():
    if not current_user.is_authenticated:
        if request.method == "GET":
            return render_template("login.html")
        elif request.method == "POST":
            quser = User.query.filter_by(username=request.form.get('username')).first()
            if quser:
                if(check_password_hash(quser.password, request.form.get('password'))):
                    login_user(quser)
                    del current_user.password
                    return redirect("/")

                else:
                    flash("Invalid credentials, please try again.")
                    return redirect(url_for("login"))
    else:
        return redirect("/")


@app.route("/register", methods=["GET","POST"])
def register():
    if not current_user.is_authenticated:
        if request.method == "GET":
            return render_template("register.html")
        if request.method == "POST":
            if User.query.filter_by(username=request.form.get('username')).first():
                flash("There is a user already registered with the username, please try again.")
                return redirect(url_for("register"))
            else:
                if request.files['file']:
                    f = request.files['file']
                    f.save(f.filename)
                    link = cloudinary.uploader.upload(f.filename,folder=f"thatday/user")["url"]
                    os.remove(f.filename)
                else:
                    link = random.choice(SAMPLE_IMAGES_AVATAR)
                name = request.form["name"]
                username = request.form["username"]
                password = generate_password_hash(request.form["password"],method=HASH_METHOD, salt_length=SALT_ROUNDS)
                new_user = User(name=name,username=username,password=password,img=link)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                del current_user.password

                return redirect("/")
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")




if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000,debug=True)
