import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config import MONGODB_URI, DB_NAME, COLL_NAME
from src.ingest import ingest

from pymongo import MongoClient



def test_ingest_inserts_expected_documents_and_indexes():
    client = mongomock.MongoClient()
    report = ingest(client=client)

    inserted = report["inserted"]
    after_quality = report["after_quality"]

    assert inserted == after_quality["row_count"], (
        f"Incohérence interne : inserted={inserted}, row_count={after_quality['row_count']}"
    )

    coll = client[DB_NAME][COLL_NAME]

    mongo_count = coll.count_documents({})

    assert mongo_count == inserted, (
        f"Incohérence avec Mongo : {mongo_count=} != {inserted=}"
    )


def test_ingest_improves_data_quality():
    client = mongomock.MongoClient()
    report = ingest(client=client)
    before = report["before_quality"]
    after = report["after_quality"]

    assert after["duplicate_rows"] <= before["duplicate_rows"]

    for rule, before_count in before["invalid_rules"].items():
        after_count = after["invalid_rules"][rule]
        assert after_count <= before_count
