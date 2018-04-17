# Server
The server is responsible for receiving reports from the device and deciding if the box should be emptied or not. If it should, the server will send an email to the joker-teachers prompting them to take action.

## Setup
1. install python 
1. install flask `pip install flask`
1. follow step 1 and 2 of this guide https://developers.google.com/gmail/api/quickstart/python

## Usage
1. run `python bookbox.py`
3. the first time this is run a browser opens, just follow the steps and allow the app to send mails
3. notice that a new file `credentials.json has been created, whenever you need to change user or in any way change the credentials, just delete this file and run the program again

