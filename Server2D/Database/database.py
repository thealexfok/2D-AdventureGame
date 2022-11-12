import mysql.connector
from mysql.connector import errorcode
import json

def NewChar(name,charData):
    global _mydb
    global _mycursor
    sql = "INSERT INTO gamesave (name, chardata) VALUES (%s, %s)"
    val = (name, charData)
    _mycursor.execute(sql, val)
    _mydb.commit()

def Init():
    global _mydb
    global _mycursor

    
    try:
        _mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="admin",
            password="adminpass",
            #auth_plugin='mysql_native_password'
            )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something's wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        
    _mycursor = _mydb.cursor(buffered=True)
    _mycursor.execute("SHOW DATABASES")

    for result in _mycursor:
        if "adventuredatabase" in result:
            break

    else:
        _mycursor.execute("CREATE DATABASE adventuredatabase")
        _mycursor.execute("USE adventuredatabase")
        _mycursor.execute("CREATE TABLE gamesave (id INT  AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), chardata JSON)")
        NewChar("me", json.dumps({"x":320,"y":240}))

    _mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="admin",
            password="adminpass",
            database = "adventuredatabase"
            )
    _mycursor = _mydb.cursor(buffered = True)

def GetCharData(id):
    global _mycursor
    
    name="me"
    _mycursor.reset()
    _mycursor.execute(f"SELECT chardata FROM gamesave WHERE name='{name}'")
    result = _mycursor.fetchone()
    return result[0]

def GetCharPos(id):
    result = GetCharData(id)
    dict = json.loads(result)
    return dict['x'], dict['y']

def SetCharPos(id, x, y):
    global _mydb
    global _mycursor

    name = "me"
    if not isinstance(x, int) or not isinstance(y, int):
        return False

    j = {"x":x, "y":y}
    sql = "UPDATE gamesave SET chardata=%s WHERE name=%s"
    val = (json.dumps(j), name)
    _mycursor.reset()
    _mycursor.execute(sql, val)
    _mydb.commit()

    return True

def ClearSave():
    global _mydb
    global _mycursor
    _mycursor.execute("DELETE FROM gamesave")
    _mydb.commit()