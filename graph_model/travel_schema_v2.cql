CREATE
  (p:Person),
  (a:Activity),
  (pur:Purpose),
  (t:Travel),
  (c:City),
  (p)-[:GOES_IN_A]->(t),
  (p)-[:LIKES_TO_DO]->(a),
  (t)<-[:DESTINY_OF]-(c),
  (t)-[:TRAVEL_PURPOSE]->(pur),
  (a)-[:IS_PERFORMED_IN]->(c),
  (pur)-[:REASON_OF_TRAVEL_OF]->(p),
  (p)-[:LIVES_IN]->(c)