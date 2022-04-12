from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return 'Hi There, The Crypto Price-Info Bot is running and online!'

def run():
  app.run(host = '0.0.0.0', port=8000)

def keep_running():
  t = Thread(target=run)
  t.start()