from Services.DBPedia import DBPedia
from Services.Stardog import Stardog
from Services.TheMovieDatabase import TheMovieDatabase
import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    action = "lmdb_actor_to_dbpedia"
    if action == "discover":
        with TheMovieDatabase() as tmdb:
            tmdb.discover("movie", "2000", "2018")

    if action == "lmdb_movies_to_dbpedia":
        stardog = Stardog()
        dbpedia = DBPedia()
        uris = stardog.get_movies()
        response = dbpedia.match_movies(uris)

    if action == "lmdb_actor_to_dbpedia":
        stardog = Stardog()
        dbpedia = DBPedia()
        uris = stardog.get_actors()
        response = dbpedia.match_actors(uris)
