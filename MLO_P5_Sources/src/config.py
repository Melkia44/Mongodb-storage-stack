import os
from pathlib import Path

# Nom de la base et de la collection
DB_NAME = os.getenv("APP_DB", "MLO_DE_Projet5")
COLL_NAME = os.getenv("COLL_NAME", "admissions")

# URI Mongo : on utilise le service Docker "mongo"
APP_USER = os.getenv("APP_USER")
APP_PWD = os.getenv("APP_PWD")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")

MONGODB_URI = os.getenv(
    "MONGODB_URI",
    f"mongodb://{APP_USER}:{APP_PWD}@{MONGO_HOST}:{MONGO_PORT}/{DB_NAME}?authSource=admin"
)

# Chemin vers le CSV - détection automatique local vs conteneur
_default_container_path = "/data/csv/healthcare_dataset.csv"
default_local_path = str(Path(file_).parent.parent / "Data" / "CSV" / "healthcare_dataset.csv")

# Utilise le chemin conteneur si le fichier existe, sinon le chemin local
if os.path.exists(_default_container_path):
    _default_csv = _default_container_path
elif os.path.exists(_default_local_path):
    _default_csv = _default_local_path
else:
    _default_csv = _default_container_path  # fallback au chemin conteneur

CSV_PATH = os.getenv("CSV_PATH", _default_csv)

# Taille des batchs pour l'insert
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))