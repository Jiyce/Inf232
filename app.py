import streamlit as st
import psycopg2
import os
import csv
from datetime import datetime

# Fonction pour exporter en CSV
def exporter_csv():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reponses")
    rows = cursor.fetchall()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'reponses'")
    columns = [col[0] for col in cursor.fetchall()]
    conn.close()
    return columns, rows

# Configuration de la page (DOIT être en premier)
st.set_page_config(page_title="Questionnaire Santé Sexuelle", page_icon="📋")

# CSS personnalisé responsive (après set_page_config)
st.markdown("""
<style>
    /* Style principal - Fond bleu clair */
    .stApp {
        background-color: #e3f2fd;
    }
    
    /* Titres - Bleu foncé */
    h1, h2, h3 {
        color: #1565c0 !important;
        font-weight: 700 !important;
    }
    
    /* Boutons - Bleu */
    .stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 12px 25px;
        font-weight: 600;
        font-size: 16px;
    }
    .stButton > button:hover {
        background-color: #1565c0 !important;
    }
    
    /* Sidebar - Gris clair */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5;
    }
    
    /* Metrics - Bleu */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #1976d2 !important;
    }
    
    /* Divider */
    hr {
        border-color: #1976d2;
    }
    
    /* Formulaires - responsive */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
        border: 1px solid #1976d2 !important;
        font-size: 16px !important;
    }
    
    /* Labels plus visibles */
    .stSelectbox label,
    .stTextArea label,
    .stNumberInput label {
        font-size: 16px !important;
        font-weight: 600 !important;
    }
    
    /* Responsive pour mobile */
    @media (max-width: 768px) {
        .stApp {
            padding: 10px;
        }
        h1 {
            font-size: 24px !important;
        }
        h2, h3 {
            font-size: 20px !important;
        }
        .stButton > button {
            width: 100%;
            padding: 15px;
            font-size: 18px;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        /* Formulaire plus large sur mobile */
        .stForm {
            padding: 10px;
        }
    }
    
    /* Messages plus lisibles */
    .stSuccess {
        font-size: 16px !important;
        padding: 15px !important;
    }
    
    /* Stats infos */
    .stInfo {
        font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# Connexion à la base de données PostgreSQL
@st.cache_resource
def connexion_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "aws-0-eu-west-1.pooler.supabase.com"),
        user=os.getenv("DB_USER", "postgres.xjsjifpburqlrzhlhjho"),
        password=os.getenv("DB_PASSWORD", "Flavimyfave!"),
        database=os.getenv("DB_NAME", "postgres"),
        port=os.getenv("DB_PORT", "6543"),
        sslmode="require"
    )

def get_connection():
    # Essayer DATABASE_URL sinon paramètres individuels
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return psycopg2.connect(db_url, sslmode="require")
    else:
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "aws-0-eu-west-1.pooler.supabase.com"),
            user=os.getenv("DB_USER", "postgres.xjsjifpburqlrzhlhjho"),
            password=os.getenv("DB_PASSWORD", "Flavimyfave!"),
            database=os.getenv("DB_NAME", "postgres"),
            port=os.getenv("DB_PORT", "6543"),
            sslmode="require"
        )

# Initialiser l'état de la page
if 'page' not in st.session_state:
    st.session_state.page = 'Accueil'

# Sidebar pour la navigation avec état initial
pages_list = ["Accueil", "Questionnaire", "Statistiques"]
current_index = pages_list.index(st.session_state.page) if st.session_state.page in pages_list else 0

st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", pages_list, index=current_index)

# Mettre à jour l'état quand on clique dans le sidebar
if page != st.session_state.page:
    st.session_state.page = page

# PAGE ACCUEIL
if st.session_state.page == "Accueil":
    st.title("📋 Questionnaire Santé Sexuelle")
    st.markdown("""
    Bienvenue dans notre questionnaire anonyme sur la santé sexuelle et reproductive.
    
    Ce questionnaire vise à collecter des données pour mieux comprendre les comportements 
    et les besoins en matière de santé sexuelle.
    
    **Votre participation est anonyme et volontaire.**
    """)
    
    if st.button("Commencer le Questionnaire"):
        st.session_state.page = "Questionnaire"
        st.rerun()

# PAGE QUESTIONNAIRE
elif st.session_state.page == "Questionnaire":
    st.title("📝 Questionnaire")
    
    with st.form("questionnaire_form"):
        st.header("Informations personnelles")
        age = st.selectbox("Âge", ["18-25", "26-35", "36-45", "46-55", "56+"])
        sexe = st.selectbox("Sexe", ["Homme", "Femme", "Autre"])
        
        st.header("Comportements et Connaissances")
        sensibilisation = st.selectbox("Avez-vous reçu une sensibilisation sur la santé sexuelle ?", ["Oui", "Non"])
        dernier_rapport = st.selectbox("Quand avez-vous eu votre dernier rapport sexuel ?", 
                                      ["Moins d'un mois", "1-3 mois", "3-6 mois", "Plus de 6 mois", "Jamais"])
        contraception = st.selectbox("Utilisez-vous une méthode contraceptive ?", 
                                    ["Oui", "Non", "Parfois"])
        preservatif = st.selectbox("Utilisez-vous des préservatifs ?", ["Toujours", "Parfois", "Jamais"])
        
        st.header("Santé et Prévention")
        mst = st.text_area("Avez-vous déjà eu une MST ? Si oui, laquelle ?")
        ist = st.selectbox("Connaissez-vous les IST ?", ["Oui", "Non", "Un peu"])
        prevention = st.text_area("Que faites-vous pour vous protéger ?")
        
        st.header("Opinions et Expériences")
        amelioration = st.text_area("Que pourrait-on améliorer dans la santé sexuelle ?")
        sexualite_precoce = st.text_area("Que pensez-vous de la sexualité précoce ?")
        facteurs = st.text_area("Quels sont les facteurs de risque pour la santé sexuelle ?")
        risques = st.text_area("Selon vous, quels sont les principaux risques ?")
        
        st.header("Accès aux Soins")
        partenaires = st.selectbox("Nombre de partenaires sexuels (12 derniers mois)", 
                                   ["0", "1", "2-3", "4-5", "Plus de 5"])
        age_premier_rapport = st.number_input("Âge du premier rapport sexuel", min_value=0, max_value=100, value=18)
        acces_sante = st.selectbox("Avez-vous facilement accès aux services de santé sexuelle ?", 
                                   ["Très facile", "Facile", "Difficile", "Très difficile"])
        protection = st.selectbox("Vous sentez-vous protégé(e) ?", ["Oui", "Non", "Parfois"])
        education = st.selectbox("Avez-vous reçu une éducation sexuelle à l'école ?", ["Oui", "Non"])
        difficultes = st.text_area("Avez-vous des difficultés à parler de santé sexuelle ?")
        frequence_sante = st.selectbox("Fréquence des dépistages de santé sexuelle", 
                                       ["Régulièrement", "Parfois", "Jamais", "Je ne sais pas"])
        
        submitted = st.form_submit_button("Soumettre")
        
        if submitted:
            if not amelioration or not sexualite_precoce or not facteurs or not risques or not difficultes or not prevention or not mst or not ist or not age or not sexe or not sensibilisation or not dernier_rapport or not contraception or not preservatif or not partenaires or not age_premier_rapport or not acces_sante or not protection or not education or not frequence_sante:
                st.warning("⚠️ Veuillez remplir tous les champs pour une meilleure analyse.")
            
            else:
                conn = get_connection()
                cursor = conn.cursor()
                
                
                    
                cursor.execute("""INSERT INTO reponses (age, sexe, sensibilisation, dernier_rapport, 
                                contraception, mst, amelioration, ist, prevention, sexualite_precoce, 
                                facteurs, risques, preservatif, partenaires, age_premier_rapport, 
                                acces_sante, protection, education, difficultes, frequence_sante) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (age, sexe, sensibilisation, dernier_rapport, contraception, mst,
                            amelioration, ist, prevention, sexualite_precoce, facteurs, risques,
                            preservatif, partenaires, age_premier_rapport, acces_sante, protection,
                            education, difficultes, frequence_sante))
                
                conn.commit()
                conn.close()
            
            st.success("✅ Merci ! Vos réponses ont été enregistrées avec succès !")
            st.balloons()

# PAGE STATISTIQUES
elif st.session_state.page == "Statistiques":
    st.title("📊 Statistiques des Réponses")
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Nombre total de réponses
        cursor.execute("SELECT COUNT(*) FROM reponses")
        total = cursor.fetchone()[0]
        st.metric("Total des réponses", total)
        
        # Répartition par sexe
        st.subheader("Répartition par sexe")
        cursor.execute("SELECT sexe, COUNT(*) FROM reponses GROUP BY sexe")
        resultats_sexe = cursor.fetchall()
        
        if resultats_sexe:
            for sexe, count in resultats_sexe:
                st.write(f"- **{sexe}** : {count}")
        
        # Graphique répartition par sexe
        if resultats_sexe:
            sexes = [s[0] for s in resultats_sexe]
            counts = [c[1] for c in resultats_sexe]
            st.bar_chart({"Sexe": dict(zip(sexes, counts))})
        
        st.divider()
        
        # Questions textuelles avec réponses fréquentes
        questions = ['risques', 'sexualite_precoce', 'facteurs', 'prevention', 'mst', 'amelioration', 'difficultes']
        
        for q in questions:
            st.subheader(f"📌 {q.replace('_', ' ').capitalize()}")
            cursor.execute(f"""
                SELECT LOWER(TRIM({q})), COUNT(*) as cnt
                FROM reponses
                WHERE {q} IS NOT NULL AND TRIM({q}) != ''
                GROUP BY LOWER(TRIM({q}))
                HAVING COUNT(*) > 1
                ORDER BY cnt DESC
            """)
            resultats = cursor.fetchall()
            
            if resultats:
                for rep, nb in resultats:
                    st.write(f"- {rep} ({nb})")
            else:
                st.info("Pas assez de réponses similaires pour afficher")
        
        conn.close()
        
    except psycopg2.Error as err:
        st.error(f"Erreur de connexion à la base de données : {err}")
    except Exception as e:
        st.error(f"Erreur : {e}")
    
    # Bouton pour télécharger CSV
    st.divider()
    st.subheader("📥 Télécharger les données")
    
    if st.button("Exporter en CSV"):
        try:
            columns, rows = exporter_csv()
            # Créer le CSV
            csv_data = ",".join(columns) + "\n"
            for row in rows:
                csv_data += ",".join([str(val) for val in row]) + "\n"
            
            st.download_button(
                label="📥 Télécharger fichier CSV",
                data=csv_data,
                file_name="reponses_questionnaire.csv",
                mime="text/csv"
            )
            st.success("✅ Fichier CSV prêt!")
        except Exception as e:
            st.error(f"Erreur: {e}")

# Instructions pour lancer l'app
st.sidebar.markdown("---")
st.sidebar.info("💡 Pour lancer : `streamlit run app.py`")
