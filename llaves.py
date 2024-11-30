import random
from utils import generate_pdf_response

class LlaveManager:
    def __init__(self):
        self.peleas = []

    def generar_llaves(self, peleadores):
        self.peleas = []  # Reiniciar peleas cada vez que se genera una nueva llave
        llave = max(8, len(peleadores))
        if len(peleadores) > 8:
            llave = 16

        # Completar peleadores faltantes con "bye"
        while len(peleadores) < llave:
            peleadores.append({'nombre': 'BYE', 'apellido': '', 'grado': ''})

        # Mezclar peleadores y crear llaves de peleas
        random.shuffle(peleadores)
        for i in range(0, llave, 2):
            if peleadores[i]['nombre'] == 'BYE' and peleadores[i + 1]['nombre'] == 'BYE':
                continue  # No emparejar dos BYE juntos
            self.peleas.append({
                'peleador1': peleadores[i],
                'peleador2': peleadores[i + 1],
                'ganador': None
            })

    def render_matches_html(self):
        peleas_html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Torneo de Peleas</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                body {
                    font-family: 'Roboto', sans-serif;
                    background-color: #1a1a1a;
                    color: #f0f0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    min-height: 100vh;
                    margin: 0;
                }
                h1 {
                    font-size: 3rem;
                    color: #ff0000;
                    text-transform: uppercase;
                    margin-bottom: 2rem;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
                }
                .bracket {
                    display: flex;
                    gap: 3rem;
                    flex-wrap: wrap;
                }
                .round {
                    display: flex;
                    flex-direction: column;
                    gap: 2rem;
                    border: 2px solid #ff0000;
                    border-radius: 15px;
                    padding: 20px;
                    background-color: #333;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
                }
                .match {
                    background-color: #444;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                    transition: transform 0.3s ease;
                    color: #ffffff;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
                }
                .match:hover {
                    transform: scale(1.05);
                }
                .round-title {
                    font-weight: bold;
                    font-size: 1.5rem;
                    color: #ff0000;
                    text-align: center;
                    margin-bottom: 1rem;
                    text-transform: uppercase;
                    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
                }
            </style>
        </head>
        <body>
            <h1>Torneo de Peleas</h1>
            <div class="bracket">
        """

        # Dividir las peleas en rondas y renderizar cada ronda como en el ejemplo
        ronda1 = self.peleas[:4]
        ronda2 = [] if len(self.peleas) <= 4 else self.peleas[4:6]
        ronda3 = [] if len(self.peleas) <= 6 else self.peleas[6:]

        # Ronda 1 - Mostrar todas las peleas originales
        peleas_html += "<div class='round'><div class='round-title'>Ronda 1 - 8 Peleadores</div>"
        for pelea in ronda1:
            peleas_html += f"<div class='match'>{pelea['peleador1']['nombre']} {pelea['peleador1']['apellido']} vs {pelea['peleador2']['nombre']} {pelea['peleador2']['apellido']}</div>"
        peleas_html += "</div>"

        # Ronda 2 - Mantener la estructura, incluso si no hay datos disponibles
        peleas_html += "<div class='round'><div class='round-title'>Ronda 2 - 4 Peleadores</div>"
        if ronda2:
            for pelea in ronda2:
                peleas_html += f"<div class='match'>Ganador {pelea['peleador1']['nombre']} vs Ganador {pelea['peleador2']['nombre']}</div>"
        else:
            for _ in range(2):  # Mostrar espacios vacíos para completar la ronda
                peleas_html += "<div class='match'>Pendiente</div>"
        peleas_html += "</div>"

        # Ronda 3 - Final y 3er Puesto
        peleas_html += "<div class='round'><div class='round-title'>Ronda 3 - Final y 3er Puesto</div>"
        if ronda3:
            peleas_html += "<div class='match'>Ganador Semifinal 1 vs Ganador Semifinal 2 (Final)</div>"
            peleas_html += "<div class='match'>Perdedor Semifinal 1 vs Perdedor Semifinal 2 (3er Puesto)</div>"
        else:
            peleas_html += "<div class='match'>Pendiente (Final)</div>"
            peleas_html += "<div class='match'>Pendiente (3er Puesto)</div>"
        peleas_html += "</div>"

        peleas_html += """
            </div>
            <form method="post" action="/descargar_pdf">
                <input type="submit" value="Descargar en PDF" class="btn btn-danger mt-3">
            </form>
            <a href='/reset' class='btn btn-secondary mt-3'>Volver al inicio</a>
        </body>
        </html>
        """
        return peleas_html

    def generate_pdf_response(self):
        return generate_pdf_response(self.peleas)
