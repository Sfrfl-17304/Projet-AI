# BD/scripts/init_databases.py

from BD.scripts.populate_onet_mongo import main as load_onet
from BD.scripts.populate_mongodb import main as build_app_collections
from BD.scripts.populate_neo4j import populate_neo4j


def main():
    # 1) Load raw O*NET text files into Mongo (onet_* collections)
    load_onet()

    # 2) Build application-level Roles / Skills collections from O*NET
    build_app_collections()

    # 3) Populate Neo4j graph from those Roles / Skills
    populate_neo4j()


if __name__ == "__main__":
    main()
