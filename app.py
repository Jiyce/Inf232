from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

    #Connection à la base de données MySQL
def connexion_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Flavimyfave!",
        database="test_db"
    )
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/questionnaire1')
def questionnaire1():
    return render_template('questionnaire1.html')

@app.route('/questionnaire2', methods=['POST'])
def questionnaire2():
    data = request.form.to_dict()
    return render_template('questionnaire2.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    
    # Enregistrer les données dans la base de données
    conn = connexion_db()
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS reponses (
                       id SERIAL PRIMARY KEY,
                       age VARCHAR(20),
                       sexe VARCHAR(20),
                       sensibilisation VARCHAR(10),
                       dernier_rapport VARCHAR(10),
                       contraception VARCHAR(20),
                       mst TEXT,
                       amelioration TEXT,
                       ist VARCHAR(10),
                       prevention TEXT,
                       sexualite_precoce TEXT,
                       facteurs TEXT,
                       risques TEXT,
                       preservatif VARCHAR(10), 
                       partenaires VARCHAR(20),
                        age_premier_rapport INTEGER,
                         acces_sante VARCHAR(10),
                        protection VARCHAR(10),
                        education VARCHAR(10),
                        difficultes TEXT,
                        frequence_sante VARCHAR(20)
                       )""")
    
    cursor.execute("""INSERT INTO reponses (age, sexe, sensibilisation,dernier_rapport,contraception,mst, amelioration, ist, preservatif, partenaires, 
                       age_premier_rapport, acces_sante, protection, education, difficultes, 
                       frequence_sante, prevention, sexualite_precoce, facteurs, risques) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (data.get('age'), data.get('sexe'), data.get('sensibilisation'), data.get('dernier_rapport'), data.get('contraception'), data.get('mst'), data.get('amelioration'),
                        data.get('ist'), data.get('preservatif'), data.get('partenaires'), data.get('age_premier_rapport'), data.get('acces_sante'), data.get('protection'), 
                        data.get('education'), data.get('difficultes'), data.get('frequence_sante'), data.get('prevention'), data.get('sexualite_precoce'),
                        data.get('facteurs'), data.get('risques'))) 
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))
    
# STATS
@app.route('/stats')
def stats():
    conn = connexion_db()
    cursor = conn.cursor()
    
    # Récupérer toutes les réponses
    cursor.execute("SELECT * FROM reponses")
    reponses = cursor.fetchall()[0]
    
    # Répartition par sexe
    cursor.execute("""
                       SELECT sexe,  COUNT(*) 
                       FROM reponses
                       GROUP BY sexe
                          """)
    repartition_sexe = cursor.fetchall()
        
    questions_textuelles = ['risques', 'sexualite_precoce', 'facteurs', 'prevention', 'mst', 'amelioration', 'difficultes']
    stats_textuelles = {}
        
    for colonne in questions_textuelles:
            cursor.execute(f"""
                           SELECT sexe, LOWER(TRIM({colonne})) AS reponse, COUNT(*) as nb
                           FROM reponses
                           WHERE {colonne} IS NOT NULL AND TRIM({colonne}) != ''
                           GROUP BY sexe, reponse
                           HAVING COUNT(*) > 1
                           ORDER BY sexe,nb DESC
                        """)
            reponses = cursor.fetchall()
            stats_textuelles[colonne] = reponses
    conn.close()
    
    return render_template('stats.html', repartition_sexe=repartition_sexe, stats_textuelles=stats_textuelles)

if __name__ == '__main__':
    app.run(debug=True)
        
       
    
   