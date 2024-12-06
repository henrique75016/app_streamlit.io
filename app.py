import pandas as pd
import streamlit as st
from streamlit_authenticator import Authenticate

# Charger les données depuis un fichier CSV
df = pd.read_csv('comptes.csv')

# Vérifiez la structure du CSV
st.write(df)

# Convertir le DataFrame en un dictionnaire compatible avec streamlit_authenticator
Comptes = {
    'usernames': {}
}

for index, row in df.iterrows():
    Comptes['usernames'][row['name']] = {
        'name': row['name'],
        'password': row['password'],
        'email': row['email'],
        'failed_login_attemps': row['failed_login_attemps'],
        'logged_in': row['logged_in'],
        'role': row['role']
    }

# Initialisation de l'authentification
authenticator = Authenticate(
    Comptes,  # Les données des comptes
    "cookie_name",  # Nom du cookie (modifiable)
    "cookie_key",  # Clé du cookie (modifiable)
    30  # Durée de vie du cookie en jours
)

# Fonction d'accueil réservée aux utilisateurs connectés
def accueil():
    st.title("Bienvenue sur ma page")
    st.image("https://www.w3schools.com/w3images/lights.jpg", use_container_width=True)





# Fonction pour afficher les photos de l'album
def afficher_photos():
    st.header("Bienvenue dans l'album de mes animaux")
    # Afficher des images sous forme de galerie
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://static.streamlit.io/examples/cat.jpg", use_container_width=True)
    with col2:
        st.image("https://static.streamlit.io/examples/dog.jpg", use_container_width=True)
    with col3:
        st.image("https://static.streamlit.io/examples/owl.jpg", use_container_width=True)

# Fonction de connexion
def page_login():
    authenticator.login()

# Vérification de la session d'authentification
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None  # Initialiser la session

# Barre latérale avec les options, seulement après la connexion
if st.session_state["authentication_status"]:
    menu = st.sidebar.radio("Menu", ["Accueil", "Les photos de mes animaux"])

    if menu == "Accueil":
        accueil()  # Afficher la page d'accueil
    elif menu == "Les photos de mes animaux":
        afficher_photos()  # Afficher les photos du chat
else:
    page_login()  # Affichage du formulaire de connexion

# Vérifier le statut d'authentification
if st.session_state.get("authentication_status"):  # Si l'utilisateur est connecté
    # Ajouter un bouton de déconnexion
    authenticator.logout("Déconnexion")
elif st.session_state.get("authentication_status") is False:
    st.error("L'username ou le mot de passe est incorrect.")
elif st.session_state.get("authentication_status") is None:
    st.warning("Les champs username et mot de passe doivent être remplis.")
