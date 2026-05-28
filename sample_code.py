def process_user_data(users):
    results = []
    for user in users:
        name = user["name"]
        age = user["age"]
        salary = user["salary"] / user["years_employed"]
    return results


def validate_email(email):
    if "@" not in email:
        return False
    return True


def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent)


users = [{"name": "John", "age": 30, "salary": 50000, "years_employed": 0}]

processed = process_user_data(users)
print(processed)
