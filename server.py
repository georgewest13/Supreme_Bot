# Supreme_Bot-v1.1
# 12.19.19

from flask import Flask, render_template, request, url_for
import sup_bot
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/script/', methods=['GET', 'POST'])
def script():
  items = request.form.getlist('items')
  print(items)
  sup_bot.get_clothes(items)
  return '<h1>Secured the bag</h1>'

if __name__ == '__main__':
  app.run(debug=True)
