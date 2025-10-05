from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# 🔐 Conexión a la base de datos con variables separadas
conn = psycopg2.connect(
    host=os.environ['PGHOST'],
    database=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.environ['PGPASSWORD'],
    port=os.environ['PGPORT']
)

# ✅ Ruta de prueba para saber si funciona
@app.route('/')
def home():
    return '<p>✅ API de sensores funcionando correctamente</p>'

# 📥 Ruta para recibir datos del ESP32
@app.route('/sensores', methods=['POST'])
def recibir_datos():
    data = request.get_json()

    sensor_id = data.get('sensor_id')
    valor = data.get('valor')
    unidad = data.get('unidad')

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sensores (sensor_id, valor, unidad) VALUES (%s, %s, %s)",
        (sensor_id, valor, unidad)
    )
    conn.commit()
    cur.close()

    return jsonify({"mensaje": "Datos guardados correctamente"}), 201

# 📤 Ruta para ver los datos almacenados
@app.route('/sensores', methods=['GET'])
def ver_datos():
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensores ORDER BY timestamp DESC LIMIT 20")
    rows = cur.fetchall()
    cur.close()

    datos = []
    for row in rows:
        datos.append({
            "id": row[0],
            "sensor_id": row[1],
            "valor": row[2],
            "unidad": row[3],
            "timestamp": row[4].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(datos)
