from flask import Flask, request
from messaging import SendMessage, SENDER, RECEIVER
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

# value that will cause alert
LIMIT = 80

@app.route("/", methods=['GET'])
def hello():
    return "hello world!"

@app.route("/", methods=['POST'])
def handle():
    print(request.form)
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

class Alarm():
    def __init__(self):
        self.counter = 0

    def check_if_report_or_alarm(self):
        self.counter = self.counter + 1
        print(self.counter)
        if self.counter > 120:
            print("no report received the last two hours")
            sendBatteryWarning(self.counter)

    def sendBatteryWarning(self, counter):
        subject = "WARNING: Bookbox is not reporting, battery may be low"
        msgHtml = '<h1>Bookbox is not reporting</h1>' \
              '<br><p>No report has been received in ' \
              '<b>' + counter + '</b> seconds</p>' \
              'This can be due to several faults: ' \
              '<ul>' \
              '<li>Battery low: please charge the battery by plugging in the device using a micro-usb cable </li>' \
              '<li>Lost connection to wifi: Make sure the router in personalrum 1 is on and working</li>' \
              '<li>Other problem: contact previous joker-teachers</li>' \
              '</ul>' 
        msgPlain = 'Bookbox is not reporting, check battery and wifi. Doesn\'t work? contact previous joker-teachers'
        SendMessage(SENDER, RECEIVER, subject, msgHtml, msgPlain)

alarm = Alarm()
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=alarm.check_if_report_or_alarm,
    trigger=IntervalTrigger(seconds=60),
    id='battery_low',
    name='Check if a report has been received the last two hours or alarm that the device is not reporting',
    replace_existing=True)

atexit.register(lambda: scheduler.shutdown())