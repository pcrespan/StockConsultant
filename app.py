from flask import Flask, jsonify, make_response, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import generate_password_hash
import jwt
import psycopg2
from helpers import *


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = ""
ALGORITHM = "HS256"
Session(app)


def jwtRequired(f):
    @wraps(f)
    def checkToken(*args, **kwargs):
        accessToken = request.form.get("accessToken")

        if not accessToken:
            return jsonify({"message": "No token provided"})
        
        # Verify token, if it's invalid, raises error
        try:
            requestInfo = jwt.decode(accessToken, app.config["SECRET_KEY"], algorithms = ALGORITHM)
            print(requestInfo)
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            return jsonify({"message": "Invalid token"})
    return checkToken


# Error here, find a way to receive info without needing forms
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        usr = request.form.get("username")
        pwd = request.form.get("password")
        pwdConf = request.form.get("confirmation")

        if not validateRegister(usr, pwd, pwdConf):
            return redirect("/register")

        hashPwd = generate_password_hash(pwd)
        registerUser(usr, hashPwd)
        return make_response("User registered", 200)
    else:
        return render_template("register.html")


# Still need to generate JWT token, needs refactoring
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        usr = request.form.get("username")
        pwd = request.form.get("password")

        if usr and pwd and validateLogin(usr, pwd):
            # Generate jwt token
            token = genToken(usr, app.config["SECRET_KEY"])
            return {"token": token}
        return redirect("/login")
    else:
        return render_template("login.html")


@app.route("/", methods = ["GET", "POST"])
@jwtRequired
def index():
    pass
    
