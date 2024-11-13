import streamlit as st
import pandas as pd
import uuid

# Initialisation de session_state pour gérer plusieurs biens
if "biens" not in st.session_state:
    st.session_state["biens"] = []

# Fonction pour ajouter un bien
def ajouter_bien():
    unique_id = str(uuid.uuid4())
    bien = {
        "nom": st.text_input("Nom du bien", key=f"nom_{unique_id}"),
        "prix_achat": st.number_input("Prix d'achat (€)", min_value=0, max_value=4000000, step=1000, key=f"prix_achat_{unique_id}"),
        "travaux": st.number_input("Travaux (€)", min_value=0, max_value=200000, step=1000, key=f"travaux_{unique_id}"),
        "loyer_mensuel": st.number_input("Loyer mensuel (€)", min_value=0, max_value=5000, step=10, key=f"loyer_mensuel_{unique_id}"),
        "charges_copropriete": st.number_input("Charges copropriété (mensuel) (€)", min_value=0, max_value=1000, step=5, key=f"charges_copropriete_{unique_id}"),
        "taxe_fonciere": st.number_input("Taxe foncière (annuel) (€)", min_value=0, max_value=5000, step=10, key=f"taxe_fonciere_{unique_id}"),
        "apport": st.number_input("Apport (€)", min_value=0, max_value=4000000, step=1000, key=f"apport_{unique_id}"),
        "montant_pret": st.number_input("Montant du prêt (€)", min_value=0, max_value=4000000, step=1000, key=f"montant_pret_{unique_id}"),
        "interet_annuel": st.number_input("Taux d'intérêt (%)", min_value=0.0, max_value=10.0, step=0.1, key=f"interet_annuel_{unique_id}"),
        "taux_assurance": st.number_input("Taux assurance (%)", min_value=0.0, max_value=4.0, step=0.1, key=f"taux_assurance_{unique_id}"),
        "duree_pret": st.slider("Durée du prêt (années)", min_value=1, max_value=30, value=20, key=f"duree_pret_{unique_id}")
    }
    st.session_state["biens"].append(bien)
    st.experimental_rerun()  # Force le rafraîchissement de la page

# Interface d'ajout de bien
st.title("Comparateur de Biens Locatifs")

# Bouton pour ajouter un bien
if st.button("Ajouter un bien"):
    ajouter_bien()

# Calcul des indicateurs pour chaque bien dans la liste
for bien in st.session_state["biens"]:
    frais_notaires = (8 / 100) * bien["prix_achat"]
    cout_total_bien = bien["prix_achat"] + frais_notaires + bien["travaux"]
    revenu_locatif_annuel = bien["loyer_mensuel"] * 12
    rentabilite_brute = (revenu_locatif_annuel / max(cout_total_bien, 1)) * 100
    frais_annuels_total = (bien["charges_copropriete"] * 12) + bien["taxe_fonciere"]
    rentabilite_nette = ((revenu_locatif_annuel - frais_annuels_total) / max(cout_total_bien, 1)) * 100
    taux_mensuel = bien["interet_annuel"] / 100 / 12
    mensualite_pret = bien["montant_pret"] * taux_mensuel / (1 - (1 + taux_mensuel) ** (-bien["duree_pret"] * 12)) if taux_mensuel != 0 else 0
    mensualite_assurance = (bien["montant_pret"] * bien["taux_assurance"] / 100) / 12
    mensualite_pret_totale = mensualite_pret + mensualite_assurance
    cashflow_mensuel = bien["loyer_mensuel"] - (frais_annuels_total / 12) - mensualite_pret_totale

    bien.update({
        "frais_notaires": frais_notaires,
        "cout_total_bien": cout_total_bien,
        "revenu_locatif_annuel": revenu_locatif_annuel,
        "rentabilite_brute": rentabilite_brute,
        "rentabilite_nette": rentabilite_nette,
        "mensualite_pret_totale": mensualite_pret_totale,
        "cashflow_mensuel": cashflow_mensuel
    })

# Affichage du tableau récapitulatif
if st.session_state["biens"]:
    data = {
        "Nom du bien": [bien["nom"] for bien in st.session_state["biens"]],
        "Prix d'achat (€)": [bien["prix_achat"] for bien in st.session_state["biens"]],
        "Loyer mensuel (€)": [bien["loyer_mensuel"] for bien in st.session_state["biens"]],
        "Frais notaires (€)": [bien["frais_notaires"] for bien in st.session_state["biens"]],
        "Coût total bien (€)": [bien["cout_total_bien"] for bien in st.session_state["biens"]],
        "Revenu locatif annuel (€)": [bien["revenu_locatif_annuel"] for bien in st.session_state["biens"]],
        "Rentabilité brute (%)": [bien["rentabilite_brute"] for bien in st.session_state["biens"]],
        "Rentabilité nette (%)": [bien["rentabilite_nette"] for bien in st.session_state["biens"]],
        "Mensualité prêt (€)": [bien["mensualite_pret_totale"] for bien in st.session_state["biens"]],
        "Cashflow mensuel (€)": [bien["cashflow_mensuel"] for bien in st.session_state["biens"]],
    }
    df = pd.DataFrame(data)
    st.subheader("Comparatif des biens")
    st.dataframe(df.style.format({
        "Prix d'achat (€)": "{:,.2f}",
        "Frais notaires (€)": "{:,.2f}",
        "Coût total bien (€)": "{:,.2f}",
        "Revenu locatif annuel (€)": "{:,.2f}",
        "Rentabilité brute (%)": "{:.2f}",
        "Rentabilité nette (%)": "{:.2f}",
        "Mensualité prêt (€)": "{:,.2f}",
        "Cashflow mensuel (€)": "{:.2f}"
    }))
else:
    st.write("Aucun bien ajouté pour le moment.")
