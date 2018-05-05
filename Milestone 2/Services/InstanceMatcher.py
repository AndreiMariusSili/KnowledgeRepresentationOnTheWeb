import collections as cl


class InstanceMatcher:
    first_instances: dict
    first_col: cl.defaultdict

    second_instance: dict
    second_col: cl.defaultdict

    def __init__(self, first_instances: str, first_lookup: str, second_instances: str, second_lookup: str):
        pass

    def __load_instances(self, instances: str, lookup: str) -> cl.defaultdict:
        """Process a dictionary of instances into a default dict of the form (URI: boolean)

        Args:
            instances: A dictionary of instances as returned by LMDB or LOD-A-LOT services.
            lookup:

            ??Maybe query as argument too? and which graph

        Returns:

        """
        import rdflib
        from rdflib import Graph

        #INIT DEF DICT
        from collections import defaultdict
        d = defaultdict(bool)

        #QUERY GRAPH
        g = Graph()
        gr = g.parse("Movie_Graph.nt", format='turtle')
        q = "SELECT  DISTINCT  ?sub  WHERE {            ?sub a <http://dbpedia.org/ontology/Film>   .            }"
        x = gr.query(q)

        for row in x.result:
            d[row] = True
            print(row)

        return d

    def __get_conjunction(self, first_col: cl.defaultdict, second_col: cl.defaultdict) -> (set, int):
        """ Compute the conjunctive set of the 2 collections.

        Args:
            first_col: DefaultDict as returned by self.load_instances.
            second_col: DefaultDict as returned by self.load_instances.

        Returns:
            The conjunctive set and its cardinality.
        """
        con = set()
        counter = 0

        for key in first_col:
            if key in first_col:
                if key in second_col:
                    con.update(key)
                    counter += 1
        print("con is ",counter)
        print("con the same is ",len(con))

        return con, len(con)

    def __get_disjunction(self, first_col: cl.defaultdict, second_col: cl.defaultdict) -> (set, int):
        """ Compute the disjunctive set of the 2 collections.

            Args:
                first_col: DefaultDict as returned by self.load_instances.
                second_col: DefaultDict as returned by self.load_instances.

            Returns:
                The disjunctive set and its cardinality.
            """
        dis = set()
        counter = 0

        for key in first_col:
            if key in first_col:
                if key in second_col:
                    dis.update(key)
                    counter += 1
        print("dis is ",counter)
        print("dis the same is ",len(dis))


        return dis, len(dis)

    def get_similarity(self, sim_type: str) -> float:
        """ Compute the similarity of 2 classes.
        Args:
            sim_type: The type of similarity to compute.
        Returns:
            The Jaccard similarity between 2 measures.
        """
        from collections import defaultdict

        d1 = self.__load_instances(" ", " ")
        #d2 = self.__load_instances(" ", " ")
        #d2 = dict(d1.items())[len(d1) / 2:]

        # half_dict = int(len(d1)/2)
        # d2 = defaultdict(bool)
        # counter = 0
        # for key in d1:
        #     d2[key] = True
        #     counter += 1
        #     if counter >= half_dict:
        #         break
        # print("how many",len(d2))

        d2 = defaultdict(bool, list(d1.items())[0:int(len(d1) / 2)])
        print("d2 ",len(d2))


        common_set, len_common = self.__get_conjunction(d1,d2)
        not_common_set, len_not_common = self.__get_disjunction(d1,d2)

        ja_sim = int(len_common) / (len(d1) + len(d2) - int(len_common))
        print("d1 ",len(d1))
        print("d2 ",len(d2))

        print("common ",len_common)

        print("Similarity ",ja_sim)




        return 0.5

if __name__ == '__main__':

    a = InstanceMatcher(" "," "," "," ")
    a.get_similarity("")
    #a.count_triples()

    print("hey")

    #pass
