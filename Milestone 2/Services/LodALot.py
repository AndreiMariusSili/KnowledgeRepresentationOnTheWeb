class LodALot:
    __file_path: str
    __base_url: str
    __graph: str

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


    def get_triples(self, sub: str = None, pred: str = None, obj: str = None) -> dict:
        """Get all the triples from LOD-A-LOT that match a specific pattern. Write the results to a file.

        Args:
            sub: The subject to match as a URI. If None, will match all subjects.
            pred: The predicate to match as URI. If None, will match all predicates.
            obj: The object to match as URI. If None, will match all objects.

        Returns:
            Dictionary of matching triples.
        """
        print("hey")
        import requests

        # DEFINE PARARMS
        page = 1

        payload = {'page': str(page), 'page_size': '1000', 's':str(sub), 'p':str(pred), 'o': str(obj), 'g':
            '<https://hdt.lod.labs.vu.nl/graph/LOD-a-lot>'}

        page_size = 1000
        headers = {'Accept': 'application/n-triples'}
        # payload = {'page': str(page),'page_size': '1000','o': '<http://dbpedia.org/ontology/Film>', 'g':
        # '<https://hdt.lod.labs.vu.nl/graph/LOD-a-lot>'}
        url = 'https://hdt.lod.labs.vu.nl/triple'

        max_pages = int(self.count_triples("","",'<http://dbpedia.org/ontology/Film>'))/page_size

        # REQUEST

        r = requests.head(url=url, params=payload, headers=headers)
        req_triples = requests.get(r.url, headers=headers)

        with open('triples', 'a') as tripple_file:
            tripple_file.write(req_triples.text)
        counter = 1
        while(1):
            page += 1
            payload['page'] = str(page)
            #print(req_triples.headers['link'])
            #r = requests.head(r.links["next"]["url"], params=payload, headers=headers)
            req_triples = requests.get(url,params=payload, headers=headers)
            #rint(req_triples.url)
            with open('triples', 'a') as tripple_file:
                tripple_file.write(req_triples.text)
                counter += 1
                #print(str(counter)+"000")
                if counter >= max_pages:
                    break




        return {}

    def convert_to_RDF_Graph(self) -> dict:

        import rdflib
        graph = rdflib.Graph()
        with open("triples",'r') as triples:

            for tr in triples:
                tr = tr.replace('\n', '')
                #print(tr)

                try:
                    graph += rdflib.Graph().parse(data = tr, format = 'nt')
                except:
                    x = 1

        graph.serialize(destination='movies_graph', format='turtle')

        with open('movies_graph') as infile, open('Movie_Graph', 'w') as outfile:
            for line in infile:

                if not line.strip():continue
                outfile.write(line)
        return 0








    def count_triples(self, sub: str = None, pred: str = None, obj: str = None) -> int:
        """Count all the triples from LOD-A-LOT that match a specific pattern.

                Args:
                    sub: The subject to match as a URI. If None, will match all subjects.
                    pred: The predicate to match as URI. If None, will match all predicates.
                    obj: The object to match as URI. If None, will match all objects.

                Returns:
                    Number of triples matching patterns
                """
        import requests

        headers = {'Accept': 'application/json'}
        payload = {'o': str(obj), 'g': '<https://hdt.lod.labs.vu.nl/graph/LOD-a-lot>'}
        url = 'https://hdt.lod.labs.vu.nl/triple/count'


        count_triples = requests.get(url, headers=headers,params = payload)
        print(count_triples.text)
        return count_triples.text




        return 0

import logging
logging.basicConfig(level='INFO')

if __name__ == '__main__':

    logging.info('Info message')



    a = LodALot()
    a.get_triples("","",'<http://dbpedia.org/ontology/Film>')
    a.convert_to_RDF_Graph()
    #a.count_triples()

    print("hey")

    #pass
