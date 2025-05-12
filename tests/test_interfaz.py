# -*- coding: utf-8 -*-
# Test suite for the GUI components of the application
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ventanas.ventanaConfiguracion import VentanaConfiguracion
import pytest
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QListWidget, QSlider, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QSize
from ventanas.ventanaPrincipal import VentanaPrincipal
from ventanas.ventanaScaneo import VentanaEscaneo
from ventanas.ventanaOpcionesArchivo import VentanaOpcionesArchivos
import qtawesome as qta
import os
import json 
from ventanas.VentanaRuta import VentanaSeleccionarRuta
from ventanas.ventanaNotificacion import VentanaNotificacion

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def ventana_principal(qtbot):
    """Crea una instancia de VentanaPrincipal para pruebas."""
    ventana = VentanaPrincipal()
    qtbot.addWidget(ventana)
    return ventana

@pytest.fixture
def ventana_escaneo(qtbot):
    """Crea una instancia de VentanaEscaneo para pruebas."""
    ventana = VentanaEscaneo()
    qtbot.addWidget(ventana)
    return ventana

@pytest.fixture
def ventana_opciones(qtbot):
    """Crea una instancia de VentanaOpcionesArchivos para pruebas."""
    ventana = VentanaOpcionesArchivos("archivo_de_prueba.txt")
    qtbot.addWidget(ventana)
    return ventana

@pytest.fixture
def ventana_configuracion(qtbot):
    """Inicializa la ventana sin mostrarla para pruebas"""
    ventana = VentanaConfiguracion()
    qtbot.addWidget(ventana)  # Asegura que la ventana solo existe en memoria
    return ventana

@pytest.fixture
def ventana_ruta(qtbot):
    """Inicializa la ventana sin mostrarla para pruebas"""
    ventana = VentanaSeleccionarRuta()
    qtbot.addWidget(ventana)
    return ventana

@pytest.fixture
def ventana_notificacion(qtbot):
    """Inicializa la ventana sin mostrarla para pruebas."""
    ventana = VentanaNotificacion("archivo_prueba.txt", tiempo_cierre=1000)  # Tiempo más corto para la prueba
    qtbot.addWidget(ventana)
    return ventana


def test_ventana_principal_abre_correctamente(ventana_principal, qtbot):
    """Verifica que la ventana principal se abra correctamente."""
    ventana_principal.show()
    assert ventana_principal.isVisible()

def test_busqueda_archivos(ventana_principal, qtbot):
    """Prueba la funcionalidad de búsqueda de archivos."""
    campo_busqueda = ventana_principal.findChild(QLineEdit)
    boton_buscar = ventana_principal.findChild(QPushButton)

    qtbot.keyClicks(campo_busqueda, "documento")
    qtbot.mouseClick(boton_buscar, Qt.LeftButton)

    qtbot.wait(500)
    assert ventana_principal.lista_archivos.count() > 0

def test_seleccion_imagen(ventana_escaneo, qtbot, monkeypatch):
    """Simula la selección de una imagen válida en VentanaEscaneo."""
    imagen_prueba = "/home/karlx/GitHub/CharlesScanner/assets/test6.jpeg"

    if not os.path.exists(imagen_prueba):
        pytest.skip("No hay una imagen de prueba disponible.")

    def mock_getOpenFileName(*args, **kwargs):
        return (imagen_prueba, "")

    monkeypatch.setattr(QFileDialog, "getOpenFileName", mock_getOpenFileName)

    boton_seleccionar = ventana_escaneo.findChild(QPushButton)
    qtbot.mouseClick(boton_seleccionar, Qt.LeftButton)

    assert ventana_escaneo.boton_procesar.isEnabled()
    assert ventana_escaneo.slider_brillo.isEnabled()
    assert ventana_escaneo.slider_contraste.isEnabled()

def test_cambiar_brillo(ventana_escaneo, qtbot):
    """Prueba el ajuste del brillo en VentanaEscaneo."""
    slider_brillo = ventana_escaneo.findChild(QSlider)
    qtbot.mouseClick(slider_brillo, Qt.LeftButton, pos=slider_brillo.rect().center())
    qtbot.wait(200)

    assert ventana_escaneo.etiqueta_brillo.text().startswith("Brillo:")

def test_cambiar_contraste(ventana_escaneo, qtbot):
    """Prueba el ajuste del contraste en VentanaEscaneo."""
    slider_contraste = ventana_escaneo.findChild(QSlider)
    qtbot.mouseClick(slider_contraste, Qt.LeftButton, pos=slider_contraste.rect().center())
    qtbot.wait(200)

    assert ventana_escaneo.etiqueta_contraste.text().startswith("Contraste:")

def test_interaccion_menu_lateral(ventana_principal, qtbot):
    """Verifica que el menú lateral responde a los clics."""
    menu_lateral = ventana_principal.findChild(QWidget)
    
    botones_menu = menu_lateral.findChildren(QPushButton)
    assert botones_menu

    for boton in botones_menu:
        if boton.text() == "Configuración":
            qtbot.mouseClick(boton, Qt.LeftButton)
            break

    print("Menú lateral probado correctamente")

def test_ventana_opciones_archivos(ventana_opciones, qtbot):
    """Prueba la inicialización de VentanaOpcionesArchivos."""
    ventana_opciones.show()

    assert ventana_opciones.windowTitle() == "Opciones"
    assert ventana_opciones.nombre_archivo == "archivo_de_prueba.txt"
    assert ventana_opciones.layout().count() == 3  # Verifica que hay tres botones

    ventana_opciones.close()


def test_botones_interaccion(ventana_configuracion, qtbot):
    """Verifica la interacción con los botones sin abrir la ventana"""
    assert ventana_configuracion.btnCamara.text() == "Abrir Cámara"
    assert ventana_configuracion.btnRuta.text() == "Cambiar Ruta"

    # Simulación de clics en los botones
    qtbot.mouseClick(ventana_configuracion.btnCamara, Qt.LeftButton)
    qtbot.mouseClick(ventana_configuracion.btnRuta, Qt.LeftButton)

    # Verificar que la ventana sigue activa (usando visibility check mejorado)
    assert ventana_configuracion.isEnabled()

def test_cargar_ruta_predeterminada(ventana_ruta):
    """Verifica que la ruta predeterminada se carga cuando no existe el archivo de configuración"""
    if os.path.exists(ventana_ruta.CONFIG_FILE):
        os.remove(ventana_ruta.CONFIG_FILE)  # Elimina archivo para probar ruta predeterminada
    assert ventana_ruta.cargar_ruta() == ventana_ruta.ruta_default

def test_guardar_ruta(ventana_ruta):
    """Verifica que la ruta se guarda correctamente en el archivo JSON"""
    ruta_prueba = "/home/user/prueba_guardado"
    ventana_ruta.ruta_actual = ruta_prueba
    ventana_ruta.guardar_ruta()

    with open(ventana_ruta.CONFIG_FILE, "r") as file:
        config = json.load(file)
    
    assert config["ruta_guardado"] == ruta_prueba

def test_cambiar_ruta(ventana_ruta, qtbot, monkeypatch):
    """Simula la selección de una nueva ruta mediante QFileDialog"""
    nueva_ruta = "/home/user/nueva_ruta"

    def mock_getExistingDirectory(*args, **kwargs):
        return nueva_ruta
    
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", mock_getExistingDirectory)

    qtbot.mouseClick(ventana_ruta.boton_cambiar_ruta, Qt.LeftButton)
    
    assert ventana_ruta.ruta_actual == nueva_ruta

def test_restaurar_ruta_default(ventana_ruta, qtbot):
    """Verifica que la ruta se restaura a la predeterminada correctamente"""
    ventana_ruta.ruta_actual = "/home/user/prueba_guardado"
    qtbot.mouseClick(ventana_ruta.boton_restaurar_default, Qt.LeftButton)

    assert ventana_ruta.ruta_actual == ventana_ruta.ruta_default

def test_mensaje_notificacion(ventana_notificacion):
    """Verifica que el mensaje de éxito se muestra correctamente."""
    mensaje_esperado = "✅ Conversión Exitosa: archivo_prueba.txt"
    assert ventana_notificacion.label_ruta.text() == mensaje_esperado

def test_mensaje_error(qtbot):
    """Verifica que el mensaje de error se muestra correctamente cuando el archivo es None."""
    ventana = VentanaNotificacion(None, tiempo_cierre=1000)
    qtbot.addWidget(ventana)

    mensaje_esperado = "❌ Error al procesar: None"
    assert ventana.label_ruta.text() == mensaje_esperado

def test_cierre_automatico(qtbot):
    """Verifica que la ventana se cierra automáticamente después del tiempo configurado."""
    ventana = VentanaNotificacion("archivo_prueba.txt", tiempo_cierre=500)  # Reduce tiempo para prueba rápida
    qtbot.addWidget(ventana)
    ventana.show()

    qtbot.wait(600)  # Espera suficiente tiempo para la autocierre
    assert not ventana.isVisible()  # Comprueba que se cerró correctamente