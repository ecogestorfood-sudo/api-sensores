from flask import Flask, request
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    dbname=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.environ['PGPASSWORD'],
    host=os.environ['PGHOST'],
    port=os.environ.get('PGPORT', 5432),
    sslmode='require'
)

@app.route('/')
def home():
    return 'API Flask lista ✅'

@app.route('/sensor', methods=['POST'])
def recibir_dato():
    data = request.get_json()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sensores (sensor_id, valor, unidad) VALUES (%s, %s, %s)",
        (data['sensor_id'], data['valor'], data['unidad'])
    )
    conn.commit()
    cur.close()
    return {'status': 'ok'}
