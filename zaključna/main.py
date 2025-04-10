from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
app.secret_key = "skrivnost"

db = TinyDB("uporabniki.json")
users = db.table("uporabniki")
user = Query()

@app.route("/")
def index():
    return render_template('index.html')

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
            return jsonify({'succes': False, 'error': 'Uporabnik že obstaja'})
        
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