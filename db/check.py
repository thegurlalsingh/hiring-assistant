from pymongo import MongoClient

DB_NAME = "talentscout"
COLLECTION_NAME = "candidates"
MONGO_URL = "mongodb+srv://singhgurlal1303:DAC8AxbePZKSgSai@test.9vz1tw8.mongodb.net/?retryWrites=true&w=majority&appName=Test"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def save_candidate_data(data: dict):
    try:
        collection.insert_one(data)
        print("✅ Candidate data saved to MongoDB.")
    except Exception as e:
        print("❌ Failed to save data:", e)
