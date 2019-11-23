from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
from flask_sqlalchemy import SQLAlchemy 
import os
  
app = Flask(__name__) 
#database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

#db creation
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120)) 
    password = db.Column(db.String(80))


bot = ChatBot("royalbot", storage_adapter="chatterbot.storage.SQLStorageAdapter", logic_adapters=[
        "chatterbot.logic.BestMatch"
    ])
trainer = ChatterBotCorpusTrainer(bot)
trainer.train(
    "./data/health.yml",
    "./data/greetings.yml",
    "./data/headache.yml",
    "./data/cough.cold.yml",
    "./data/fever.yml",
    "./data/botprofile.yml",
    "./data/doctor.yml", 
    "./data/fracture.yml",
    "./data/generalhealth.yml"

)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/botdoctor")
def botdoctor():
    return render_template("botdoctor.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot.get_response(userText))

# login 

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("botdoctor"))
    return render_template("login.html")

# register 

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/About")
def about():
    return render_template("about-us.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/tologin")
def tologin():
    return render_template("login.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
