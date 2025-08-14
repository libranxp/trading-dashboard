from flask import Flask, render_template, jsonify
from scanner.scan_logic import run_scan
from alerts.telegram import send_alert

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    results = run_scan()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
