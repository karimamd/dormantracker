# not working yet
import requests
import json
from datetime import date, timedelta

BASE_URL = 'http://localhost:5000'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

# Create categories
categories = ["Fight", "Fitness", "Learning"]
category_ids = {}

for category_name in categories:
    category_data = {"name": category_name}
    response = requests.post(f"{BASE_URL}/category", json=category_data)
    print(f"Creating category '{category_name}':")
    print_response(response)
    category_ids[category_name] = response.json()['id']

# Create tasks with levels
tasks = [
    {
        "name": "Read 'The Great Gatsby'",
        "category": "Fight",
        "levels": [
            {"level": 1, "description": "Basic", "target_value": 10, "unit": "pages"},
            {"level": 2, "description": "Good", "target_value": 30, "unit": "pages"},
            {"level": 3, "description": "Excellent", "target_value": 50, "unit": "pages"}
        ]
    },
    {
        "name": "Daily Jogging",
        "category": "Fitness",
        "levels": [
            {"level": 1, "description": "Basic", "target_value": 1, "unit": "km"},
            {"level": 2, "description": "Intermediate", "target_value": 3, "unit": "km"},
            {"level": 3, "description": "Advanced", "target_value": 5, "unit": "km"}
        ]
    },
    {
        "name": "Learn Python",
        "category": "Learning",
        "levels": [
            {"level": 1, "description": "Beginner", "target_value": 1, "unit": "hour"},
            {"level": 2, "description": "Intermediate", "target_value": 2, "unit": "hours"},
            {"level": 3, "description": "Advanced", "target_value": 4, "unit": "hours"}
        ]
    }
]

task_ids = {}

for task in tasks:
    task_data = {
        "name": task["name"],
        "category_id": category_ids[task["category"]],
        "levels": task["levels"]
    }
    response = requests.post(f"{BASE_URL}/task", json=task_data)
    print(f"Creating task '{task['name']}':")
    print_response(response)
    task_ids[task["name"]] = response.json()['id']

# Log progress for the past week
today = date.today()
for i in range(7):
    progress_date = today - timedelta(days=i)
    for task_name, task_id in task_ids.items():
        progress_value = (i + 1) * 2  # Simulating increasing progress each day
        progress_data = {
            "task_id": task_id,
            "date": progress_date.isoformat(),
            "value": progress_value
        }
        response = requests.post(f"{BASE_URL}/progress", json=progress_data)
        print(f"Logging progress for '{task_name}' on {progress_date}:")
        print_response(response)

print("Sample data creation completed.")