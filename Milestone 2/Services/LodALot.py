import logging
import os
import pickle
from typing import Iterable

import rdflib
import requests

logging.basicConfig(level='INFO')


class LodALot:
    __file_path: str
    __base_url: str
    __graph: rdflib.Graph

    def __init__(self, file_path: str, graph_path: str):
        self.__file_path = file_path
        self.__graph_path = graph_path
        if os.path.isfile(self.__graph_path):
            self.__graph = pickle.load(open(self.__graph_path, 'rb'))

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_triples(self, sub: str = None, pred: str = None, obj: str = None) -> None:
        """Get all the triples from LOD-A-LOT that match a specific pattern. Write the results to a file.

        Args:
            sub: The subject to match as a URI. If None, will match all subjects.
            pred: The predicate to match as URI. If None, will match all predicates.
            obj: The object to match as URI. If None, will match all objects.

        Returns:
            Dictionary of matching triples.
        """
        page = 1
        page_size = 1000
        headers = {'Accept': 'application/n-triples'}
        url = 'https://hdt.lod.labs.vu.nl/triple'
        max_pages = int(self.count_triples('<http://dbpedia.org/ontology/Film>')) / page_size
        payload = {
            'page': str(page),
            'page_size': '1000',
            's': str(sub),
            'p': str(pred),
            'o': str(obj),
            'g': '<https://hdt.lod.labs.vu.nl/graph/LOD-a-lot>'
        }

        r = requests.head(url=url, params=payload, headers=headers)
        req_triples = requests.get(r.url, headers=headers)

        with open(self.__file_path, 'a+') as triple_file:
            triple_file.write(req_triples.text)
        counter = 1
        while True:
            page += 1
            payload['page'] = str(page)
            req_triples = requests.get(url, params=payload, headers=headers)

            with open(self.__file_path, 'a+') as triple_file:
                triple_file.write(req_triples.text)
                counter += 1
                if counter >= max_pages:
                    break

        return self.__convert_to_rdf_graph()

    def __convert_to_rdf_graph(self) -> None:
        graph = rdflib.Graph()
        with open(self.__file_path, 'r') as triples:
            for tr in triples:
                tr = tr.replace('\n', '')
                try:
                    graph += rdflib.Graph().parse(data=tr, format='nt')
                except Exception as e:
                    logging.error(e)
        pickle.dump(graph, open(self.__graph_path, 'wb+'))

    @staticmethod
    def count_triples(obj: str = None) -> int:
        """Count all the triples from LOD-A-LOT that match a specific pattern.

                Args:
                    obj: The object to match as URI. If None, will match all objects.

                Returns:
                    Number of triples matching patterns
                """
        headers = {'Accept': 'application/json'}
        payload = {'o': str(obj), 'g': '<https://hdt.lod.labs.vu.nl/graph/LOD-a-lot>'}
        url = 'https://hdt.lod.labs.vu.nl/triple/count'
        count_triples = requests.get(url, headers=headers, params=payload)

        return count_triples.text

    def get_instances(self, prop_uri: str) -> Iterable[str]:
        """Get all the instances of a particular LMDB class.

        Args:
            prop_uri: the property values that will be retrieved.

        Returns:
            A map of instances.
        """
        if prop_uri == 'subject':
            results = self.__graph.query("""
                PREFIX owl: <http://www.w3.org/2002/07/owl#>
                PREFIX dbo: <http://dbpedia.org/ontology/>
                SELECT ?sub WHERE {
                    ?sub a dbo:Film
            }""")
            return map(lambda uri_tuple: str(uri_tuple[0]), results)
        else:
            pass


if __name__ == '__main__':
    logging.info('Info message')

    a = LodALot(os.path.join('..', 'Data', 'LodALot', 'RawTriples'))
    a.get_triples("", "", '<http://dbpedia.org/ontology/Film>')

    print("hey")

    # pass
