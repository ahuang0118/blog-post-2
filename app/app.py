# to run this website and watch for changes: 
# $ export FLASK_ENV=development; flask run
# set FLASK_ENV=development & flask run (for PC)

from flask import Flask, g, render_template, request
import sqlite3



# Create web app, run with flask run
# (set "FLASK_ENV" variable to "development" first!!!)

app = Flask(__name__)

# Create main page (fancy)

@app.route('/')
def main():
    return render_template('base.html')

# functions to storage messages
def get_message_db():
    # with app.app_context():
        if hasattr(g,"message_db") == False:
            g.message_db = sqlite3.connect("message_db.sqlite")
        cursor = g.message_db.cursor()
        cmd = \
        """ CREATE TABLE IF NOT EXISTS message(id, handle, message) """
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    db = get_message_db()
    cursor = db.cursor()
    count = db.cursor().execute("SELECT * From message")
    id = len(count.fetchall()) + 1
    message = request.form['message']
    handle = request.form['handle']
    if message and handle:
        cursor.execute("INSERT INTO message VALUES(?, ?, ?)" , (id, handle, message))
        db.commit()
    db.close()

# Page with form

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    with app.app_context():
        if request.method == 'GET':
            return render_template('submit.html')
        else:
            try:
                insert_message(request)
                if request.form['handle'] and request.form['message']:
                      return render_template('submit.html', thanks = True)
                else:
                    return render_template('submit.html', error = True)
            except:
                return render_template('submit.html', error = True)



def random_messages(n=3):
    db = get_message_db()
    cursor = db.cursor()
    count = db.cursor().execute("SELECT * From message")
    total_rows = len(count.fetchall())
    if n > total_rows:
        n = total_rows
    cmd = """SELECT handle, message FROM message ORDER BY RANDOM() LIMIT %d""" %n
    cursor.execute(cmd)
    data = cursor.fetchall()
    db.close()
    return data

@app.route('/view/')
def view():
    return render_template('view.html', data=random_messages())
    
# File uploads and interfacing with complex Python
# basic version


