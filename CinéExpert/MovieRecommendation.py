from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)

# Lists of unique values
unique_sentiments = ['Suspense', 'Inspiration', 'Réflexion', 'Divertissement', 'Adrénaline', 'Émotion']
unique_genres = ['Drame/Comédie dramatique', 'Mystère/Thriller', 'Action/Thriller', 'Science-fiction/Drame', 'Animation/Comédie', 'Comédie', 'Aventure/Fantastique', 'Drame']
unique_realisateurs = ['George Miller', 'Denis Villeneuve', 'David Fincher', 'John Lasseter', 'Damien Chazelle', 'Frank Darabont', 'Peter Jackson', 'Gabriele Muccino']
unique_acteurs = ['Tom Hardy', 'Ben Affleck', 'Tom Hanks', 'Will Smith', 'Ryan Gosling', 'Elijah Wood', 'Tim Robbins']
unique_durees = ['90-120', '120-150']

class RecommandationFilm(Fact):
    pass

class SystemeExpertFilms(KnowledgeEngine):
    result = None

    @Rule(RecommandationFilm(sentiment='Inspiration', genre='Drame/Comédie dramatique', Réalisateur='Gabriele Muccino', Acteur='Will Smith', Duree='90-120'))
    def regle1(self):
        self.result = "Film : The Pursuit of Happyness"

    @Rule(RecommandationFilm(sentiment='Suspense', genre='Mystère/Thriller', Réalisateur='David Fincher', Acteur='Ben Affleck', Duree='120-150'))
    def regle2(self):
        self.result = "Film : Gone Girl"

    @Rule(RecommandationFilm(sentiment='Adrénaline', genre='Aventure/Fantastique', Réalisateur='Peter Jackson', Acteur='Elijah Wood', Duree='120-150'))
    def regle3(self):
        self.result = "Film : Seigneur des Anneaux : La Communauté de l'Anneau"

    @Rule(RecommandationFilm(sentiment='Divertissement', genre='Animation/Comédie', Réalisateur='John Lasseter', Acteur='Tom Hanks', Duree='90-120'))
    def regle4(self):
        self.result = "Film : Toy Story"

    @Rule(RecommandationFilm(sentiment='Divertissement', genre='Comédie', Réalisateur='Damien Chazelle', Acteur='Ryan Gosling', Duree='90-120'))
    def regle5(self):
        self.result = "Film : La La Land"

    @Rule(RecommandationFilm(sentiment='Émotion', genre='Drame', Réalisateur='Frank Darabont', Acteur='Tim Robbins', Duree='120-150'))
    def regle6(self):
        self.result = "Film : Les Évadés"

    @Rule(RecommandationFilm(sentiment='Adrénaline', genre='Action/Thriller', Réalisateur='George Miller', Acteur='Tom Hardy', Duree='90-120'))
    def regle7(self):
        self.result = "Film : Mad Max: Fury Road"

    @Rule(RecommandationFilm(sentiment='Réflexion', genre='Science-fiction/Drame', Réalisateur='Denis Villeneuve', Acteur='Ryan Gosling', Duree='120-150'))
    def regle8(self):
        self.result = "Film : Blade Runner 2049"

# Initialize the expert system
moteur_films = SystemeExpertFilms()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        selected_genre = request.form.get("genre")
        selected_sentiment = request.form.get("sentiment")
        selected_realisateur = request.form.get("realisateur")
        selected_acteur = request.form.get("acteur")
        selected_duree = request.form.get("duree")

        # Pass form data to the expert system
        moteur_films.result = None 
        moteur_films.reset()
        moteur_films.declare(RecommandationFilm(
            sentiment=selected_sentiment,
            genre=selected_genre,
            Réalisateur=selected_realisateur,
            Acteur=selected_acteur,
            Duree=selected_duree
        ))

        # Run the expert system
        moteur_films.run()
        # Check if there's a result
        if moteur_films.result is None:
            moteur_films.result = "Aucun film recommandé pour les critères spécifiés."

    return render_template("index.html", 
                           genres=unique_genres, 
                           sentiments=unique_sentiments,
                           realisateurs=unique_realisateurs,
                           acteurs=unique_acteurs,
                           durees=unique_durees,
                           result=moteur_films.result)

if __name__ == "__main__":
    app.run(debug=True)
