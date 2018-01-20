from neo4j.v1 import GraphDatabase, basic_auth


def get_neo4j_connection(host, port, user, auth):
    """
    Returns a neo4j driver and a neo4j session with the requested params

    :param host:
        Neo4J Host IP/URL
    :param port:
        Neo4J Bolt Port, default 7687
    :param user:
        Neo4J User, default is neo4j
    :param auth:
        Neo4J Password
    :return:
        Neo4j Driver object
        Neo4j Session object
    """
    driver = GraphDatabase.driver("bolt://%s:%s" % (host, str(port)), auth=basic_auth(user,auth))
    session = driver.session()
    return driver, session

# TODO: Create Nodes
# TODO: Create Relationship

class GraphManager:
    basic_queries = {
        "create": "CREATE (n:%s{%});",
        "get_or_create": "MERGE (n:%s{%s}) RETURN n;"
    }
    driver = None,
    session = None

    def __init__(self, credentials_dict):
        self.driver, self.session = get_neo4j_connection(
            credentials_dict['host'],
            credentials_dict['port'],
            credentials_dict['user'],
            credentials_dict['auth']
        )

    def run_query(self, query):
        return self.session.run(query)