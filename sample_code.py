def process_user_data(users):
    results = []
    for user in users:
        name = user["name"]
        age = user["age"]
        salary = (
            user["salary"] / user["years_employed"]
        )  # BUG: Division by zero if years_employed is 0
        results.append(name)
    return results


def validate_email(email):
    if "@" not in email:
        return False
    return True


def calculate_discount(price, discount_percent):
    return price * (
        1 - discount_percent
    )  # BUG: No validation for discount_percent > 100


# Test data
users = [
    {
        "name": "John",
        "age": 30,
        "salary": 50000,
        "years_employed": 0,
    },  # BUG: Will cause division by zero
    {"name": "Jane", "age": 25, "salary": 45000, "years_employed": 2},
]

emails = ["john@example.com", "invalid-email", "jane@test.com"]
prices = [100, 200, 150]

processed = process_user_data(users)
print(processed)

for email in emails:
    print(f"{email}: {validate_email(email)}")

discounted = [
    calculate_discount(p, 150) for p in prices
]  # BUG: 150% discount is invalid
print(discounted)
