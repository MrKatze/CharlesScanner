import sys
import os
from PyQt5.QtWidgets import QApplication

# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ventanas.ventanaBusquedaInteligente import VentanaBusquedaInteligente

def test_ventana_busqueda_inteligente():
    """Prueba la funcionalidad de la ventana de búsqueda inteligente."""
    app = QApplication(sys.argv)

    # Ruta de prueba para un archivo DOCX o PDF
    ruta_archivo = os.path.join(os.getcwd(), "documentos", "Crónicas Del Cataclismo Galapago.pdf")  # Cambia esto por la ruta de tu archivo de prueba
    # ruta_archivo = os.path.join(os.getcwd(), "tests", "documentos\prueba6.pdf")  # Cambia esto por la ruta de tu archivo de prueba

    # Verificar que el archivo de prueba exista
    if not os.path.exists(ruta_archivo):
        print(f"Error: El archivo de prueba no existe en la ruta {ruta_archivo}")
        return

    # Crear la ventana de búsqueda inteligente
    ventana = VentanaBusquedaInteligente(ruta_archivo)
    ventana.show()

    # Simular la búsqueda personalizada
    ventana.barra_busqueda.setText("Albert")
    ventana.buscar_texto_personalizado()

    # Verificar que la categoría "Personalizado" se haya agregado
    categorias = [ventana.lista_categorias.item(i).text() for i in range(ventana.lista_categorias.count())]
    assert any("Personalizado" in categoria for categoria in categorias), "La categoría 'Personalizado' no se agregó correctamente."

    # Cerrar la ventana
    ventana.close()
    print("Prueba completada exitosamente.")

if __name__ == "__main__":
    test_ventana_busqueda_inteligente()