# test_db.py
from check import save_candidate_data

test_data = {
    "name": "Test User",
    "email": "test@example.com"
}

save_candidate_data(test_data)
