class LMDB:
    __file_path: str

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def clean_uris(self) -> dict:
        """Clean all the sameAs URIS. (e.g. unquote, remove bad characters)

        Returns:
            dictionary of cleaned URIS.
        """

        return {}

    def get_instances(self, class_uri: str) -> dict:
        """Get all the instances of a particular LMDB class.

        Args:
            class_uri: The URI of the class for which instances will be retrieved.

        Returns:
            Dictionary of instances.
        """

        return {}

    def count_instances(self, class_uri: str) -> int:
        """Count the instances of a particular LMDB class.

        Args:
            class_uri: The URI of the class for which instances will be retrieved.

        Returns:
            Number of instances in the class.
        """

        return 0
