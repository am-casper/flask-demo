from flask import Flask, request

app = Flask(__name__)


@app.post('/login')
def login():
    req = request.get_json()
    return req['username']+"\n"+req['password']


@app.get('/users')
def users():
    users = [
        {
            "username": "admin",
            "password": "admin"
        },
        {
            "username": "user",
            "password": "user"
        },
        {
            "username": "test",
            "password": "test"
        }
    ]
    return users

@app.get('/user')
def user():
    user = request.args.get('username')
    for u in users():
        if u['username'] == user:
            return u
        
    app.logger.info('User not found')
    return "User not found"
