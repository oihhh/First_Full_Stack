from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import init_db
import sqlite3

app = Flask(__name__)
CORS(app)
init_db()

def get_db():
    conn = sqlite3.connect('clicker.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/leaderboard')
def leaderboard():
    conn = get_db()
    visitors = conn.execute(
        'SELECT nickname, hearts, cookies FROM visitors ORDER BY hearts + cookies DESC'
    ).fetchall()
    conn.close()
    return jsonify([dict(v) for v in visitors])

@app.route('/join', methods=['POST'])
def join():
    nickname = request.json['nickname']
    conn = get_db()
    try:
        conn.execute('INSERT INTO visitors (nickname) VALUES (?)', (nickname,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Welcome {nickname}!"})
    except:
        conn.close()
        return jsonify({"message": "Nickname already taken!"})

@app.route('/click', methods=['POST'])
def click():
    nickname = request.json['nickname']
    type = request.json['type']
    conn = get_db()
    conn.execute(f'UPDATE visitors SET {type} = {type} + 1 WHERE nickname = ?', (nickname,))
    conn.commit()
    conn.close()
    return jsonify({"message": "clicked!"})
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)