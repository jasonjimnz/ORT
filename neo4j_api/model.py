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
    driver = None
    session = None
    minube_api_key = None
    hotels_combined_affiliate_id = None
    hotels_combined_api_key = None
    hotels_combined_session_id = None

    def __init__(
            self,
            credentials_dict,
            minube_api_key=None,
            hotels_combined_affiliate_id=None,
            hotels_combined_api_key=None,
            hotels_combined_session_id=None
    ):
        self.driver, self.session = get_neo4j_connection(
            credentials_dict['host'],
            credentials_dict['port'],
            credentials_dict['user'],
            credentials_dict['auth']
        )
        if minube_api_key:
            self.minube_api_key = minube_api_key
        if hotels_combined_affiliate_id:
            self.hotels_combined_affiliate_id = hotels_combined_affiliate_id
        if hotels_combined_api_key:
            self.hotels_combined_api_key = hotels_combined_api_key
        if hotels_combined_session_id :
            self.hotels_combined_session_id = hotels_combined_session_id

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
        p = PersonGenerator("", self.get_cities())
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

    def get_similar_travels_based_on_destiny(self, city):
        query = """
        MATCH (c:City)-[:DESTINY_OF]->(t:Travel)<-[:GOES_IN_A]-(p:Person) 
        WHERE c.city_name = "%s" RETURN count(distinct p);
        """ % city

        return self.session.run(query)

    def get_total_travels_based_on_origin_and_destiny(self, origin, destiny):
        query = """
        MATCH p=((c1:City)<-[:LIVES_IN]-(pe:Person)-[:GOES_IN_A]->(t:Travel)<-[:DESTINY_OF]-(c2:City)) 
        WHERE c2.city_name = "%s" 
        AND c1.city_name = "%s" return count(p)
        """ % (destiny, origin)

        return self.session.run(query)

    def get_related_activities_based_in_travel(self, origin, destiny):
        query = """
        MATCH (c1:City)<-[:LIVES_IN]-(pe:Person)-[:GOES_IN_A]->(t:Travel)<-[:DESTINY_OF]-(c2:City)<-[:IS_PERFORMED_IN]-(act:Activity) 
        WHERE c2.city_name = "%s" AND c1.city_name = "%s" 
        RETURN distinct act.activity_name
        """ % (destiny, origin)

        return self.session.run(query)

    def add_spanish_cities_minube(self):
        country_id = 63
        url = "http://papi.minube.com/zones?lang=es&country_id=%s&api_key=%s" % (str(country_id), self.minube_api_key)
        r = requests.get(url)
        zones = r.json()
        for zone in zones:
            zone_id = zone['zone_id']
            url2 = "http://papi.minube.com/cities?lang=es&zone_id=%s&country_id=%s&api_key=%s" % (str(zone_id), str(country_id), self.minube_api_key)
            r2 = requests.get(url2)
            cities = r2.json()
            for city  in cities:
                try:
                    query = "MERGE (c:City{city_name: \"%s\", zone_id: %s, country_id: %s, city_id: %s}) RETURN c;" % (
                        city['city_name'],
                        str(city['zone_id']),
                        str(city['country_id']),
                        str(city['city_id'])
                    )
                    self.session.run(query)
                    url2 = "https://sandbox.hotelscombined.com/api/2.0/hotels?apiKey=%s&affiliateID=%s&sessionID=%s&destination=place:%s&pageSize=100&pageIndex=0" % (
                        str(self.hotels_combined_api_key),
                        str(self.hotels_combined_affiliate_id),
                        str(self.hotels_combined_session_id),
                        city['city_name']
                    )
                    r3 = requests.get(url2)
                    hotels = r3.json()
                    for hotel in hotels['results']:
                        print(hotel)
                        query2 = """
                        MATCH (c:City{city_name: \"%s\", zone_id: %s, country_id: %s, city_id: %s})
                        MERGE (h:HOTEL{name: "%s", link: "%s", hotel_id: %s})
                        MERGE (c)<-[:HOTEL_LOCATED_IN]-(h)
                        RETURN c;
                        """ % (
                            city['city_name'],
                            str(city['zone_id']),
                            str(city['country_id']),
                            str(city['city_id']),
                            hotel['name'],
                            hotel['href'],
                            str(hotel['id'])
                        )
                        print(query2)
                        self.session.run(query2)
                except:
                    print("Failure in iteration")
                print("City %s added and their hotels" % city['city_name'])

    def add_pois_from_cities(self):
        country_id = 63
        url = "http://papi.minube.com/zones?lang=es&country_id=%s&api_key=%s" % (
        str(country_id), self.minube_api_key)
        r = requests.get(url)
        zones = r.json()
        for zone in zones:
            zone_id = zone['zone_id']
            url2 = "http://papi.minube.com/cities?lang=es&zone_id=%s&country_id=%s&api_key=%s" % (
            str(zone_id), str(country_id), self.minube_api_key)
            r2 = requests.get(url2)
            cities = r2.json()
            for city in cities:
                try:
                    query = "MERGE (c:City{city_name: \"%s\", zone_id: %s, country_id: %s, city_id: %s}) RETURN c;" % (
                        city['city_name'],
                        str(city['zone_id']),
                        str(city['country_id']),
                        str(city['city_id'])
                    )
                    self.session.run(query)
                    url2 = "http://papi.minube.com/pois?lang=es&country_id=%s&zone_id=%s&city_id=%s&api_key=%s" % (
                        str(country_id),
                        str(zone_id),
                        str(city['city_id']),
                        self.minube_api_key
                    )
                    r3 = requests.get(url2)
                    pois = r3.json()
                    for po in pois:
                        query2 = """
                            MATCH (c:City{city_name: \"%s\", zone_id: %s, country_id: %s, city_id: %s})
                            MERGE (h:Pois{pois_name: "%s", pois_picture_link: "%s", pois_id: %s})
                            MERGE (c)<-[:POIS_LOCATED_IN]-(h)
                            RETURN c;
                        """ % (
                            city['city_name'],
                            str(city['zone_id']),
                            str(city['country_id']),
                            str(city['city_id']),
                            po['name'],
                            po['picture_url'],
                            str(po['id'])
                        )
                        self.session.run(query2)
                except:
                    print("Failure in iteration")
                print("City %s added and their pois" % city['city_name'])

    def get_cities(self):
        query = "MATCH (c:City) WHERE exists(c.city_id) return c.city_name;"
        records = self.session.run(query)
        cities = [r for r in records.records()]
        city_names = [c[0] for c in cities]
        return city_names

    def get_pois(self, city):
        query = """
        MATCH (p:Pois)-[:POIS_LOCATED_IN]->(c:City) 
        WHERE c.city_name = "%s"
        RETURN p.pois_name, p.pois_picture_link, p.pois_id;
        """ % city
        records = self.session.run(query)
        pois = [r for r in records.records()]
        pois_list = [c.properties.__dict__ for c in pois]
        return pois_list

    def get_all_pois(self):
        query = """
        MATCH (p:Pois) 
        RETURN p.pois_name, p.pois_picture_link, p.pois_id;
        """
        records = self.session.run(query)
        pois = [r for r in records.records()]

        return pois


class ApiManager:
    minube = None
    hotelscombined = None
    bbva = None

    def __init__(self, **kwargs):
        if 'minube_key' in kwargs:
            self.minube = kwargs['minube_key']