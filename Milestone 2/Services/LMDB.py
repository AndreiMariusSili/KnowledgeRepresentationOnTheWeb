import os
import pickle
import urllib.parse
from typing import Iterable

import rdflib
import logging
from Services.ParallelExecutor import ParallelExecutor

logging.basicConfig(level='INFO')


class LMDB:

    def __init__(self, data_path: str, reset: bool = False, graph_only: bool = False):
        self._data_path = data_path
        self._original_file_path = os.path.join(data_path, 'Original.nt')
        self._cleaned_file_path = os.path.join(data_path, 'Cleaned.nt')
        self._malformed_file_path = os.path.join(data_path, 'Malformed.nt')
        self._graph_file_path = os.path.join(data_path, 'Graph.pkl')
        self.reset = reset
        self.graph_only = graph_only

        if os.path.isfile(self._original_file_path):
            if not not self.graph_only:
                self._original_file = open(self._original_file_path, 'r')
                self._original_file_size = sum([1 for _ in self._original_file.readlines()])
                self._original_file.close()
                self._original_file = open(self._original_file_path, 'r')
        else:
            raise Exception(
                'Original file {} does not exist'.format(os.path.join(os.getcwd(), self._original_file_path)))

        if self.reset:
            logging.info('Removing previously processed data.')
            os.remove(self._cleaned_file_path)
            os.remove(self._malformed_file_path)

        self._cleaned_file_size = 0
        if os.path.isfile(self._cleaned_file_path) and not self.graph_only:
            self._cleaned_file = open(self._cleaned_file_path, 'r+')
            self._cleaned_file_size = sum(1 for _ in self._cleaned_file.readlines())
            self._cleaned_file.close()
        self._cleaned_file = open(self._cleaned_file_path, 'ab+')

        self._malformed_file_size = 0
        if os.path.isfile(self._malformed_file_path) and not self.graph_only:
            self._malformed_file = open(self._malformed_file_path, 'r+')
            self._malformed_file_size = sum(1 for _ in self._malformed_file.readlines())
            self._malformed_file.close()
        self._malformed_file = open(self._malformed_file_path, 'ab+')

        if os.path.isfile(self._graph_file_path):
            logging.info('Loading graph from pickle.')
            self._graph_file = open(self._graph_file_path, 'rb')
            self._graph: rdflib.Graph = pickle.load(self._graph_file)
            logging.info('Loading done.')
        else:
            logging.info('No graph file to load.')
            self._graph_file = open(self._graph_file_path, 'wb+')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._original_file.close()
        self._cleaned_file.close()
        self._malformed_file.close()
        self._graph_file.close()

    def build_valid_graph(self) -> rdflib.Graph:
        """Build and save a valid graph from the n-tuples dump. Processing is done asynchronously.

        Returns:
            The valid RDFLIB graph.
        """
        valid_graph = rdflib.Graph()
        malformed_triples = []
        logging.info('Chunking {} triples.'.format(self._original_file_size))
        triple_chunks = ParallelExecutor.chunk(100000, self._original_file.readlines())
        logging.info('Finished chunking')
        for part_graph, part_mal_triples in ParallelExecutor.execute(LMDB.clean_triples, triple_chunks):
            valid_graph += part_graph
            malformed_triples += part_mal_triples
            logging.info('Processed {} and skipped {} of {} triples.'.format(len(valid_graph),
                                                                             len(malformed_triples),
                                                                             self._original_file_size))

        valid_graph.serialize(destination=self._cleaned_file_path, format='nt')
        pickle.dump(valid_graph, self._graph_file)
        for triple in malformed_triples:
            self._malformed_file.write(bytes(triple, encoding='utf-8'))

        return valid_graph

    def get_instances(self, cls_uri: str, prop_uri: str, unquote: bool) -> Iterable[str]:
        """Get all the instances of a particular LMDB class.

        Args:
            cls_uri: The URI of the class for which instances will be retrieved.
            prop_uri: the property values that will be retrieved.
            unquote: Whether to unquote the property uri.

        Returns:
            Dictionary of instances.
        """
        results = self._graph.query("""
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX lmdbm: <http://data.linkedmdb.org/resource/movie/>
            SELECT ?obj WHERE {{
                ?sub rdf:type {cls} .
                ?sub {prop} ?obj .
            }}""".format(cls=cls_uri, prop=prop_uri))
        if unquote:
            return map(self.unquote_uri, results)
        else:
            return map(lambda x: x, results)

    @staticmethod
    def unquote_uri(uri_tuple: tuple) -> str:
        """Unquote a URI.

        Returns:
            An unquoted uri as a string
        """
        uri_str = str(uri_tuple[0])
        return urllib.parse.unquote(uri_str)

    @staticmethod
    def clean_triples(triples: Iterable[str]):
        """Parse a list of triples, ignoring any malformed triples.

        Args:
            triples: An iterable of triples.

        Returns:
            The valid graph built from the triples.
        """
        partial_graph = rdflib.Graph()
        partial_malformed_triples = []
        for triple in triples:
            triple = triple.rstrip('\n')
            try:
                valid_triple = rdflib.Graph().parse(data=triple, format='nt')
                valid_triple = LMDB.unquote_triple(valid_triple)
                partial_graph += valid_triple
            except Exception as e:
                partial_malformed_triples.append(triple + '\n')

        return partial_graph, partial_malformed_triples


if __name__ == '__main__':
    with LMDB(data_path=os.path.join('..', 'Data', 'LMDB')) as lmdb:
        lmdb.build_valid_graph()
