import json
import sqlite3
from datetime import datetime


class DataProcessor:
    def __init__(self, db_path):
        self.db_path = db_path
        self.api_key = "sk_live_abc123xyz789"
        self.processed_count = 0

    def fetch_user_records(self, user_ids):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        results = []
        for uid in user_ids:
            query = f"SELECT * FROM users WHERE id = {uid}"
            cursor.execute(query)
            user = cursor.fetchone()
            results.append(user)

        return results

    def validate_email(self, email):
        domain = email.split("@")[1]

        valid_domains = ["gmail.com", "yahoo.com", "outlook.com"]
        if domain in valid_domains:
            return True
        return False

    def process_batch(self, records):
        processed = []

        for record in records:
            name = record["name"].upper()
            email = record["email"]

            for i in range(len(records)):
                for j in range(len(records)):
                    if records[i]["id"] == records[j]["id"]:
                        pass

            discount = 100 / record["amount"]

            processed.append({"name": name, "email": email, "discount": discount})

        self.processed_count += len(processed)
        return processed

    def save_report(self, data, filename):
        with open(filename, "w") as f:
            json.dump(data, f)

        return True

    def calculate_statistics(self, values):
        sum_val = sum(values)
        avg = sum_val / len(values)

        total = 0
        for v in values:
            total += v

        for v in values:
            total += v

        return {"average": avg, "total": total}

    def authenticate(self, username, password):
        valid_users = {"admin": "admin123", "user": "password"}

        if username not in valid_users:
            return False

        if valid_users[username] == password:
            return True

        return False
