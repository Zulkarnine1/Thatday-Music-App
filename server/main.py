# Imports
from flask import Flask, render_template, redirect, url_for, flash,request, abort
from flask import jsonify
from flask_login import LoginManager, UserMixin, login_required, current_user, logout_user, login_user
from configs.dbconfig import DBConfig
from env import DB_CONNECTION, SALT_ROUNDS, HASH_METHOD, SECRET_KEY, CLOUDINARY_API_SECRET,CLOUDINARY_API_KEY,CLOUDINARY_CLOUD_NAME
from models import load_class_User, load_class_Playlist, load_class_Card, get_LIKES_table
from utilities.get_quote import get_quote
from utilities.playlist_utility import PlaylistManager
from werkzeug.security import generate_password_hash, check_password_hash
from appconstants import SAMPLE_IMAGES_AVATAR
import random
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from datetime import datetime
from functools import wraps
from custom_decors.card_processor import card_processor





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

def card_creator_only(f):
    @wraps(f)
    def creator_only_decor(*args, **kwargs):
        params = dict(kwargs)
        card = Card.query.get(params["id"])
        if(current_user.id==card.creator):
            return f(*args,**kwargs,card=card)
        else:
            return redirect(url_for("errorFunc", error="401:Unauthorized request."))

    return creator_only_decor


# Media Manager configs
cloudinary.config(cloud_name = CLOUDINARY_CLOUD_NAME,api_key = CLOUDINARY_API_KEY,
                  api_secret = CLOUDINARY_API_SECRET,secure = True)






# Load models
get_LIKES_table(db)
User = load_class_User(db)
Playlist = load_class_Playlist(db)
Card = load_class_Card(db)

db.create_all()

# Playlist manager

playlist_manager = PlaylistManager(Playlist)

# Temp Constants




# Constants

MONTHS = {
    "01":"January",
    "02":"February",
    "03":"March",
    "04":"April",
    "05":"May",
    "06":"June",
    "07":"July",
    "08":"August",
    "09":"September",
    "10":"October",
    "11":"November",
    "12":"December",
}


"""
       *************        =========================================================        *************
                            ====================== Routes Section ===================
                            =========================================================
                            
"""




"""
                            =========================================================
                            ==================== General Routes =====================
                            =========================================================
"""


@app.route("/")
def home():
    if current_user.is_authenticated:
        Cards = card_processor(Card.query.all()[::-1], current_user.id)
    else:
        Cards = card_processor(Card.query.all()[::-1], None)
    return render_template("home.html",loggedin=current_user.is_authenticated, all_cards=Cards, user_data=current_user)


"""
                            =========================================================
                            =============== Authentication Routes ===================
                            =========================================================
"""


@app.route("/login", methods=["GET","POST"])
def login():
    try:
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
    except:
        flash("Something went wrong while logging in, please try again.")
        return redirect("/login")


@app.route("/register", methods=["GET","POST"])
def register():
    try:
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
    except:
        flash("Something went wrong while registering, please try again.")
        return redirect("/register")




@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")




"""
                            =========================================================
                            ================ Playlist Card Routes ===================
                            =========================================================
"""


@app.route("/createcard", methods=["GET","POST"])
@login_required
def createcardroute():
    if (request.method == "GET"):
        return render_template("createcard.html", loggedin=current_user.is_authenticated, user_data=current_user,hide_create_card_link=True)
    elif (request.method=="POST"):
        # Validation of inputs
        date = request.form["date"]
        title = request.form["title"]
        if(date and title):
            date_format = "%Y-%m-%d"
            dateinformat = datetime.strptime(date,date_format)
            now = datetime.now()
            if(dateinformat<=now and len(title)<31):
                # Create playlist
                # Playlist
                no_error, link1 = playlist_manager.get_playlist(date,db)
                if(no_error):
                    try:
                        # Get random image and quote if doesnt exist
                        if request.files['file']:
                            f = request.files['file']
                            f.save(f.filename)
                            link = cloudinary.uploader.upload(f.filename,folder=f"thatday/card")["url"]
                            os.remove(f.filename)
                        else:
                            link = cloudinary.uploader.upload("https://source.unsplash.com/random",folder=f"thatday/card")["url"]
                        if(not request.form["quote"]):
                            quote = get_quote(10)
                        else:
                            quote = request.form["quote"]

                        year,m,d = tuple(date.split("-"))
                        if (d[0]=="0"):
                            d = d[1]
                        newCard = Card(creator=current_user.id,img=link,title=title,dateformatted=f"{d} {MONTHS[m]} {year}",date=date,by=current_user.name,playlist=link1,quote=quote,likes=0)
                        db.session.add(newCard)
                        db.session.commit()
                        return redirect("/")
                    except Exception as e:
                        return redirect(
                            url_for("errorFunc", error="500:Internal server error, please try again later."))
                else:
                    return redirect(
                        url_for("errorFunc", error="500:Internal server error, please try again later."))
            else:
                return redirect(url_for("errorFunc",error="422:Invalid input,date should be in present or past . "))

        else:
            return redirect(url_for("errorFunc", error="422:Invalid input,missing date or title. "))



# Edit Card
@app.route("/editcard/<id>", methods=["GET","POST"])
@card_creator_only
def edit_card(id, card):
    if(request.method=="GET"):
        try:
            if (not card):
                return redirect(url_for("errorFunc", error="404:Couldn't find playlist card for this ID"))
            else:
                return render_template("editcardpage.html", card=card, loggedin=current_user.is_authenticated,
                                       user_data=current_user)
        except Exception as e:
            return redirect(url_for("errorFunc", error="500:Internal server error please try again later."))

    elif (request.method == "POST"):
        try:
            # Check if title has been changed and if new title is valid
            if(request.form["title"] and len(request.form["title"])<31):
                if(request.form["title"]!=card.title):
                    card.title = request.form["title"]
            else:
                return redirect(url_for("errorFunc", error="422:Invalid input,Length of title too long. "))

            if (request.form["quote"] and len(request.form["quote"])<251):
                if (request.form["quote"] != card.quote):
                    card.quote = request.form["quote"]
            else:
                return redirect(url_for("errorFunc", error="422:Invalid input,Length of quote too long. "))
            date = request.form["date"]
            if (date):
                if (date != card.date):
                    date_format = "%Y-%m-%d"
                    dateinformat = datetime.strptime(date, date_format)
                    now = datetime.now()
                    if (dateinformat <= now):
                        no_error, link1 = playlist_manager.get_playlist(date, db)
                        if(not no_error):
                            return redirect(url_for("errorFunc", error="500:Internal server error, please try again later."))
                        else:
                            card.playlist = link1
                            card.date = date
                            year, m, d = tuple(date.split("-"))
                            if (d[0] == "0"):
                                d = d[1]
                            card.dateformatted = f"{d} {MONTHS[m]} {year}"
                    else:
                        return redirect(
                            url_for("errorFunc", error="422:Invalid input,date should be in present or past . "))


            if request.files['file']:
                f = request.files['file']
                f.save(f.filename)
                link = cloudinary.uploader.upload(f.filename, folder=f"thatday/card")["url"]
                os.remove(f.filename)
                card.img = link

            db.session.commit()
            return redirect(f"/card/{card.id}")
        except Exception as e:
            return redirect(url_for("errorFunc", error="500:Internal server error, please try again later."))




# Like unlike cards

@app.route("/like/<id>", methods=["PUT"])
def card_like(id):
    if(request.method=="PUT"):
        try:
            card = Card.query.get(id)
            user = User.query.get(current_user.id)
            cards_liked = user.liked_cards
            if(card in cards_liked):

                card.likes = card.likes - 1
                user.liked_cards.remove(card)
            else:
                card.likes = card.likes + 1
                user.liked_cards.append(card)
            likes = card.likes
            db.session.commit()
            return jsonify({"message":"Successfully liked card.","status":True,"likes":likes}), 200
        except Exception as e:
            return jsonify({"message":"Couldn't like card. Internal server error.","status":False,"likes":likes}), 500








# Get card
@app.route("/card/<id>")
def get_card(id):
    try:
        card = card_processor([Card.query.get(id)], current_user.id)
        if(not card):
            return redirect(url_for("errorFunc",error="404:Couldn't find playlist card for this ID"))
        else:
            return render_template("cardpage.html", all_cards=card,loggedin=current_user.is_authenticated, user_data=current_user)
    except Exception as e:
        print(e)
        return redirect(url_for("errorFunc", error="500:Internal server error please try again later."))




# Delete card
@app.route("/deletecard/<id>", methods=["DELETE"])
@card_creator_only
def delete_card(id, card):
    try:
        db.session.delete(card)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return redirect(url_for("errorFunc", error="500:Internal server error please try again later."))


# Error Handling

@app.route("/error/<error>")
def errorFunc(error):
    e_code = error.split(":")[0]
    e_msg = error.split(":")[1]
    return render_template('error.html',ecode=e_code,msg=e_msg), e_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
