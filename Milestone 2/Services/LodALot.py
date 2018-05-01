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
        return {}

    def count_triples(self, sub: str = None, pred: str = None, obj: str = None) -> int:
        """Count all the triples from LOD-A-LOT that match a specific pattern.

                Args:
                    sub: The subject to match as a URI. If None, will match all subjects.
                    pred: The predicate to match as URI. If None, will match all predicates.
                    obj: The object to match as URI. If None, will match all objects.

                Returns:
                    Number of triples matching patterns
                """

        return 0
