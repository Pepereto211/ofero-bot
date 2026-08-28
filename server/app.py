from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Ecosistema Lumen Activo</h1>"

@app.route('/api/status')
def status():
    return jsonify({"status": "running", "system": "Lumen Core"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
