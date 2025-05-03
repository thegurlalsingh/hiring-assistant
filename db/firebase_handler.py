# db/firebase_handler.py

import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Direct path to the service account key (adjust this to your actual location)
cred = credentials.Certificate("/Users/singhgurlal/Desktop/assignment test/db/streamlit-e3d2a-firebase-adminsdk-fbsvc-806c19598b.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred)

# Get Firestore DB reference
db = firestore.client()

def save_candidate_data(data):
    return db.collection("candidates").add(data)

def get_all_candidates():
    docs = db.collection("candidates").stream()
    return [doc.to_dict() for doc in docs]
