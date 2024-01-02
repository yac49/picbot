from flask import Flask
from threading import Thread
from bot import run_bot

app = Flask('')


@app.route('/')
def home():
  return "I'm alive"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()

if __name__ == '__main__':
    keep_alive()
    run_bot()