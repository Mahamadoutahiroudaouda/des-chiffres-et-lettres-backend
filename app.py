from flask import Flask, request, jsonify, send_from_directory
import json
import os
import datetime

app = Flask(__name__)

# Mot de passe admin
PASSWORD = 'admin123'  # ← CHANGE-LE ! (ex: 'MonSuperMotDePasse2024')

DATA_FILE = 'data.json'

# Créer data.json si absent
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    player_name = data.get('playerName', '').strip()
    chiffres = data.get('chiffres', [])
    lettres = data.get('lettres', [])

    if not player_name:
        return jsonify({'error': 'Nom requis'}), 400

    # Charger anciennes soumissions
    with open(DATA_FILE, 'r') as f:
        submissions = json.load(f)

    # Nouvelle soumission
    submission = {
        'id': len(submissions) + 1,
        'playerName': player_name,
        'chiffres': chiffres,
        'lettres': lettres,
        'timestamp': datetime.datetime.now().isoformat(),
        'code': 'DC' + str(1000 + len(submissions))
    }
    submissions.append(submission)

    # Sauvegarder
    with open(DATA_FILE, 'w') as f:
        json.dump(submissions, f, indent=2)

    return jsonify({'success': True, 'code': submission['code']})

@app.route('/results')
def results():
    pwd = request.args.get('pwd')
    if pwd != PASSWORD:
        return jsonify({'error': 'Accès refusé'}), 403

    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    return jsonify(data)

@app.route('/admin')
def admin():
    return send_from_directory('.', 'admin.html')

@app.route('/')
def home():
    return '<h1>Serveur actif 🚀</h1><p>Accès admin : <a href="/admin?pwd=' + PASSWORD + '">/admin?pwd=' + PASSWORD + '</a></p>'

# Pour servir admin.html et style.css
@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(port=5000)