from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import qtawesome as qta

def crear_menu_lateral(callback):
    # Crear el menú lateral como un QWidget
    menu_lateral = QWidget()
    layout_menu = QVBoxLayout()
    menu_lateral.setLayout(layout_menu)
    menu_lateral.setProperty("nombre_widget", "menu_lateral") # Añadimos una propiedad para identificarlo
    menu_lateral.setStyleSheet("QWidget[nombre_widget='menu_lateral'] { background-color: #F7F7F7; border:1px solid black; }")
    menu_lateral.setFixedWidth(150)  # Ancho fijo del menú lateral

    # Añadir elementos al menú
    lista_menu = QListWidget()
    lista_menu.setObjectName("lista_menu_lateral") # Le damos un nombre de objeto para identificarlo
    lista_menu.setFocusPolicy(Qt.NoFocus)
    lista_menu.setStyleSheet("""
        QListWidget#lista_menu_lateral {
            background-color: #F7F7F7;
            border: none;
            padding-bottom: 50px;
        }
        QListWidget#lista_menu_lateral::item {
            padding-top: 10px;
            padding-bottom: 10px;
        }
        QListWidget#lista_menu_lateral::item:hover {
            background-color: #DCDCDC;
            border-left: 5px solid #3498db;
        }
        QListWidget#lista_menu_lateral::item:selected {
            background-color: #F7F7F7;
            color: black;
            border-left: 5px solid #3498db;
        }
    """)

    # Crear íconos con qtawesome y asignarlos a los elementos
    items_con_iconos = [
        ("Inicio", qta.icon('fa5s.home', color='black')),
        ("Configuración", qta.icon('fa5s.cogs', color='black')),
        ("Escanear", qta.icon('fa5s.camera', color='black')),
        ("Salir", qta.icon('fa5s.sign-out-alt', color='black')),
    ]

    for texto, icono in items_con_iconos:
        item = QListWidgetItem(icono, texto)  # Asociar texto e ícono
        lista_menu.addItem(item)

    # Conectar eventos de clic al callback proporcionado
    lista_menu.itemClicked.connect(callback)
    layout_menu.addWidget(lista_menu)

    return menu_lateral, lista_menu # Devolvemos ambos: el widget contenedor y la lista interna