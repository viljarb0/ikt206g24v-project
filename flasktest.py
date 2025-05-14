#!/usr/bin/env python

from flask import Flask, request, session

app = Flask(__name__)

@app.route('/1', methods = ["GET", "POST"])
def first():
    return str(request.environ)

@app.route('/2', methods = ["GET", "POST"])
def second():
    return str(session)

app.run(debug=True)
