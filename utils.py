import pdfkit

def generate_pdf_response(matches):
    html_content = "<html><body><h1>Llaves del Torneo</h1><ul>"
    for match in matches:
        peleador1 = match['peleador1']
        peleador2 = match['peleador2']
        html_content += f"<li>{peleador1['nombre']} {peleador1['apellido']} vs {peleador2['nombre']} {peleador2['apellido']}</li>"
    html_content += "</ul></body></html>"

    pdf = pdfkit.from_string(html_content, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=llaves_torneo.pdf'

    return response
