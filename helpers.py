import psycopg2
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from api import *
import jwt


class dbConnection:
    @staticmethod
    def getConnection():
        conn = psycopg2.connect(
                host = "localhost",
                database = "api",
                user = "enid",
                password = "stockapi"
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


    @staticmethod
    def commitChanges(conn, cursor):
        conn.commit()
        dbConnection.closeConnection(conn, cursor)


# Create checkUser function to simplify
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


def registerUser(usr, hashPwd):
    conn, cursor = dbConnection.getConnection()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (usr, hashPwd))
    dbConnection.commitChanges(conn, cursor)


# Needs refactoring
def validateLogin(usr, pwd):
    userInfo = getUser(usr)
    if check_password_hash(userInfo[0][1], pwd):
        return True
    return False


def getUser(usr):
    conn, cursor = dbConnection.getConnection()
    cursor.execute("SELECT id, password FROM users WHERE username = %s;", (usr, ))
    userInfo = cursor.fetchall()
    dbConnection.closeConnection(conn, cursor)
    return userInfo


def genToken(usr, SECRET_KEY):
    userInfo = getUser(usr)
    tokenExpire = datetime.utcnow() + timedelta(minutes = 30)
    print(tokenExpire)

    token = jwt.encode({
        "uid": userInfo[0][0],
        "exp": tokenExpire
    }, SECRET_KEY)

    return token


def getStock(stockSymbol):
    soup = getStockSoup(stockSymbol)
    stockInfo = getStockInfo(soup)
    return stockInfo
