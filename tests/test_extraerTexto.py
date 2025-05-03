import os
import pytest
import numpy as np
from unittest import mock
from app.Extraer_texto import extraccion

# Crea una imagen simulada para pasarla como entrada
def create_fake_image():
    return np.zeros((100, 100, 3), dtype=np.uint8)

@mock.patch("app.Extraer_texto.easyocr.Reader")
def test_extraccion_texto(mock_reader_class):
    fake_texto = ["Hola", "mundo"]
    
    # Configura el mock del lector para que devuelva texto simulado
    mock_reader = mock.Mock()
    mock_reader.readtext.return_value = fake_texto
    mock_reader_class.return_value = mock_reader

    imagen = create_fake_image()
    name = "prueba"

    texto, ruta = extraccion(imagen, name)

    assert texto == fake_texto
    assert ruta.endswith(f"documentos/{name}.docx")
    assert "documentos" in ruta
