from pymongo import MongoClient

from src.config import MONGODB_URI, DB_NAME, COLL_NAME
from src.ingest import ingest


def test_ingest_inserts_expected_documents_and_indexes():
    report = ingest()

    inserted = report["inserted"]
    after_quality = report["after_quality"]

    assert inserted == after_quality["row_count"], (
        f"Incohérence interne : inserted={inserted}, row_count={after_quality['row_count']}"
    )

    client = MongoClient(MONGODB_URI)
    coll = client[DB_NAME][COLL_NAME]
    mongo_count = coll.count_documents({})
    assert mongo_count == inserted, (
        f"Incohérence avec Mongo : {mongo_count=} != {inserted=}"
    )


def test_ingest_improves_data_quality():
    report = ingest()
    before = report["before_quality"]
    after = report["after_quality"]

    assert after["duplicate_rows"] <= before["duplicate_rows"]

    for rule, before_count in before["invalid_rules"].items():
        after_count = after["invalid_rules"][rule]
        assert after_count <= before_count
