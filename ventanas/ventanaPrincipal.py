import subprocess
import platform
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ventanas.ventanaConfiguracion import VentanaConfiguracion
from ventanas.ventanaScaneo import VentanaEscaneo
from ventanas.ventanaOpcionesArchivo import VentanaOpcionesArchivos
from recursos.MenuLateral import crear_menu_lateral

import qtawesome as qta

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        # ... (tu código de inicialización) ...
        self.menu_lateral_widget = None # Añade una variable para guardar la referencia al widget del menú
        self.menu_lateral_lista = None  # Añade una variable para guardar la referencia a la lista del menú
        self.crear_interfaz()
        
        ruta_logo = os.path.join(os.path.dirname(__file__), "..","recursos/assets","logo.png")
      #  ruta_logo = os.path.abspath("../assets/logo.png")
        self.setWindowIcon(QIcon(ruta_logo))
        self.setStyleSheet("background-color: white")
        # Estilos generales para la ventana principal
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            QWidget {
                background-color: white;
                border: 1px solid #cfcfcf; /* Reemplaza box-shadow */
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #e6e6e6;
                color: #a0a0a0;
            }
            QLineEdit {
                background-color: #F5F5F5;
                border: 2px solid #87CEEB;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #4682B4;
                background-color: #FFFFFF;
            }
            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #DDDDDD;
                border-radius: 10px;
            }
            QLabel {
                font-family: Arial, sans-serif;
                font-size: 12pt;
            }
        """)
        self.crear_interfaz()


    def crear_interfaz(self):
        # Crear el contenedor principal
        contenedor_principal = QWidget()
        self.layout_principal = QHBoxLayout()  # Cambiamos a `self.layout_principal`
        contenedor_principal.setLayout(self.layout_principal)

        # Crear el menú lateral
        self.menu_lateral_widget, self.menu_lateral_lista = crear_menu_lateral(self.manejar_menu)
        self.layout_principal.addWidget(self.menu_lateral_widget)

        # Crear la región principal
        self.region_principal = self.crear_region_principal()
        self.layout_principal.addWidget(self.region_principal)

        self.setCentralWidget(contenedor_principal)



    def crear_region_principal(self):
            # Contenedor para la región principal
        region_principal = QWidget()
        layout_region = QVBoxLayout()
        region_principal.setLayout(layout_region)

        # Barra de búsqueda
        barra_busqueda = self.crear_barra_busqueda()
        layout_region.addWidget(barra_busqueda)

        # Lista de archivos
        self.lista_archivos = QListWidget()
        self.lista_archivos.setStyleSheet("""
            QListWidget {
                background-color: #FFFFFF;
                border: 1px solid #DDDDDD;
            }
        """)

        # Conectar el clic de un ítem al método que abre VentanaOpcionesArchivos
        self.lista_archivos.itemClicked.connect(self.abrir_opciones_archivo)

        layout_region.addWidget(self.lista_archivos)

        self.buscar_archivos()
        return region_principal

    def abrir_opciones_archivo(self, item):
        if item.flags() & Qt.ItemIsSelectable:
            nombre_archivo = item.text().strip()
            print(f"Archivo seleccionado: {nombre_archivo}")
            if nombre_archivo.endswith('.docx'):
                tarjeta = VentanaOpcionesArchivos(nombre_archivo,1)
            else:
                tarjeta = VentanaOpcionesArchivos(nombre_archivo,0)
            tarjeta.exec()
            #tarjeta.setParent(self)  # Establecer el padre para la tarjeta
            #tarjeta.move(300, 200)  # Posición en la ventana principal
            #tarjeta.show()

    def crear_barra_busqueda(self):
        # Contenedor para la barra de búsqueda
        barra_busqueda = QWidget()
        layout_busqueda = QHBoxLayout()
        barra_busqueda.setLayout(layout_busqueda)
        barra_busqueda.setFixedSize(600, 60)

        # Etiqueta de búsqueda
        etiqueta = QLabel("Buscar:")
        etiqueta.setStyleSheet(
            """
            QLabel {
                background-color: #F5F5F5; /* Fondo gris claro */
                border: 2px solid #87CEEB; /* Borde azul cielo */
                border-radius: 10px; /* Bordes redondeados */
                color: #333; /* Color del texto */
                font-size: 14px; /* Tamaño de la fuente */
            }
            QLabel:focus {
                border: 2px solid #4682B4; /* Borde azul más oscuro al hacer foco */
                background-color: #FFFFFF; /* Fondo blanco al hacer foco */
            }
        """
        )
        layout_busqueda.addWidget(etiqueta)

        # Campo de texto para la búsqueda
        self.campo_busqueda = QLineEdit()
        self.campo_busqueda.setPlaceholderText("Escribe aquí para buscar archivos...")
        self.campo_busqueda.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5; /* Fondo gris claro */
                border: 2px solid #87CEEB; /* Borde azul cielo */
                border-radius: 10px; /* Bordes redondeados */
                padding: 8px; /* Espaciado interno */
                color: #333; /* Color del texto */
                font-size: 14px; /* Tamaño de la fuente */
            }
            QLineEdit:focus {
                border: 2px solid #4682B4; /* Borde azul más oscuro al hacer foco */
                background-color: #FFFFFF; /* Fondo blanco al hacer foco */
            }
        """)
        layout_busqueda.addWidget(self.campo_busqueda)

        # Botón de búsqueda
        boton_buscar = QPushButton("")
        boton_buscar.setFixedSize(40, 40)
        boton_buscar.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB;
                border-radius: 20px;
            }
        """)
        boton_buscar.setIcon(qta.icon('fa5s.search', color='black'))
        boton_buscar.clicked.connect(self.buscar_archivos)
        layout_busqueda.addWidget(boton_buscar)

        # Botón para abrir el explorador de archivos
        boton_explorador = QPushButton("")
        boton_explorador.setFixedSize(40, 40)
        boton_explorador.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB;
                border-radius: 20px;
            }
        """)
        boton_explorador.setIcon(qta.icon('fa5s.folder-open', color='black'))
        boton_explorador.clicked.connect(self.abrir_explorador_archivos)
        layout_busqueda.addWidget(boton_explorador)

        # Botón para alternar entre modo oscuro y claro
        self.boton_modo = QPushButton("")
        self.boton_modo.setFixedSize(40, 40)
        self.boton_modo.setStyleSheet("""
            QPushButton {
                background-color: #87CEEB;
                border-radius: 20px;
            }
        """)
        self.boton_modo.setIcon(qta.icon('fa5s.moon', color='black'))  # Ícono inicial para modo oscuro
        self.boton_modo.setProperty("modo", "claro")  # Establecer modo inicial como claro
        self.boton_modo.clicked.connect(self.alternar_modo)
        layout_busqueda.addWidget(self.boton_modo)

        return barra_busqueda

    def alternar_modo(self):
        """Alterna entre modo oscuro y modo claro."""
        modo_actual = self.boton_modo.property("modo")
        if modo_actual == "claro":
            # Cambiar a modo oscuro
            self.setStyleSheet("""
                QMainWindow { background-color: #121212; }
                QWidget { background-color: #121212; border: 1px solid #333333; }
                QPushButton { background-color: #1E88E5; color: white; border-radius: 5px; padding: 5px 10px; }
                QPushButton:hover { background-color: #1565C0; }
                QPushButton:disabled { background-color: #424242; color: #BDBDBD; }
                QLineEdit { background-color: #424242; border: 2px solid #1E88E5; border-radius: 10px; padding: 8px; font-size: 14px; color: white; }
                QLineEdit:focus { border: 2px solid #1565C0; background-color: #616161; }
                QListWidget { background-color: #212121; border: 1px solid #424242; border-radius: 10px; color: white; }
                QLabel { font-family: Arial, sans-serif; font-size: 12pt; color: white; }
            """)
            if self.menu_lateral_widget:
                self.menu_lateral_widget.setStyleSheet("QWidget[nombre_widget='menu_lateral'] { background-color: #212121; border: 1px solid #424242; }")
            if self.menu_lateral_lista:
                self.menu_lateral_lista.setStyleSheet("""
                    QListWidget#lista_menu_lateral {
                        background-color: #212121;
                        border: none;
                        padding-bottom: 50px;
                        color: white;
                    }
                    QListWidget#lista_menu_lateral::item {
                        color: white;
                        padding-top: 10px;
                        padding-bottom: 10px;
                    }
                    QListWidget#lista_menu_lateral::item:hover {
                        background-color: #333333;
                        border-left: 5px solid #1E88E5;
                        color: white;
                    }
                    QListWidget#lista_menu_lateral::item:selected {
                        background-color: #212121;
                        color: white;
                        border-left: 5px solid #1E88E5;
                    }
                """)
            self.actualizar_estilo_lista_archivos("oscuro")
            self.boton_modo.setIcon(qta.icon('fa5s.sun', color='yellow'))
            self.boton_modo.setProperty("modo", "oscuro")
        else:
            # Cambiar a modo claro
            self.setStyleSheet("""
                QMainWindow { background-color: white; }
                QWidget { background-color: white; border: 1px solid #cfcfcf; }
                QPushButton { background-color: #007BFF; color: white; border-radius: 5px; padding: 5px 10px; }
                QPushButton:hover { background-color: #0056b3; }
                QPushButton:disabled { background-color: #e6e6e6; color: #a0a0a0; }
                QLineEdit { background-color: #F5F5F5; border: 2px solid #87CEEB; border-radius: 10px; padding: 8px; font-size: 14px; color: #333; }
                QLineEdit:focus { border: 2px solid #4682B4; background-color: #FFFFFF; }
                QListWidget { background-color: #FFFFFF; border: 1px solid #DDDDDD; border-radius: 10px; color: black; }
                QLabel { font-family: Arial, sans-serif; font-size: 12pt; color: black; }
            """)
            if self.menu_lateral_widget:
                self.menu_lateral_widget.setStyleSheet("QWidget[nombre_widget='menu_lateral'] { background-color: #F7F7F7; border: 1px solid black; }")
            if self.menu_lateral_lista:
                self.menu_lateral_lista.setStyleSheet("""
                    QListWidget#lista_menu_lateral {
                        background-color: #F7F7F7;
                        border: none;
                        padding-bottom: 50px;
                        color: black;
                    }
                    QListWidget#lista_menu_lateral::item {
                        color: black;
                        padding-top: 10px;
                        padding-bottom: 10px;
                    }
                    QListWidget#lista_menu_lateral::item:hover {
                        background-color: #DCDCDC;
                        border-left: 5px solid #3498db;
                        color: black;
                    }
                    QListWidget#lista_menu_lateral::item:selected {
                        background-color: #F7F7F7;
                        color: black;
                        border-left: 5px solid #3498db;
                    }
                """)
            self.actualizar_estilo_lista_archivos("claro")
            self.boton_modo.setIcon(qta.icon('fa5s.moon', color='black'))
            self.boton_modo.setProperty("modo", "claro")

    def actualizar_estilo_lista_archivos(self, modo):
        """Actualiza los colores de los elementos de la lista de archivos según el modo."""
        for i in range(self.lista_archivos.count()):
            item = self.lista_archivos.item(i)
            if item.text().startswith(">"):  # Es un encabezado de subcarpeta
                if modo == "oscuro":
                    item.setForeground(QColor("white"))  # Texto blanco
                    item.setBackground(QColor("#333333"))  # Fondo gris oscuro
                else:
                    item.setForeground(QColor("black"))  # Texto negro
                    item.setBackground(QColor("#DCDCDC"))  # Fondo gris claro
            else:  # Es un archivo
                if modo == "oscuro":
                    item.setForeground(QColor("white"))  # Texto blanco
                    item.setBackground(QColor("#212121"))  # Fondo gris oscuro
                else:
                    item.setForeground(QColor("black"))  # Texto negro
                    item.setBackground(QColor("#FFFFFF"))  # Fondo blanco


    def abrir_explorador_archivos(self):
        directorio_base = os.path.join(os.path.dirname(__file__), "..", "documentos")
        directorio_base = os.path.abspath(directorio_base)

        if os.path.exists(directorio_base):
            sistema = platform.system()

            try:
                if sistema == "Windows":
                    os.startfile(directorio_base)
                elif sistema == "Darwin":  # macOS
                    subprocess.Popen(["open", directorio_base])
                else:  # Linux
                    subprocess.Popen(["xdg-open", directorio_base])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el explorador:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Error", "El directorio no existe. Por favor, verifica la ruta.")


    def buscar_archivos(self):
        # Obtener el texto del campo de búsqueda
        texto_busqueda = self.campo_busqueda.text()

        # Directorio base para buscar archivos
        directorio_base = os.path.join(os.path.dirname(__file__), "..", "documentos")
        print(f"Directorio base: {directorio_base}")
        
        # Limpiar la lista de archivos mostrados
        self.lista_archivos.clear()

        # Verificar si el directorio existe antes de iterar
        if os.path.exists(directorio_base):
            for root, dirs, files in os.walk(directorio_base):
                if files:  # Si hay archivos en la carpeta actual
                    # Crear un encabezado para la subcarpeta
                    subcarpeta = os.path.relpath(root, directorio_base)  # Ruta relativa de la subcarpeta
                    encabezado = QListWidgetItem(f">{subcarpeta}")
                    encabezado.setFlags(Qt.ItemIsEnabled)  # Solo habilitado, para que sea visible pero no seleccionable
                    encabezado.setForeground(QColor("black"))  # Texto en negro para mejor visibilidad
                    encabezado.setBackground(QColor("#949494FF"))  # Fondo gris claro
                    self.lista_archivos.addItem(encabezado)

                    # Añadir los archivos de la subcarpeta
                    for archivo in files:
                        if archivo.endswith('.docx') or archivo.endswith('.pdf'):  # Filtrar por extensión, si es necesario
                            # Si hay texto de búsqueda, filtrar los resultados
                            if not texto_busqueda or texto_busqueda.lower() in archivo.lower():
                                item = QListWidgetItem(f"    {archivo}")
                                icono = qta.icon('fa5s.file', color='black')  # Ícono genérico
                                item.setIcon(icono)
                                self.lista_archivos.addItem(item)
        else:
            print("El directorio no existe. Por favor, verifica la ruta.")


    def manejar_menu(self, item):
        print(f"Seleccionaste: {item.text()}")
        if item.text() == "Inicio":
            self.volver_a_pantalla_principal()  # Regresa a la ventana principal
        elif item.text() == "Escanear":
            self.cambiar_a_ventana_escaneo()  # Cambia a la ventana de escaneo
        elif item.text() == "Configuración":
            #pass # Lo desabilito por que no hace nada aun
            tarjeta = VentanaConfiguracion()
            tarjeta.exec_()
        elif item.text() == "Salir":
            self.close()

    def cambiar_a_ventana_escaneo(self):
        # Eliminar el contenido actual de la región principal
        self.layout_principal.removeWidget(self.region_principal)
        self.region_principal.deleteLater()

        # Crear y añadir la nueva ventana (VentanaEscaneo)
        self.region_principal = VentanaEscaneo(self)  # Pasamos self como referencia
        self.layout_principal.addWidget(self.region_principal)
   
    def volver_a_pantalla_principal(self):
        # Eliminar el contenido actual de la región principal
        if self.region_principal:
            self.layout_principal.removeWidget(self.region_principal)
            self.region_principal.deleteLater()
            self.region_principal = None

        # Recrear la vista principal (barra de búsqueda + lista de archivos)
        self.region_principal = self.crear_region_principal()
        self.layout_principal.addWidget(self.region_principal)
