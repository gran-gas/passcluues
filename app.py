import cs50
import os
import datetime
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, g, session, url_for
import sqlite3
import secrets
from cs50 import SQL


db = SQL("postgres://ldbrsofbafwwau:6d2b7da61029e4e41a603abacd1222cb04b5a9582522c35d59295d325eba85f6@ec2-23-21-115-109.compute-1.amazonaws.com:5432/dfpd4foear0e3q")

# Configure application
app = Flask(__name__)

logged_id = 0

app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.config.from_object(__name__)
app.secret_key = "super secret key"

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Default Route
@app.route("/")
def default():
    return render_template("index.html")

# Click on logo
@app.route('/index.html', methods=["GET", "POST"])
def index():

    if request.method == "POST":

        userkey = request.form.get("userkey")

        print(userkey)

        key = db.execute("SELECT * FROM users WHERE pass = :userkey",userkey=userkey)

        print(key)

        if not key:

          return render_template("error.html")
        
        else: 

          logged_id = key[0]["id"]

          session['logged'] = logged_id

          print(logged_id)

          sites = db.execute("SELECT * FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

          print(sites)



          return render_template("main.html",sites=sites,logged_id=logged_id)
        
    else:

        return render_template("index.html")




@app.route("/generate.html")
def generate():

    return render_template("generate.html")



@app.route("/success.html")
def success():

    keygen = secrets.token_hex(8)

    db.execute("INSERT INTO users (pass) VALUES (:keygen)",keygen=keygen)

    return render_template("success.html",keygen=keygen)



  

@app.route('/addsite.html', methods=['GET', 'POST'])
def addsite():

  logged_id = session['logged']
      
  sitio = request.form.get("sitename")

  print (sitio)

  color = request.form.get("sitecolor")
        
  print (color)

  print (logged_id)

  url = request.form.get("url")

  db.execute("INSERT INTO sites (usuario,site,color,url) VALUES (:logged_id,:sitio,:color,:url)", logged_id=logged_id, sitio=sitio, color=color, url=url)

  db.execute("INSERT INTO descriptions (user_id, usuario, sitio) VALUES (:logged_id, :logged_id, :sitio)", logged_id=logged_id, sitio=sitio)

  print("done it!")

  sites = db.execute("SELECT site FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

  print(sites)

  

  return redirect (url_for('main'))




@app.route("/main.html")
def main():

  print("-------main------")

  logged_id = session['logged']

  print(logged_id)

  sites = db.execute("SELECT * FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

  print(sites)

  return render_template("main.html",sites=sites,logged_id=logged_id)



@app.route("/delete.html", methods=['GET', 'POST'])
def delete():

  print("-------delete------")

  logged_id = session['logged']

  print(logged_id)

  deleted = request.form.get("deleteRadio")

  db.execute("DELETE FROM sites WHERE  (usuario,site) = (:logged_id, :deleted)",logged_id=logged_id, deleted=deleted)

  sites = db.execute("SELECT * FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

  print(sites)

  return render_template("main.html",sites=sites,logged_id=logged_id)


@app.route("/logout.html")
def logout():

  session.clear()

  logged_id = 0

  return render_template("index.html")



@app.route('/results.html', methods=['GET', 'POST'])
def results():

  print("-------results------")

  logged_id = session['logged']


  sitio = request.form.get("selected")

  print(sitio)

  session['sitio'] = sitio

  keywords = db.execute("SELECT keyword FROM words WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  description = db.execute("SELECT description FROM descriptions WHERE (usuario,sitio) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  url = db.execute("SELECT url FROM sites WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  print(description)

  return render_template("results.html", keywords=keywords, sitio=sitio, description=description, url=url)


@app.route('/newkey.html', methods=['GET', 'POST'])
def newkey():

  print("------new key -------")

  logged_id = session['logged']

  sitio = session['sitio']

  print (sitio)

  newKey = request.form.get("newKey")

  print(newKey)

  

  db.execute("INSERT INTO words (site,keyword,usuario) VALUES (:sitio,:newKey,:logged_id)", logged_id=logged_id, sitio=sitio, newKey=newKey)

  

  keywords = db.execute("SELECT keyword FROM words WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  description = db.execute("SELECT description FROM descriptions WHERE (usuario,sitio) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  url = db.execute("SELECT url FROM sites WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  print(description)

  return render_template("results.html", keywords=keywords, sitio=sitio, description=description, url=url)



@app.route('/newdesc.html', methods=['GET', 'POST'])
def newdesc():

  logged_id = session['logged']

  sitio = session['sitio']

  newDesc = request.form.get("newDesc")

  db.execute("UPDATE descriptions SET description = :newDesc WHERE (usuario,sitio) = (:logged_id, :sitio)", newDesc=newDesc, logged_id=logged_id, sitio=sitio)

  keywords = db.execute("SELECT keyword FROM words WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  description = db.execute("SELECT description FROM descriptions WHERE (usuario,sitio) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  url = db.execute("SELECT url FROM sites WHERE (usuario,site) = (:logged_id,:sitio)", logged_id=logged_id, sitio=sitio)

  print(description)

  return render_template("results.html", keywords=keywords, sitio=sitio, description=description, url=url)



@app.route('/tutorial.html')
def tutorial():

  return render_template("tutorial.html")





















    









if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

