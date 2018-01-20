# ORT Neo4J API

Restful API for serve NEO4J query proxy for avoid Neo4J and Cypher Knowledge

## Requirements

- Python 3.4+
- Python 3 PIP:
    - flask
    - neo4j-driver
    
## Deployment instructions

- Create a config.py file with your neo4J credentials
- run the following command
 ```shell
python3 api.py   
```

The RESTfull API Will be able in http://YOUR_IP_ADDRESS:3000/