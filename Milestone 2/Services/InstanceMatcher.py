import collections as cl
import os

import rdflib

from Services.LMDB import LMDB
from Services.LodALot import LodALot


class InstanceMatcher:
    first_instances: map
    first_set: set

    second_instances: map
    second_set: set

    def __init__(self, first_instances: map, first_lookup: str, second_instances: map, second_lookup: str):
        pass

    def __load_instances(self) :
        """Process a dictionary of instances into a default dict of the form (URI: boolean)

        Args:
            instances: A dictionary of instances as returned by LMDB or LOD-A-LOT services.
            lookup:
        Returns:
            The instances loaded as a defaultdict(bool)
        """

        set_a = set()
        set_b = set()

        for x in self.first_instances:
            set_a.update(str(x))

        for y in self.second_instances:
            set_b.update(str(y))

        self.first_set = set_a
        self.second_set =set_b

        return ""


    def __get_conjunction(self) -> (set):
        """ Compute the conjunctive set of the 2 collections.

        Args:
            first_col: defaultdict as returned by self.load_instances.
            second_col: defaultdict as returned by self.load_instances.

        Returns:
            The conjunctive set and its cardinality.
        """
        con_set = set()
        con_set.update(self.first_set.intersection(self.second_set))

        print("con cardinality ", len(con_set))

        return con_set

    def __get_disjunction(self,first_col: cl.defaultdict, second_col: cl.defaultdict) -> (set, int):
        """ Compute the disjunctive set of the 2 collections.

            Args:
                first_col: defaultdict as returned by self.load_instances.
                second_col: defaultdict as returned by self.load_instances.

            Returns:
                The union set and its cardinality.
            """
        dis_set = set()
        dis_set.update(self.first_set.union(self.second_set))

        print("dis cardinality ", len(dis_set))

        return dis_set

    def get_similarity(self, sim_type: str) -> float:
        """ Compute the similarity of 2 classes.
        Args:
            sim_type: The type of similarity to compute.
        Returns:
            The Jaccard similarity between 2 measures.
        """

        conjunction_set = self.__get_conjunction()
        disjunction_set = self.__get_disjunction()

        jaccard_sim = len(conjunction_set)/len(disjunction_set)

        print("Jaccard Similarity ", jaccard_sim)

        return jaccard_sim


if __name__ == '__main__':
    with LMDB(os.path.join('..', 'Data', 'LMDB')) as lmdb:
        lmdb_instances = lmdb.get_instances()
    with LodALot() as lol:
        lol_instances = lol.get_instances()

    with InstanceMatcher(lmdb_instances, 'owl:sameAs', lol_instances, 'subject') as im:
        im.get_similarity("jaccard")
