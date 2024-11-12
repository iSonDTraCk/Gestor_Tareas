# src/logica/gestor_tareas.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QStringListModel
from src.vista.gestor_tareasGUI import Ui_Dialog

class Tarea:
    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        self.completada = False

class GestorTareas:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, titulo, descripcion):
        if not titulo:
            raise ValueError("El título no puede estar vacío")
        tarea = Tarea(titulo, descripcion)
        self.tareas.append(tarea)

    def obtener_tareas(self):
        return self.tareas

    def marcar_completada(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].completada = True
        else:
            raise IndexError("Índice fuera de rango")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
        else:
            raise IndexError("Índice fuera de rango")

class GestorTareasGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Instance of the task manager
        self.gestor = GestorTareas()

        # Connect buttons to their respective functions
        self.ui.pbAdd.clicked.connect(self.agregar_tarea)
        self.ui.pbCheck.clicked.connect(self.marcar_completada)
        self.ui.pbDelete.clicked.connect(self.eliminar_tarea)
        self.ui.pbExit.clicked.connect(self.close)

        # Create a model for the QListView
        self.model = QStringListModel()
        self.ui.listWorks.setModel(self.model)

        # Update task list display
        self.actualizar_lista()

    def agregar_tarea(self):
        # Get title and description from the text fields
        titulo = self.ui.txtName.toPlainText().strip()
        descripcion = self.ui.txtDetail.toPlainText().strip()
        try:
            # Add the new task using the task manager
            self.gestor.agregar_tarea(titulo, descripcion)
            # Update the list of tasks
            self.actualizar_lista()
            # Clear input fields
            self.ui.txtName.clear()
            self.ui.txtDetail.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

    def actualizar_lista(self):
        lista_tareas = []
        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            estado = "Completada" if tarea.completada else "Pendiente"
            lista_tareas.append(f"{indice + 1}. {tarea.titulo} - {estado}")
        # Update the model with the new list of tasks
        self.model.setStringList(lista_tareas)

    def marcar_completada(self):
        current_row = self.ui.listWorks.currentIndex().row()
        if current_row != -1:
            self.gestor.marcar_completada(current_row)
            self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una tarea para marcar como completada")

    def eliminar_tarea(self):
        current_row = self.ui.listWorks.currentIndex().row()
        if current_row != -1:
            self.gestor.eliminar_tarea(current_row)
            self.actualizar_lista()
        else:
            QMessageBox.warning(self, "Advertencia", "Selecciona una tarea para eliminar")

def main():
    app = QApplication(sys.argv)
    window = GestorTareasGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
