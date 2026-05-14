from backend.app import create_app

app = create_app()

@app.route("/")
def home():

    return "Le serveur fonctionne"

@app.route("/admin")
def admin():

    return "Bonjour admin"

if __name__ == "__main__":

    app.run(
        debug=True
    )
