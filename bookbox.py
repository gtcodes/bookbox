from flask import Flask, request
from messaging import SendMessage, SENDER, RECEIVER

app = Flask(__name__)

# value that will cause alert
LIMIT = 80

@app.route("/", methods=['GET'])
def hello():
    return "hello world!"

@app.route("/", methods=['POST'])
def handle():
    level = request.form['level']
    print("current level is " + level)

    if int(level) >= LIMIT:
        sendAlert(level)
    return "got report! \ncurrent level is " + level

def sendAlert(level):
    subject = "The bookbox is almost full!"
    msgHtml = '<h1>The bookbox is almost full!</h1>' \
              '<br><p>The current level is: ' \
              '<b>' + level + '</b></p>'
    msgPlain = 'The bookbox is almost full! current level is ' + level
    SendMessage(SENDER, RECEIVER, subject, msgHtml, msgPlain)