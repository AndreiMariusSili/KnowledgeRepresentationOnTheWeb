
def lmdb_movies_to_dbpedia_uris():
    return """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX lmdb: <http://data.linkedmdb.org/movie/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?uri WHERE {
          ?sub rdf:type lmdb:film .
          ?sub owl:sameAs ?uri .
          FILTER REGEX(STR(?uri), "http://dbpedia.org/resource/")
        }
    """


def lmdb_actors_to_dbpedia_uris():
    return """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX lmdb: <http://data.linkedmdb.org/movie/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?uri WHERE {
          ?sub rdf:type lmdb:actor .
          ?sub owl:sameAs ?uri .
          FILTER REGEX(STR(?uri), "http://dbpedia.org/resource/")
        }
    """


def dbpedia_uris_to_resources(uri: str, uri_type):
    return """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        CONSTRUCT {{
            ?sub ?pred ?obj
        }} WHERE {{
          ?sub ?pred ?obj . 
          ?sub a dbo:{} .
          FILTER(?sub in {})
        }}
    """.format(uri_type, uri)
