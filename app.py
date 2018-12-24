#!/usr/bin/env python3
from flask import Flask, url_for, request
import krampus18
app = Flask(__name__)

@app.route("/")
def main():
    return krampus18.main()

@app.route("/lab")
def lab():
    return krampus18.lab()

@app.route("/arena")
def arena():
    return krampus18.arena()

if __name__ == "__main__":
    app.run()
