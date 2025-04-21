import mammoth
from weasyprint import HTML

def convertir_docx_a_pdf(docx_path, pdf_path):
    # Convertir .docx a HTML con Mammoth
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        html_content = result.value  # Contenido HTML del archivo .docx

    # Convertir HTML a PDF con WeasyPrint
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"PDF generado con formato: {pdf_path}")

# Uso básico
