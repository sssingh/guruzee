import pymongo
from app_config import config


# Generic functions
def get_db_client():
    """Returns MongoDB client object, connect to MongoDB Atlas instance if required"""
    try:
        if config.mongo_client == None:
            client = pymongo.MongoClient(config.MONGO_CONN_STR)
            config.mongo_client = client
    except Exception as e:
        print(e)
    return config.mongo_client


def fetch_document(client, db, collection):
    """Get a single document from the provided db and collection"""
    try:
        document = client[db][collection].find_one()
    except Exception as e:
        print(e)
    return document


def update_document(client, db, collection, key, value):
    """Update the passed key in the document for provided db and collection"""
    try:
        document = fetch_document(client, db, collection)
        client[db][collection].update_one(
            {"_id": document["_id"]},
            {"$set": {key: value}},
        )
    except Exception as e:
        print(e)


# Use case specific functions
def fetch_curr_access_count():
    client = get_db_client()
    curr_count = fetch_document(
        client=client, db=config.db, collection=config.collection
    )[config.key]
    config.openai_curr_access_count = curr_count


def increment_curr_access_count():
    client = get_db_client()
    updated_count = config.openai_curr_access_count + 1
    update_document(
        client=client,
        db=config.db,
        collection=config.collection,
        key=config.key,
        value=updated_count,
    )
    config.openai_curr_access_count = updated_count
