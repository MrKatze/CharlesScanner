import os
import tempfile
import pytest
from app.Extraer_texto import conversionformato  # Ajusta el path según tu estructura

def test_conversionformato_docx_creado():
    texto = ["Línea 1", "Línea 2", "Línea 3"]
    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_docx = os.path.join(tmpdir, "archivo_prueba.docx")
        conversionformato(texto, "archivo_prueba.docx", ruta_docx, indicador=1)

        # Verifica que el archivo .docx fue creado
        assert os.path.exists(ruta_docx), "El archivo .docx no fue creado"
        assert os.path.getsize(ruta_docx) > 0, "El archivo .docx está vacío"
