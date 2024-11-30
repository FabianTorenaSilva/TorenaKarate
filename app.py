from flask import Flask, request, render_template_string, redirect, url_for
import os
from dotenv import load_dotenv
from llaves import LlaveManager
from utils import generate_pdf_response

# Cargar configuraciones desde archivo .env
load_dotenv()

app = Flask(__name__)
llave_manager = LlaveManager()

# Plantilla HTML para la entrada de datos
form_template = """
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <title>Registro de Torneo de Karate</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f8f9fa;
        padding: 20px;
      }
      .container {
        max-width: 600px;
        margin: 0 auto;
        background: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
      }
      h1 {
        text-align: center;
        margin-bottom: 20px;
      }
      .btn {
        width: 100%;
        margin-top: 10px;
      }
      .peleas-container {
        margin-top: 30px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Registro de Torneo de Karate</h1>
      <form method="post">
        <div class="form-group">
          <label for="nombre">Nombre:</label>
          <input type="text" name="nombre" class="form-control" id="nombre" required>
        </div>
        <div class="form-group">
          <label for="apellido">Apellido:</label>
          <input type="text" name="apellido" class="form-control" id="apellido" required>
        </div>
        <div class="form-group">
          <label for="grado">Grado:</label>
          <input type="text" name="grado" class="form-control" id="grado" required>
        </div>
        <input type="submit" value="Agregar Peleador" class="btn btn-primary">
      </form>
      <form method="post" action="/sortear">
        <input type="submit" value="Sortear Peleas" class="btn btn-success mt-3">
      </form>
      <h2 class="mt-4">Peleadores Registrados</h2>
      <ul class="list-group">
        {% for peleador in peleadores %}
          <li class="list-group-item">{{ peleador['nombre'] }} {{ peleador['apellido'] }} - Grado: {{ peleador['grado'] }}</li>
        {% endfor %}
      </ul>
    </div>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Agregar peleador
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        grado = request.form.get('grado')
        llave_manager.peleas.append({'nombre': nombre, 'apellido': apellido, 'grado': grado})
    return render_template_string(form_template, peleadores=llave_manager.peleas)

@app.route('/sortear', methods=['POST'])
def sortear():
    llave_manager.generar_llaves(llave_manager.peleas)
    return llave_manager.render_matches_html()

@app.route('/reset', methods=['GET'])
def reset():
    llave_manager.peleas = []
    return redirect('/')

@app.route('/descargar_pdf', methods=['POST'])
def descargar_pdf():
    return generate_pdf_response(llave_manager.peleas)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
