from flask import Flask, jsonify, render_template, session, url_for, redirect, request
import flask
from api import DB
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16).hex()
db = DB()
app.jinja_env.filters["points"] = db.get_challenges_points
app.jinja_env.filters["get_points"] = db.get_points
current_path = os.path.abspath(os.path.dirname(__file__))

def check_login():
    if "username" in session:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if check_login():
        return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register():
    if check_login():
        return redirect(url_for("index"))
    else:
        return render_template("registration.html")


@app.route("/leaderboard/", methods=["GET", "POST"])
def leaderboard():
    return render_template("leaderboard.html")


@app.route("/challenges/", methods=["GET", "POST"])
def challenges():
    if check_login():
        return render_template("challenges.html", challenges=db.get_challenges(session["username"]))
    else:
        return redirect(url_for("login"))

@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/login", methods=["POST"])
def api_login():
    if "username" in request.form and "password" in request.form:
        username = request.form.get("username")
        password = request.form.get("password")

        if db.check_login(username, password):
            session["username"] = username
            session["points"] = db.get_points(username)
            logged_in = True
        else:
            logged_in = False
    else:
        logged_in = False
    return jsonify(
        dict(
            logged_in=logged_in
        )
    )

@app.route("/api/register", methods=["POST"])
def api_register():
    if "username" in request.form and "password" in request.form and "first_name" in request.form and "last_name" in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if not all([username, password, first_name, last_name]):
            registered = False
            message = "Tous les champs doivent être renseignés"
        elif not db.check_username(username):
            registered = False
            message = "Ce pseudo est déjà pris"
        else:
            db.register(first_name, last_name, username, password)
            session["username"] = username
            session["points"] = 0
            registered = True
            message = ""
    else:
        registered = False
        message = "Tous les champs doivent être renseignés"

    return jsonify(registered=registered, message=message)

@app.route("/api/flag", methods=["POST"])
def api_flag():
    if "flag" in request.form and "chall_id" in request.form:
        flag = request.form.get("flag")
        chall_id = request.form.get("chall_id")

        if db.check_flag(flag, chall_id):
            if not db.check_solve(session["username"], chall_id):
                validated = True
                message = "Bien joué !"
                color = "green"
                earned_points = db.get_challenges_points(chall_id)
                db.add_solve(session["username"], chall_id, earned_points)
            else:
                validated = False
                message = "Bien joué mais tu as déjà valider ce challenge"
                color = "orange"
                earned_points = 0
        else:
            validated = False
            message = "Flag incorrect..."
            color = "red"
            earned_points = 0
    else:
        validated = False
        message = "Flag non renseigné..."
        color = "red"
        earned_points = 0

    return jsonify(dict(validated=validated, message=message, color=color, earned_points=earned_points))

@app.route("/api/leaderboard", methods=["POST"])
def api_leaderboard():
    scoreboard = db.get_leaderboard()
    return jsonify(scoreboard)


######################################### Challenges #########################################

@app.route("/infos/", methods=["GET", "POST"])
def infos():
    return "Toutes les infos sont dans l'énoncé"

@app.route("/algo-c/", methods=["GET", "POST"])
def algo_c():
    return flask.send_file(f"{current_path}/files/algo_c.txt")

@app.route("/algo-js/", methods=["GET", "POST"])
def algo_js():
    return flask.send_file(f"{current_path}/files/algo_js.txt")

@app.route("/special-lines/", methods=["GET", "POST"])
def special_lines():
    return flask.send_file(f"{current_path}/files/des_lignes_speciales.txt")

@app.route("/some-lines/", methods=["GET", "POST"])
def some_lines():
    return flask.send_file(f"{current_path}/files/quelques_lignes.txt")

@app.route("/no-help/", methods=["GET", "POST"])
def no_help():
    return "Pas d'aide pour ce challenge, je pense que vous pouvez chercher seul ;)"

if __name__ == "__main__":
    app.run("0.0.0.0", port=9013)