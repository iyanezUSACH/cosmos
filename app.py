# app.py
from flask import Flask, send_file
import threading
import time
from generate_georss import generate_georss

app = Flask(__name__)

@app.route('/')
def index():
    return "Servidor GeoRSS funcionando. Accede a /georss para ver el feed."

@app.route('/georss')
def serve_georss():
    return send_file("latest_truck_data.xml")

# Hilo para actualizar el archivo cada 30 segundos
def periodic_update():
    while True:
        try:
            generate_georss()
        except Exception as e:
            print(f"Error actualizando GeoRSS: {e}")
        time.sleep(30)

# Lanzar hilo en segundo plano
if __name__ == '__main__':
    threading.Thread(target=periodic_update, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
