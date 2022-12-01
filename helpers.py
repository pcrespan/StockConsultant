import psycopg2
from werkzeug.security import check_password_hash
from functools import wraps
import jwt


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


    @staticmethod
    def commitChanges(conn, cursor):
        cursor.commit()
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
    if check_password_hash(userInfo[0][2], pwd):
        return True
    return False


def getUser(usr):
    conn, cursor = dbConnection.getConnection()
    cursor.execute("SELECT id, password FROM users WHERE username = %s;", (usr, ))
    dbConnection.closeConnection(conn, cursor)
    userInfo = cursor.fetchall()
    return userInfo


