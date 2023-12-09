from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World! Debugged!'

@app.route('/hello/<name>')
def hello(name):
    return f'<h1>Hello, {escape(name)}!</h1>'

@app.route('/user/<username>')
def use(username):
    return f'User is {escape(username)}'

@app.route('/post/<int:post_id>')
def post(post_id):
    return f'Post id is {post_id}'

@app.route('/path/<path:add>')
def show_path(add):
    return f'Path is {escape(add)}'

@app.route('/string/<string:my_str>')
def show_string(my_str):
    return f'String is {escape(my_str)}'