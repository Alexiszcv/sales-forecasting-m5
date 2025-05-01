import os

# Dossier racine du projet = remonter depuis utils/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dossier contenant les images
IMAGES_DIR = os.path.join(ROOT_DIR, "views", "images")

# Dossier des datasets
DATA_DIR = os.path.join(ROOT_DIR, "data")

# Chemins précis
ICON_PREDICTION = os.path.join(IMAGES_DIR, "icone_prediction.png")
ICON_HEATMAP = os.path.join(IMAGES_DIR, "icone_heatmap.png")
ICON_FIABILITE = os.path.join(IMAGES_DIR, "icone_precision.png")

DATA_SALES = os.path.join(DATA_DIR, "sales_train_validation.csv")
DATA_CALENDAR = os.path.join(DATA_DIR, "calendar.csv")

