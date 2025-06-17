import random
import pandas as pd

def generate_clean_data(n):
    rows = []
    for _ in range(n):
        montant = round(random.uniform(10, 20000), 2)
        heure = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        type_paiement = random.choice(["Carte bancaire", "En ligne", "Espèces", "Virement", "Cryptomonnaie"])
        pays_origine = random.choice(["Maroc", "France", "États-Unis", "Chine", "Brésil"])
        appareil_utilisé = random.choice(["Mobile", "Ordinateur", "Tablette", "ATM"])
        tentative_connexion = random.randint(1, 5)
        localisation_ip = random.choice(["Casablanca", "Rabat", "Paris", "New York", "Pékin", "São Paulo"])
        is_fraud = random.choices([1, 0], weights=[0.1, 0.9])[0]  # 10% fraude
        rows.append([
            montant, heure, type_paiement, pays_origine,
            appareil_utilisé, tentative_connexion, localisation_ip, is_fraud
        ])
    return rows

# Colonnes
colonnes = [
    "Montant", "Heure", "Type de paiement", "Pays d'origine",
    "Appareil utilisé", "Tentatives de connexion", "Localisation IP", "is_fraud"
]

# Générer les données et créer DataFrame
df = pd.DataFrame(generate_clean_data(1000), columns=colonnes)

# Sauvegarder dans un fichier CSV
df.to_csv("transactions_1000.csv", index=False, encoding="utf-8")

print("✅ Fichier 'transactions_1000.csv' généré avec succès.")
