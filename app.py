import cs50
import os
import datetime
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, g, session, url_for
import sqlite3
import binascii, hashlib, base58
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

          print(logged_id)

          sites = db.execute("SELECT site FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

          print(sites)



          return render_template("main.html",sites=sites,logged_id=logged_id)
        
    else:

        return render_template("index.html")




@app.route("/generate.html")
def generate():

    return render_template("generate.html")



@app.route("/success.html")
def success():

    fullkey = "80"+ binascii.hexlify(os.urandom(32)).decode()
    keygen = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()

    db.execute("INSERT INTO users (pass) VALUES (:keygen)",keygen=keygen)

    return render_template("success.html",keygen=keygen)



  

@app.route('/addsite.html/<int:logged_id>/', methods=['GET', 'POST'])
def addsite(logged_id):
      
  sitio = request.form.get("sitename")

  print (sitio)

  color = request.form.get("sitecolor")
        
  print (color)

  print (logged_id)

  db.execute("INSERT INTO sites (id,usuario,site,color) VALUES (:logged_id,:logged_id,:sitio,:color)", logged_id=logged_id, sitio=sitio, color=color)

  print("done it!")

  sites = db.execute("SELECT site FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

  print(sites)

  return redirect (url_for('main',logged_id=logged_id))




@app.route("/main.html")
def main():

  print("-------main------")

  logged_id = request.args['logged_id']

  print(logged_id)

  sites = db.execute("SELECT * FROM sites WHERE  usuario = :logged_id",logged_id=logged_id)

  print(sites)

  return render_template("main.html",sites=sites,logged_id=logged_id)









    









if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)

