#!/usr/bin/env python3
from flask import Flask, url_for, request, session, redirect, Response
from login import do_login
import krampus18
import time
import database
import config
app = Flask(__name__)
app.secret_key = config.SESSIONKEY
@app.route("/")
def main():
    return krampus18.main()

@app.route("/lab")
def lab():
    return krampus18.lab()

@app.route("/arena")
def arena():
    return krampus18.arena(request.args.get("player", None))

@app.route("/arena/start")
def arena_start():
    if "username" in session:
        username = session["username"]
        database.restart_arena(username, 1, 1)
    return redirect(url_for("arena"))

@app.route("/arena/dna", methods = ["POST"])
def arena_dna():
    return krampus18.arena_dna()

@app.route("/arena/pos", methods = ["POST"])
def arena_pos(): return krampus18.arena_pos()

@app.route("/arena/t", methods = ["POST"])
def arena_t(): return krampus18.arena_t()

@app.route("/arena/round", methods = ["POST"])
def arena_round(): return krampus18.arena_round()

@app.route('/login', methods = ["POST"])
def login():
    return do_login()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("main"))

@app.route("/save", methods = ["POST"])
def save():
    if "username" in session:
        username = session["username"]
        dna = request.form["dna"]
        if username and dna:
            database.access_db()
            database.save_pet(username, dna)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
