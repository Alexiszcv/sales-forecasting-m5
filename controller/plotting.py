from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import io

def plot_prediction_on_label(X_test, y_pred, label_widget):
    # 1. Nettoyage
    label_widget.clear()

    # 2. Création du graphe
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#e5e5e5')
    ax.bar(X_test['d'], X_test['sales'], alpha=0.4, label="Ventes réelles")
    ax.bar(X_test['d'], y_pred, alpha=0.0001, hatch='//', label="Prédictions")
    ax.set_xlabel("Jour")
    ax.set_ylabel("Ventes") 
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    # 3. Conversion matplotlib → QPixmap
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img = QImage.fromData(buf.getvalue())
    pixmap = QPixmap.fromImage(img)

    # 4. Affichage dans le QLabel
    label_widget.setPixmap(pixmap)

    # 5. Libération mémoire
    plt.close(fig)
