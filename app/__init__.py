import sqlite3
import random
from flask import Flask, render_template, session, request, redirect
import os
from utility import *

app = Flask(__name__)
app.secret_key = os.urandom(12)

initiate_data()

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/imposter', methods=["GET", "POST"])
def imposter():
    return render_template("imposter.html")

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0')
