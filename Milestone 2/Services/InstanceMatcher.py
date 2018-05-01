import collections as cl


class InstanceMatcher:
    first_instances: dict
    first_col: cl.defaultdict

    second_instance: dict
    second_col: cl.defaultdict

    def __init__(self, first_instances: dict, first_lookup: str, second_instances: dict, second_lookup: str):
        pass

    def __load_instances(self, instances: dict, lookup: str) -> cl.defaultdict:
        """Process a dictionary of instances into a default dict of the form (URI: boolean)

        Args:
            instances: A dictionary of instances as returned by LMDB or LOD-A-LOT services.
            lookup:

        Returns:

        """
        return cl.defaultdict()

    def __get_conjunction(self, first_col: cl.defaultdict, second_col: cl.defaultdict) -> (set, int):
        """ Compute the conjunctive set of the 2 collections.

        Args:
            first_col: DefaultDict as returned by self.load_instances.
            second_col: DefaultDict as returned by self.load_instances.

        Returns:
            The conjunctive set and its cardinality.
        """

        return set(), len(set())

    def __get_disjunction(self, first_col: cl.defaultdict, second_col: cl.defaultdict) -> (set, int):
        """ Compute the disjunctive set of the 2 collections.

            Args:
                first_col: DefaultDict as returned by self.load_instances.
                second_col: DefaultDict as returned by self.load_instances.

            Returns:
                The disjunctive set and its cardinality.
            """

        return set(), 0

    def get_similarity(self, sim_type: str) -> float:
        """ Compute the similarity of 2 classes.
        Args:
            sim_type: The type of similarity to compute.
        Returns:
            The Jaccard similarity between 2 measures.
        """
        return 0.5
