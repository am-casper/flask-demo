from flask import Flask, request
from db import create_table, connect_db, close_db
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app) 


create_table()

@app.route('/create', methods=['POST'])
def create():
    req = request.get_json()
    conn, cur = connect_db()
    
    # Get the data from the request
    name = req['name']
    password = req['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 

    # Insert the data into the table
    cur.execute('''INSERT INTO users (name, password) VALUES (%s, %s)''', (name, hashed_password))

    
    close_db(conn, cur)

    return {
        "name": name,
        "hashed_password": hashed_password
    }
    
@app.route('/login', methods=['GET'])
def login():
    req = request.get_json()
    
    
    # Get the data from the request
    name = req['name']
    password = req['password']
    
    result =  authorize(name, password)
    
    return {
        "remark":name + " " +result
    }
    
    
    
@app.route('/update', methods=['PUT'])
def update():
    req=request.get_json()
    
    # Get the data from the request
    name = req['name']
    password = req['password']
    result =  authorize(name, password)
    if result != "Login successful":
        return {
            "remark":result
        }
    try:
        newName = req['newName']
    except:
        newName = name
    try:
        newPassword = req['newPassword']
    except:
        newPassword = password
    hashed_password = bcrypt.generate_password_hash(newPassword).decode('utf-8') 

    # Insert the data into the table
    conn, cur = connect_db()
    cur.execute('''UPDATE users SET password = %s, name= %s WHERE name = %s''', (hashed_password,newName, name))
    close_db(conn, cur)

    return {
        "name": newName,
        "hashed_password": hashed_password
    }
    
@app.route('/delete', methods=['DELETE'])
def delete():
    req = request.get_json()
    name = req['name']
    password = req['password']
    result =  authorize(name, password)
    if result != "Login successful":
        return {
            "remark":result
        }
    conn, cur = connect_db()
    cur.execute('''DELETE FROM users WHERE name=%s''', (name,))
    close_db(conn, cur)
    return {
        "remark": f"User {name} deleted"
    }
    
    
def authorize(name, password):
    conn, cur = connect_db()
    cur.execute('''SELECT * FROM users WHERE name = %s''', (name,))
    user = cur.fetchone()
    close_db(conn, cur)
    if user:
        if bcrypt.check_password_hash(user[2], password):
            return "Login successful"
        else:
            return "Wrong password"
    else:
        return "User not found"