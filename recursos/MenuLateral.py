from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import qtawesome as qta

def crear_menu_lateral(callback):
    # Crear el menú lateral como un QWidget
    menu_lateral = QWidget()
    layout_menu = QVBoxLayout()
    menu_lateral.setLayout(layout_menu)
    menu_lateral.setStyleSheet("background-color: #F7F7F7; border:1px solid black;")
    menu_lateral.setFixedWidth(150)  # Ancho fijo del menú lateral
    
    # Añadir elementos al menú
    lista_menu = QListWidget()
    lista_menu.setFocusPolicy(Qt.NoFocus)
    lista_menu.setStyleSheet("""
        QListWidget {
            background-color: #F7F7F7;
            border: none;
            padding-bottom: 50px;
        }
        QListWidget:item {
            padding-top: 10px;
            padding-bottom: 10px;
        }
        QListWidget:item:hover {
            background-color: #DCDCDC;
            border-left: 5px solid #3498db;
        }
        QListWidget:item:selected {
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
    
    return menu_lateral
