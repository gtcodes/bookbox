from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello():
    return "hello world!"

@app.route("/", methods=['POST'])
def handle():
    print("current level is " + request.form['level'])
    return "got report! \ncurrent level is " + request.form['level']