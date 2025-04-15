from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
app.secret_key = "skrivnost"

db = TinyDB("uporabniki.json")
users = db.table("uporabniki")
vozila = db.table("vozila")
ocene = db.table("ocene")
User = Query()

if len(vozila) == 0:
    vozila.insert_multiple([
        {"ime": "BMW M4", "lokacija": "Ljubljana", "tip": "Avto", "priljubljenost": 10},
        {"ime": "Audi RS5", "lokacija": "Maribor", "tip": "Avto", "priljubljenost": 9},
        {"ime": "Ford Mustang", "lokacija": "Celje", "tip": "Avto", "priljubljenost": 8},
        {"ime": "Renault Clio RS", "lokacija": "Koper", "tip": "Avto", "priljubljenost": 7}
    ])

if len(ocene) == 0:
    ocene.insert_multiple([
        {"uporabnik": "lana", "vozilo": "BMW M4", "mnenje": "Res hiter in udoben!", "ocena": 5},
        {"uporabnik": "miha", "vozilo": "Ford Mustang", "mnenje": "Zvok motorja je top!", "ocena": 4},
        {"uporabnik": "eva", "vozilo": "Renault Clio RS", "mnenje": "Mali športnik – zakon!", "ocena": 4}
    ])

@app.route("/")
def index():
    prikazana_vozila = sorted(vozila.all(), key=lambda x: x['priljubljenost'], reverse=True)
    mnenja = ocene.all()
    return render_template("index.html", vozila=prikazana_vozila, ocene=mnenja)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(User.username == username)

        if user:
            if user['password'] == password:
                session['username'] = username
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'error':'Napačno geslo'})
        else:
            return jsonify({'success': False, 'error':'Uporabnik ne obstaja'})
    return render_template('login.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 

        if users.get(User.username == username):
            return jsonify({'success': False, 'error': 'Uporabnik že obstaja'})
        
        users.insert({'username': username,'password': password})
        session['username'] = username
        return jsonify({'success': True})
    
    return render_template('signup.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__=="__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)