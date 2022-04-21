#!/usr/bin/env python3

from time import time
from flask import Flask, jsonify, redirect, render_template, request, make_response, url_for
import os
import sys
from hashlib import md5
from base64 import b64encode

def transform(timestamp:str, salt:str=""):
    to_encode = salt + timestamp
    hashed = bytes.fromhex(md5(to_encode.encode()).hexdigest())
    return b64encode(hashed).decode().replace("=", "").replace("+", "").replace("/", "")

def check_session(timestamp:str):
    if time() - float(timestamp) > 60:
        return False
    return True

question1 = "Nb]J@jvN6h"
question2 = "i0RFus}m&6"
question3 = "q<\K<'?boz"
question4 = "f]qxeB.|Y."
question5 = "~V{mnyDwgy"


app = Flask(__name__)
app.jinja_env.filters["transform"] = transform
flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("go") is not None:
            session = str(time())
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("sess", session)
            return resp
        else:
            return "Error"
    else:
        if request.cookies.get("sess") is None:
            return render_template("create.html")
        else:
            return render_template("index.html", page=url_for('challenge'), session=request.cookies.get("sess"))

@app.route("/challenge/", methods=["GET", "POST"])
def challenge():
    session = request.cookies.get("sess")
    if session is None:
        return redirect(url_for('index'))
    elif not check_session(session):
        return redirect(url_for("session_killed"))
    else:
        return render_template("challenge.html", q1=transform(session, question1), q2=transform(session, question2), q3=transform(session, question3), q4=transform(session, question4), q5=transform(session, question5), sess=session)

@app.route("/answer/", methods=["POST"])
def answer():
    session = request.cookies.get("sess")
    rep1 = request.form.get("question1")
    rep2 = request.form.get("question2")
    rep3 = request.form.get("question3")
    rep4 = request.form.get("question4")
    rep5 = request.form.get("question5")

    if session is None:
        return redirect(url_for("/"))
    elif not check_session(session):
        return redirect(url_for('session_killed'))
    
    if not (None in [rep1, rep2, rep3, rep4, rep5]):
        if rep1 == transform(session, question1) and rep2 == transform(session, question2) and rep3 == transform(session, question3) and rep4 == transform(session, question4) and rep5 == transform(session, question5):
            message = f"Bravo vous êtes un super scrapper ! Voici votre flag: {flag}"
        else:
            message = "Il y a au moins une mauvaise réponse désolé !"
    else:
        message = "Vous devez répondre à toutes les questions avant de valider"
    
    return jsonify(dict(message=message))
        

@app.route("/session_killed/", methods=["GET", "POST"])
def session_killed():
    resp = make_response(render_template("session_killed.html"))
    resp.set_cookie('sess', '', expires=0)
    return resp

if __name__ == "__main__":
    app.run("0.0.0.0", port=sys.argv[1])
