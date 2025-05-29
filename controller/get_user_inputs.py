def get_user_inputs(ui) -> dict:

    selected_store = ui.comboMagasin.currentText()
    selected_product = ui.comboProduit.currentText()
    selected_period = ui.comboDuree.currentText()

    # vérifie que les valeurs ne sont pas restées sur "Sélectionner"
    if selected_store == "Sélectionner" or selected_product == "Sélectionner":
        return None
    
    # Conversion de la durée de prédiction sélectionnée en entier
    periode_mapping = {
    "1 jour": 1,
    "1 semaine": 7,
    "1 mois": 30,
    "1 an": 365
    }
    period = periode_mapping.get(selected_period, 30)  # valeur par défaut : 30 jours

    return {
        "store_id": selected_store,
        "item_id": selected_product,
        "period": period
    }






