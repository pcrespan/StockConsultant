from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import psycopg2

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


class dbConnection:
    @staticmethod
    def getConnection():
        conn = psycopg2.connect(
                host = "localhost",
                database = "api",
                user = "postgres",
                password = "postgres"
                )

        cursor = conn.cursor()
        return conn, cursor

    @staticmethod 
    def closeConnection(conn, cursor):
        try:
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Couldn't close connection: ", e)
            return False


def validateRegister(usr, pwd, pwdConf):
    conn, cursor = dbConnection.getConnection()

    if not usr or not pwd or not pwdConf or pwd != pwdConf:
        dbConnection.closeConnection(conn, cursor)
        return False
        
    cursor.execute("SELECT id FROM users WHERE username = %s;", (usr, ))
    usr_exists = cursor.fetchall()
    if usr_exists or pwd != pwdConf:
        dbConnection.closeConnection(conn, cursor)
        return False
    dbConnection.closeConnection(conn, cursor)
    return True
    


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        usr = request.form.get("user")
        pwd = request.form.get("password")
        pwdConf = request.form.get("confirmation")


