#!/usr/bin/env python3

from flask import Flask, render_template
import os
import sys

app = Flask(__name__)
flag = open(f"{os.path.abspath(os.path.dirname(__file__))}/.passwd", "r").read()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", flag=flag)

if __name__ == "__main__":
    app.run("0.0.0.0", port=sys.argv[1])