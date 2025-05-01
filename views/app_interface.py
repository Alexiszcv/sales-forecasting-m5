from views.Interface import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QPixmap
from utils.paths import ICON_FIABILITE, ICON_HEATMAP, ICON_PREDICTION
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.initialiser_interface()  

        # Connexion bouton
        self.ui.predictionBtn.clicked.connect(self.lancer_prediction)

    def initialiser_interface(self):
        
        self.ui.labelPrediction.setPixmap(QPixmap(ICON_PREDICTION))
        self.ui.labelPrediction.setScaledContents(True)
        self.ui.labelPrediction.setMinimumSize(200, 200)  


        self.ui.labelHeatmap.setPixmap(QPixmap(ICON_HEATMAP))
        self.ui.labelHeatmap.setScaledContents(True)
        self.ui.labelHeatmap.setMinimumSize(200, 200) 

        self.ui.labelFiabilite.setPixmap(QPixmap(ICON_FIABILITE))
        self.ui.labelFiabilite.setScaledContents(True)
        self.ui.labelHeatmap.setMinimumSize(200, 200) 

        self.ui.labelPrediction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.labelHeatmap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.labelFiabilite.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ComboBox Périodes de prédiction


        self.ui.comboDuree.addItem("Sélectionner")
        self.ui.comboDuree.addItems(["1 jour", "1 semaine", "1 mois", "1 an"])

        # ComboBox Villes disponibles 
        # Tu peux les lire dynamiquement avec pandas si tu veux, mais en dur :
        villes_disponibles = ["CA_1", "CA_2", "TX_1", "WI_2"]  # à adapter à ton dataset M5
        self.ui.comboMagasin.addItem("Sélectionner")
        self.ui.comboMagasin.addItems(villes_disponibles)

    def lancer_prediction(self):
        # 🔸 Ici tu vas :
        # - effacer les icônes (clear)
        # - lancer la prédiction
        # - afficher les résultats
        print("Prédiction en cours...")