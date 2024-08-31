import requests
import json
from datetime import date, timedelta

BASE_URL = 'http://localhost:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

# 1. Create a category
category_data = {
    "name": "Reading"
}
response = requests.post(f"{BASE_URL}/category", json=category_data)
print("Creating category:")
print_response(response)
category_id = response.json()['id']

# 2. Create a task with levels
task_data = {
    "name": "Read Book 'The Great Gatsby'",
    "category_id": category_id,
    "levels": [
        {"level": 1, "description": "Basic", "target_value": 1, "unit": "pages"},
        {"level": 2, "description": "Good", "target_value": 5, "unit": "pages"},
        {"level": 3, "description": "Excellent", "target_value": 10, "unit": "pages"},
        {"level": 4, "description": "Extraordinary", "target_value": 1, "unit": "chapters"}
    ]
}
response = requests.post(f"{BASE_URL}/task", json=task_data)
print("Creating task:")
print_response(response)
task_id = response.json()['id']

# 3. Log progress for a week
today = date.today()
for i in range(7):
    progress_date = today - timedelta(days=i)
    progress_data = {
        "task_id": task_id,
        "date": progress_date.isoformat(),
        "value": (i + 1) * 2  # Simulating increasing progress each day
    }
    response = requests.post(f"{BASE_URL}/progress", json=progress_data)
    print(f"Logging progress for {progress_date}:")
    print_response(response)

# 4. Get the report
response = requests.get(f"{BASE_URL}/report")
print("Getting report:")
print_response(response)