from pymongo import MongoClient, ASCENDING, TEXT
from tqdm import tqdm
from .config import MONGODB_URI, DB_NAME, COLL_NAME, CSV_PATH, BATCH_SIZE
from .transform import load_csv, transform_dataframe, dataframe_to_mongo_docs, quality

def create_indexes(coll):
    coll.create_index([("Hospital", ASCENDING)])
    coll.create_index([("Doctor", ASCENDING)])
    coll.create_index([("Medical Condition", ASCENDING), ("Date of Admission", ASCENDING)])
    coll.create_index([("Date of Admission", ASCENDING)])
    coll.create_index([("Discharge Date", ASCENDING)])
    coll.create_index([("Name", TEXT), ("Medical Condition", TEXT), ("Medication", TEXT)])

def ingest(client: MongoClient | None = None):
    raw = load_csv(CSV_PATH)
    before_quality = quality(raw)
    df = transform_dataframe(raw)
    after_quality = quality(df)
    docs = dataframe_to_mongo_docs(df)
    is_owned_client = client is None
    client = client or MongoClient(MONGODB_URI)
    coll = client[DB_NAME][COLL_NAME]
    coll.delete_many({})
    for i in tqdm(range(0, len(docs), BATCH_SIZE), desc="Insert"):
        coll.insert_many(docs[i:i+BATCH_SIZE], ordered=False)
    create_indexes(coll)
    count = coll.count_documents({})
    assert count == len(docs), f"Inconsistent count: mongo={count}, prepared={len(docs)}"
    if is_owned_client:
        client.close()
    return {"before_quality": before_quality, "after_quality": after_quality, "inserted": count}

if __name__ == "__main__":
    rep = ingest()
    print(rep)
