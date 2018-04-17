# Bookbox
This repository is for the bookbox notification system.
In the bookbox there is (or will be) a microcontroller (adafruit feather huzzah based on esp8266) that is connected to the wifi. This will, once a day, measure the amount of books in the box and report it to the webserver running on the network. 
The webserver will send an email to joker@gtg.se to notify them to empty the box.

## Setup
1. install python 
1. install flask `pip install flask`
1. follow step 1 and 2 of this guide https://developers.google.com/gmail/api/quickstart/python
2. run `python bookbox.py`
3. a browser opens, just follow the steps and allow the app to send mails
3. notice that a new file `credentials.json has been created, whenever you need to change user or in any way change the credentials, just delete this file and run the program again

## Usage
