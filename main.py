from PyQt6.QtWidgets import QApplication
from views.app_interface import MainWindow
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)     # Initialise l'application Qt
    window = MainWindow()            # Crée ta fenêtre principale (définie dans app_interface.py)
    window.show()                    # Affiche la fenêtre
    sys.exit(app.exec())           # Lance la boucle principale de l'app

