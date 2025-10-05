from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Conexión a Neon usando el string completo
def get_db_connection():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    return conn

@app.route('/')
def home():
    return "✅ API de sensores funcionando correctamente"

@app.route('/sensores')
def sensores():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM sensores ORDER BY timestamp DESC LIMIT 10;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
