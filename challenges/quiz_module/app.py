#!/usr/bin/env python3

from flask import Flask, render_template, request
import os
import sys

app = Flask(__name__)
flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()
good_resp = "pip"
question = "Quel programme permet d'installer une nouvelle librairie python ?"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        resp = request.form.get("resp")
        if resp is not None and resp.lower() == good_resp:
            message = f"Bien joué voici ton flag: {flag}"
        else:
            message = "Mauvaise réponse :)"
    
    return render_template("index.html", message=message, question=question)

if __name__ == "__main__":
    app.run("0.0.0.0", port=sys.argv[1])