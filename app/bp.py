from flask import current_app as app, request
from flask_restx import Api, Resource

from app import models, schemas
from app.models import db

api: Api = app.config['api']
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movie_schema = schemas.Movie()
movies_schema = schemas.Movie(many=True)

director_schema = schemas.Director()
directors_schema = schemas.Director(many=True)

genre_schema = schemas.Genre()
genres_schema = schemas.Genre(many=True)


@movies_ns.route('/')
class MoviesViews(Resource):

    def get(self):
        movies = db.session.query(models.Movie)

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies = movies.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies = movies.filter(models.Movie.genre_id == genre_id)

        movies = movies.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()

        return None, 201


@movies_ns.route('/<int:movie_id>')
class MovieViews(Resource):

    def get(self, movie_id):
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

        if movie is None:
            return {}, 404

        return movie_schema.dump(movie), 200

    def put(self, movie_id):
        db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)
        db.session.commit()

        return None, 204

    def delete(self, movie_id):
        db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
        db.session.commit()

        return None, 200


@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200


@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):

    def get(self, director_id):
        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()

        if director is None:
            return {}, 404

        return director_schema.dump(director), 200


@genres_ns.route('/')
class GenresView(Resource):

    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id):
        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()

        if genre is None:
            return {}, 404

        return genre_schema.dump(genre), 200



