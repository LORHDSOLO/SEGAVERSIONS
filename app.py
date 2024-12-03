from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)

# Función para obtener la conexión a la base de datos MySQL
def get_db_connection():
    return pymysql.connect(
        host='localhost',           # Dirección del servidor MySQL
        user='tu_usuario',          # Usuario de la base de datos
        password='tu_contraseña',   # Contraseña del usuario
        database='mi_base_de_datos', # Nombre de tu base de datos
        cursorclass=pymysql.cursors.DictCursor  # Retorna resultados como diccionarios
    )

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para mostrar el formulario de registro de audiencias
@app.route('/registrar', methods=['GET', 'POST'])
def registrar_audiencia():
    if request.method == 'POST':
        # Recibir datos del formulario
        numero_carpeta = request.form['numero_carpeta']
        fecha = request.form['fecha']
        numero_sala = request.form['numero_sala']
        modalidad = request.form['modalidad']
        hora_inicio = request.form['hora_inicio']
        numero_consolidacion = request.form['numero_consolidacion']
        participantes = request.form.getlist('participante')  # Lista de participantes

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Insertar audiencia
                cursor.execute("""
                    INSERT INTO audiencias (numero_carpeta, fecha, numero_sala, modalidad, hora_inicio, numero_consolidacion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (numero_carpeta, fecha, numero_sala, modalidad, hora_inicio, numero_consolidacion))
                audiencia_id = cursor.lastrowid

                # Insertar participantes
                for participante in participantes:
                    cursor.execute("""
                        INSERT INTO participantes (nombre, audiencia_id)
                        VALUES (%s, %s)
                    """, (participante, audiencia_id))

            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', mensaje="Ocurrió un error al registrar la audiencia.")
        finally:
            conn.close()

        return render_template('exito.html', mensaje="Audiencia registrada correctamente.")
    
    return render_template('registrar.html')

# Ruta para mostrar el formulario de solicitudes
@app.route('/solicitar', methods=['GET', 'POST'])
def solicitar_copia():
    if request.method == 'POST':
        # Recibir datos del formulario
        participante_id = request.form['participante_id']
        audiencia_id = request.form['audiencia_id']
        fecha_solicitud = datetime.now().strftime('%Y-%m-%d')

        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Guardar solicitud en la base de datos
                cursor.execute("""
                    INSERT INTO solicitudes (participante_id, audiencia_id, fecha_solicitud)
                    VALUES (%s, %s, %s)
                """, (participante_id, audiencia_id, fecha_solicitud))
            conn.commit()
        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', mensaje="Ocurrió un error al realizar la solicitud.")
        finally:
            conn.close()

        return render_template('exito.html', mensaje="Copia solicitada correctamente.")

    return render_template('solicitar.html')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
