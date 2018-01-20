from neo4j.v1 import GraphDatabase, basic_auth
from test_model_interface import PersonGenerator
import requests

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

    def build_property_dict(self, **kwargs):
        props = ""
        for k in kwargs:
            if props != "":
                props += ", "
            props += '%s: "%s"' % (k, str(kwargs[k]))
        return props

    def add_travels_to_schema(self, limit=5000):
        p = PersonGenerator()
        for x in range(limit):
            person = p.get_preson_travels()
            per = person["person"]
            home = person["home"]['city']
            q1 = "MERGE (n:Person{%s}) MERGE (c:City{%s}) MERGE (n)-[r:LIVES_IN]->(c) RETURN n,r,c ;"
            q7 = "MERGE (n:Person{%s}) MERGE (c:Activity{%s}) MERGE (n)-[r:LIKES_TO_DO]->(c) RETURN n,r,c ;"
            q5 = "MERGE (n:Activity{%s}) MERGE (c:City{%s}) MERGE (n)-[r:IS_PERFORMED_IN]->(c) RETURN n,r,c ;"
            q6 = "MERGE (n:Purpose{%s}) MERGE (c:Person{%s}) MERGE (n)-[r:REASON_OF_TRAVEL_OF]->(c) RETURN n,r,c ;"
            q4 = "MERGE (n:Travel{%s}) MERGE (c:Purpose{%s}) MERGE (n)-[r:TRAVEL_PURPOSE]->(c) RETURN n,r,c ;"
            q3 = "MERGE (n:City{%s}) MERGE (c:Travel{%s}) MERGE (n)-[r:DESTINY_OF]->(c) RETURN n,r,c ;"
            q2 = "MERGE (n:Person{%s}) MERGE (c:Travel{%s}) MERGE (n)-[r:GOES_IN_A]->(c) RETURN n,r,c ;"
            self.session.run(
                q1 % (
                    self.build_property_dict(name=per['name'], last_name=per['last_name']),
                    self.build_property_dict(city_name=home)
                )
            )
            for travel in person['travels']:
                purpose = p.get_purpose()
                activity = p.get_activity()
                self.session.run(
                    q7 % (
                        self.build_property_dict(name=per['name'], last_name=per['last_name']),
                        self.build_property_dict(activity_name=activity)
                    )
                )
                self.session.run(
                    q6 % (
                        self.build_property_dict(purpose_name=purpose),
                        self.build_property_dict(name=per['name'], last_name=per['last_name'])
                    )
                )
                self.session.run(
                    q5 % (
                        self.build_property_dict(activity_name=activity),
                        self.build_property_dict(city_name=travel['city'])
                    )
                )
                self.session.run(
                    q4 % (
                        self.build_property_dict(
                            travel_date=travel["date"],
                            traveler_name=per['name'],
                            traveler_last_name=per["last_name"]
                        ),
                        self.build_property_dict(purpose_name=purpose)
                    )
                )
                self.session.run(
                    q3 % (
                        self.build_property_dict(city_name=travel["city"]),
                        self.build_property_dict(
                            travel_date=travel["date"],
                            traveler_name=per['name'],
                            traveler_last_name=per["last_name"]
                        )
                    )
                )
                self.session.run(
                    q2 % (
                        self.build_property_dict(name=per['name'], last_name=per['last_name']),
                        self.build_property_dict(
                            travel_date=travel["date"],
                            traveler_name=per['name'],
                            traveler_last_name=per["last_name"]
                        )
                    )
                )
            print("Finished %s of %s" % (str(x+1), str(limit)))


class ApiManager:
    minube = None
    hotelscombined = None
    bbva = None

    def __init__(self, **kwargs):
        if 'minube_key' in kwargs:
            self.minube = kwargs['minube_key']