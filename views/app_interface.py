from views.Interface import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtGui import QPixmap
from utils.paths import ICON_FIABILITE, ICON_HEATMAP, ICON_PREDICTION
from PyQt6.QtCore import Qt
from utils.constant import AVAILABLE_PRODUCTS, AVAILABLE_STORES
from models.predictions import predict_sales
from controller.get_user_inputs import get_user_inputs
from controller.plotting import plot_prediction_on_label

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
        # ComboBox Périodes de prédiction


        self.ui.comboDuree.addItem("Sélectionner")
        self.ui.comboDuree.addItems(["1 jour", "1 semaine", "1 mois", "1 an"])

        self.ui.comboProduit.addItem("Sélectionner")
        self.ui.comboProduit.addItems(AVAILABLE_PRODUCTS)

        self.ui.comboMagasin.addItem("Sélectionner")
        self.ui.comboMagasin.addItems(AVAILABLE_STORES)

    # Dans app_interface.py
    def lancer_prediction(self):
        print("Prédiction en cours...")
        inputs = get_user_inputs(self.ui)
        X_test, y_pred = predict_sales(inputs)
        plot_prediction_on_label(X_test, y_pred, self.ui.labelPrediction)

        