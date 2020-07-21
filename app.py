from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import trello_items as trello
import logging

app = Flask(__name__)
app.config.from_object('flask_config.Config')
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    items = trello.get_items()
    return render_template('index.html', items = items)

@app.route('/items/new', methods=['POST'])
def add_item():
    trello.add_item(
        title = request.form['title'],
        desc  = request.form['description'],
        due   = request.form['due']
    )
    return redirect(url_for('index')) 

@app.route('/items/<id>/complete')
def complete_item(id):
    trello.complete_item(id)
    return redirect(url_for('index')) 


if __name__ == '__main__':
    app.run()
