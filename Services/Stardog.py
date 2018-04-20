import logging

from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, List, Tuple
from SPARQL import Queries
import urllib.parse


class Stardog:
    __endpoint = None
    __sparql = None

    def __init__(self):
        self.__endpoint = "http://localhost:5820/BetterLinkedMDB/query"
        self.__sparql = SPARQLWrapper(self.__endpoint)
        self.__sparql.setReturnFormat(JSON)

    def get_movies(self)-> Tuple:
        """Get the DBPedia resource URI of all movies in Stardog LinkedMDB.

        Returns:
            List: the list of unqouted uris in 50 pieces chunks.
        """
        self.__sparql.setQuery(Queries.lmdb_movies_to_dbpedia_uris())
        response = self.__sparql.query().convert()
        uris = list(map(Stardog.__to_uri, response["results"]["bindings"]))
        uris = list(filter(Stardog.__no_bad_uris, uris))
        return tuple(tuple(uris[i:i+50]) for i in range(0, len(uris), 50))

    def get_actors(self) -> Tuple:
        """Get the DBPedia resource URI of all actors in Stardog LinkedMDB.

            Returns:
                List: the list of unqouted uris in 50 pieces chunks.
        """
        self.__sparql.setQuery(Queries.lmdb_actors_to_dbpedia_uris())
        response = self.__sparql.query().convert()
        uris = list(map(Stardog.__to_uri, response["results"]["bindings"]))
        uris = list(filter(Stardog.__no_bad_uris, uris))

        return tuple(tuple(uris[i:i + 100]) for i in range(0, len(uris), 100))

    @staticmethod
    def __to_uri(resource: Dict) -> str:
        """Parse the URI string from a result resource.

        Args:
            resource: a resource dictionary returned by the SPARQL endpoint.

        Returns: The string representation of the resource URI.
        """
        return """<""" + urllib.parse.unquote(resource['uri']['value'], encoding='utf8', errors='strict') + """>"""

    @staticmethod
    def __no_bad_uris(uri):
        if '@' in uri:
            logging.info('URI has bad character @: {}'.format(uri))
            return False
        return True
