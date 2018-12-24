#!/usr/bin/env python3
from flask import Flask, url_for, request, session, redirect
from login import do_login
import krampus18
app = Flask(__name__)
app.secret_key = b'ZG\xf2-s\x80\xb9\xcc\xbe;\xc1d\xa9\xab|\x80'
@app.route("/")
def main():
    return krampus18.main()

@app.route("/lab")
def lab():
    return krampus18.lab()

@app.route("/arena")
def arena():
    return krampus18.arena()

@app.route('/login', methods = ["POST"])
def login():
    return do_login()

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
