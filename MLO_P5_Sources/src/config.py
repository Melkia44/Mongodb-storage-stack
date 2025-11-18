import os

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

# Chemin vers le CSV dans le conteneur
CSV_PATH = os.getenv("CSV_PATH", "/data/csv/healthcare_dataset.csv")

# Taille des batchs pour l'insert
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))

