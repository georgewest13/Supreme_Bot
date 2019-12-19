# Supreme_Bot-v1.1
# 12.19.19

from flask import Flask, render_template, request, url_for
from sup_bot import get_clothes
import threading, webbrowser
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/script/', methods=['GET', 'POST'])
def script():
  items = request.form.getlist('items')
  print(items)
  get_clothes(items)
  return '<h1>Secure the bag in Firefox</h1>'

if __name__ == '__main__':
  port = 5000 
  url  = "http://127.0.0.1:{0}".format(port)
  threading.Timer(1.25, lambda: webbrowser.open(url)).start()
  app.run(debug=False)
