import logging
import pprint

from SPARQLWrapper import SPARQLWrapper, TURTLE, CONSTRUCT
from SPARQL import Queries
from typing import Tuple


class DBPedia:
    __endpoint = None
    __sparql = None

    def __init__(self):
        self.__endpoint = "http://dbpedia.org/sparql"
        self.__sparql = SPARQLWrapper(self.__endpoint)
        self.__sparql.setReturnFormat(TURTLE)
        self.__sparql.setMethod(CONSTRUCT)

    def match_movies(self, uri_chunks: Tuple):
        response = None
        skipped = 0
        with open('Data/DBPediaMovies.ttl', 'wb') as output:
            for uri_chunk in uri_chunks:
                uri_string = "(" + "".join(uri + "," for uri in uri_chunk)[:-1] + ")"

                try:
                    self.__sparql.setQuery(Queries.dbpedia_uris_to_resources(uri_string, 'Film'))
                    response = self.__sparql.query().convert()
                except Exception as e:
                    logging.warning("Exception occurred. Skipped so far: {}".format(skipped))
                    pprint.pprint(uri_chunk)
                    skipped += len(uri_chunk)
                    continue

                output.write(response)
                output.flush()

        return response

    def match_actors(self, uri_chunks: Tuple):
        response = None
        skipped = 0
        with open('Data/DBPediaActors.ttl', 'wb') as output:
            for uri_chunk in uri_chunks:
                uri_string = "(" + "".join(uri + "," for uri in uri_chunk)[:-1] + ")"

                try:
                    self.__sparql.setQuery(Queries.dbpedia_uris_to_resources(uri_string, 'Person'))
                    response = self.__sparql.query().convert()
                except Exception as e:
                    skipped += len(uri_chunk)
                    logging.warning("Exception occurred. Skipped so far: {}".format(skipped))
                    pprint.pprint(uri_chunk)
                    continue

                output.write(response)
                output.flush()

        return response
