import streamlit as st
import pandas as pd
import pickle
import numpy as np
import io

# --- Fonction de prétraitement pour la colonne 'Heure' ---
def convert_time_to_minutes(time_str):
    if pd.isna(time_str):
        return -1
    try:
        hours, minutes = map(int, str(time_str).split(':'))
        return hours * 60 + minutes
    except ValueError:
        return -1

# --- Chargement du pipeline et des colonnes originales ---
@st.cache_resource
def load_model_and_columns():
    try:
        model_pipeline = pickle.load(open('model_pipeline.pkl', 'rb'))
        original_columns = pickle.load(open('original_columns.pkl', 'rb'))
        return model_pipeline, original_columns
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du modèle : {e}")
        st.stop()

model_pipeline, original_columns = load_model_and_columns()

# --- Interface utilisateur Streamlit ---
st.title("🛡️ Détection de Fraude dans les Transactions")
st.write("Téléchargez un fichier CSV pour prédire les fraudes potentielles.")

uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file:
    try:
        file_content = uploaded_file.getvalue().decode('utf-8')

        if not file_content.strip():
            st.warning("❌ Le fichier est vide ou invalide.")
        else:
            df = pd.read_csv(io.StringIO(file_content))

            expected_columns = [
                'Montant', 'Heure', 'Type de paiement', 'Pays d\'origine',
                'Appareil utilisé', 'Tentatives de connexion', 'Localisation IP'
            ]

            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                st.error(f"❌ Colonnes manquantes : {', '.join(missing_cols)}.")
                st.info(f"Colonnes attendues : {', '.join(expected_columns)}.")
            else:
                df['Heure_minutes'] = df['Heure'].apply(convert_time_to_minutes)
                df = df.drop('Heure', axis=1)

                processed_df = df[original_columns]

                probas = model_pipeline.predict_proba(processed_df)
                predictions = model_pipeline.predict(processed_df)

                df_display = pd.read_csv(io.StringIO(file_content))
                df_display['Prédiction Fraude'] = predictions
                df_display['Confiance (%)'] = (probas.max(axis=1) * 100).round(2)
                df_display['Prédiction Fraude'] = df_display['Prédiction Fraude'].map({0: 'Non-Fraude', 1: 'Fraude'})

                st.success("✅ Prédictions générées avec succès.")
                st.dataframe(df_display)

                # Téléchargement du résultat
                csv_result = df_display.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Télécharger les résultats au format CSV", data=csv_result, file_name='résultats_fraude.csv', mime='text/csv')
    except Exception as e:
        st.error(f"❌ Erreur lors du traitement du fichier : {e}")
