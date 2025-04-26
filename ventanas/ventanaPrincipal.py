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
        
        self.setWindowTitle("CScan")
        self.resize(800, 600)
        
        ruta_logo = os.path.join(os.path.dirname(__file__), "..","assets","logo.png")
      #  ruta_logo = os.path.abspath("../assets/logo.png")
        self.setWindowIcon(QIcon(ruta_logo))
        self.setStyleSheet("background-color: white")

        self.crear_interfaz()


    def crear_interfaz(self):
        # Crear el contenedor principal
        contenedor_principal = QWidget()
        self.layout_principal = QHBoxLayout()  # Cambiamos a `self.layout_principal`
        contenedor_principal.setLayout(self.layout_principal)
        
        # Crear el menú lateral
        menu_lateral = crear_menu_lateral(self.manejar_menu)
        self.layout_principal.addWidget(menu_lateral)

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
            tarjeta = VentanaOpcionesArchivos(nombre_archivo)
            tarjeta.setParent(self)  # Establecer el padre para la tarjeta
            tarjeta.move(300, 200)  # Posición en la ventana principal
            tarjeta.show()

    def crear_barra_busqueda(self):
        # Contenedor para la barra de búsqueda
        barra_busqueda = QWidget()
        layout_busqueda = QHBoxLayout()
        barra_busqueda.setLayout(layout_busqueda)
        barra_busqueda.setFixedSize(500, 60)
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
        QPushButton{
        background-color:#87CEEB;
        border-radius:20px;
        }
    """)
        boton_buscar.setIcon(qta.icon('fa5s.search', color='black'))
        boton_buscar.clicked.connect(self.buscar_archivos)
        layout_busqueda.addWidget(boton_buscar)

        return barra_busqueda



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
                    encabezado.setBackground(QColor("#DCDCDC"))  # Fondo gris claro
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
            pass # Lo desabilito por que no hace nada aun
         #  tarjeta = VentanaConfiguracion()
           # tarjeta.exec_()
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
