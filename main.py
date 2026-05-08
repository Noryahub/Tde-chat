from flask import Flask, render_template

# Initialisation de l'application Flask
app = Flask(__name__)

# Définition de la route pour la page d'accueil
@app.route("/")
def home():
    # Appel du template HTML index.html pour l'affichage
    return "Le serveur fonctionne"
# Définition d'une route supplémentaire pour la page admin
@app.route("/admin")
def admin():
    return "bonjour admin"

# Lancement de l'application
if __name__ == "__main__":
    # Le mode debug=True permet d'actualiser les modifications automatiquement
    app.run(debug=True)