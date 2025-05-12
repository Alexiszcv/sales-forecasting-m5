# Prévision des ventes avec le jeu de données M5

Ce projet a pour objectif de développer un produit de prévision des ventes en utilisant le jeu de données M5.

## Description du projet

L'objectif est de construire des modèles prédictifs capables d'anticiper les ventes futures à différents niveaux d'agrégation (article, magasin, état). Nous explorerons différentes techniques de séries temporelles ainsi que des approches de machine learning.

## Structure du projet

- Exploration et préparation des données
- Ingénierie des variables
- Entraînement et évaluation des modèles
- Visualisation des prévisions

## Installation

1. Créer un environnement virtuel :
    ```bash
    python -m venv projdatbi
    source projdatbi/bin/activate  # Sur Windows : projdatbi\Scripts\activate
    ```
2. Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Dépendances

Voir [requirements.txt](./requirements.txt).

## Licence

Ce projet est destiné à un usage éducatif et non commercial uniquement.
# sales-forecasting-m5

## Cleaning des données

Visualisation des données:

Beaucoup de journées à 0 vente (voir histogramme)

Organisation des données:

Aucune valeur vide sauf pour les colonnes "évènements" signalant si un évènement particulier était arrivé ce jour là. 
On a d'abord décidé de les remplacer par None au lieu de Nan. 

## Première méthode envisagée

Utilisation de Random Forest

Premier constat: Le classifieur "toujours prédire 0 vente" est meilleur 