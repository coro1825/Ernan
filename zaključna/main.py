from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "skrivnost"

db = TinyDB("uporabniki.json")
users = db.table("uporabniki")
vozila = db.table("vozila")
ocene = db.table("ocene")
rezervacije = db.table("rezervacije")
User = Query()

vozila.truncate()
vozila.insert_multiple([
    {"id": 1, "ime": "BMW M4",           "lokacija": "Ljubljana", "tip": "Avto",  "priljubljenost": 10, "cena_na_dan": 100},
    {"id": 2, "ime": "Audi RS5",         "lokacija": "Maribor",   "tip": "Avto",  "priljubljenost":  9, "cena_na_dan":  90},
    {"id": 3, "ime": "Ford Mustang",     "lokacija": "Celje",     "tip": "Avto",  "priljubljenost":  8, "cena_na_dan":  85},
    {"id": 4, "ime": "Renault Clio RS",  "lokacija": "Koper",     "tip": "Avto",  "priljubljenost":  7, "cena_na_dan":  70},
    {"id": 5, "ime": "KTM Duke 390",         "lokacija": "Ljubljana", "tip": "Motor", "priljubljenost":  9, "cena_na_dan":  60},
    {"id": 6, "ime": "VW Transporter",   "lokacija": "Maribor",   "tip": "Kombi", "priljubljenost":  6, "cena_na_dan":  65},
])



@app.route("/")
def index():
    prikazana_vozila = sorted(vozila.all(), key=lambda x:x['priljubljenost'], reverse=True)
    mnenja = ocene.all()
    return render_template('index.html', vozila=prikazana_vozila, ocene=mnenja)

@app.route("/vozila")
def vozila_stran():
    return render_template('vozila.html')

@app.route("/rezervacija")
def rezervacija():
    if 'username' not in session:
        return redirect(url_for("login"))
    vozila_vsa = vozila.all()
    print("DEBUG vozila_vsa", vozila_vsa)
    return render_template('rezervacija.html', vozila=vozila_vsa)

#iskanje oz rezerviranje prevoznih sredstev glede na datum
@app.route("/api/razpolozljiva-vozila")
def razpolozljiva():
    zacetek = request.args.get("zacetek")
    konec =request.args.get("konec")
    razpolozljiva_vozila = []
    for v in vozila.all():
        if v['tip'] not in ["Avto", "Kombi", "Motor"]:
            continue
        id_v = v['id']
        kolizija = False
        for r in rezervacije.search(Query().vozilo_id == id_v):
            z = datetime.strptime(zacetek, "%Y-%M-%d")
            k = datetime.strptime(konec, "%Y-%M-%d")
            z_r = datetime.strptime(r['zacetek'], "%Y-%M-%d")
            k_r = datetime.strptime(r['konec'], "%Y-%M-%d")
            if (z <= k_r and k >= z_r):
                kolizija = True
                break
        if not kolizija:
            razpolozljiva_vozila.append(v)
    return jsonify(razpolozljiva_vozila)

#iskanje prevoznih sredstev glede na lokacijo in tip vozila
@app.route("/api/iskanje")
def iskanje():
    tip = request.args.get("tip")
    lokacija = request.args.get("lokacija")
    min_ocena = request.args.get("min_ocena", type=float)

    rezultati = []

    for v in vozila.all():
        if tip and v["lokacija"] != lokacija:
            continue

        vozilo_ocene = [float(o["ocena"]) for o in ocene.all() if o.get("vozilo_id") == v["id"] and "ocena" in o]
        povprecje = sum(vozilo_ocene) / len(vozilo_ocene) if vozilo_ocene else 0

        if min_ocena and povprecje < min_ocena:
            continue

        v["povprecna_ocena"] = round(povprecje, 2)
        rezultati.append(v)

        return jsonify(rezultati)
    

@app.route("/api/rezerviraj", methods=['POST'])
def rezerviraj():
    if 'username' not in session:
        return jsonify({'success': False, 'error': 'Niste prijavljeni'}), 401
    
    data = request.json
    vozilo_id = int(data.get('vozilo_id'))
    zacetek = data.get('zacetek')
    konec = data.get('konec')

    if not vozilo_id or not zacetek or not konec:
        return jsonify({'success': False, 'error': 'manjkajo podatki'})
    
    z = datetime.strptime(zacetek, "%Y-%m-%d")
    k = datetime.strptime(konec, "%Y-%m-%d")

    for r in rezervacije.search(Query().vozilo_id == vozilo_id):
        z_r = datetime.strptime(r['zacetek'], "%Y-%m-%d")
        k_r = datetime.strptime(r['konec'], "%Y-%m-%d")
        if (z <= k_r and k >= z_r):
            return jsonify({'success': False, 'error': 'Vozilo je že rezervirano v tem terminu'})
        
    rezervacije.insert({
        'username' : session['username'],
        'vozilo_id' : vozilo_id,
        'zacetek' : zacetek,
        'konec' : konec,
    })    

    return jsonify({'success': True, 'error': 'Rezervacija uspešna!'})

#prikaz profila in kaj si rezerviral
@app.route("/moj_profil")
def moj_profil():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    uporabnik_rezervacije = rezervacije.search(Query().username == session['username'])
    vozila_dict = {v["id"]: v["ime"] for v in vozila.all()}

    for r in uporabnik_rezervacije:
        r["vozilo"] = vozila_dict.get(r["vozilo_id"], "neznano vozilo")
        r["id"] = r.doc_id
    return render_template("moj_profil.html", rezervacije = uporabnik_rezervacije)

@app.route("/api/preklici-rezervacijo", methods=["POST"])
def preklic_rezervacije():
    data = request.json
    id_str = str(data.get("id", ""))

    if not id_str.isdigit():
        return jsonify({"success": False, "error": "Neveljaven ID"}), 400

    id = int(id_str)
    rezervacija = rezervacije.get(doc_id=id)

    if rezervacija:
        rezervacije.remove(doc_ids=[id])
        return jsonify({"success": True, "message": "Rezervacija je bila uspešno preklicana."})
    else:
        return jsonify({"success": False, "error": "Rezervacija ne obstaja"}), 404


#prijava
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

#registracija
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

#odjava
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


#premium
@app.route("/premium")
def premium():
    if 'username' not in session:
        return redirect(url_for("login"))

    user = users.get(User.username == session["username"])
    is_premium = user.get("premium", False)
    return render_template("premium.html", is_premium=is_premium)

@app.route("/placaj_premium", methods=["GET", "POST"])
def placaj_premium():
    if 'username' not in session:
        return redirect(url_for("login"))
    
    if request.method == "post":
        kartica = request.form.get("kartica")
        mesec_poteka = request.form.get("mesec_poteka")
        leto_poteka = request.form.get("leto_poteka")
        cvv = request.form.get("cvv")
        samodejno = request.form.get("samodejno") == "on"

        users.update({"premium": True}, User.username == session["username"])

        return redirect(url_for("premium"))

    return render_template("placaj_premium.html")

@app.route("/o-nas")
def o_nas():
    return render_template("o_nas.html")


if __name__=="__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(debug=True)