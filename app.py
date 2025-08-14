from flask import Flask, render_template, request, redirect, url_for
from models import scan_market
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    results = scan_market()
    return render_template('index.html', results=results)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/add-trade')
def add_trade():
    return render_template('add_trade.html')

if __name__ == '__main__':
    app.run(debug=True)
