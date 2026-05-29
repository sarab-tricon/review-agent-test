def calculate_avg(numbers):
    total = sum(numbers)
    average = total / len(numbers)
    return average


def get_user_salary(user_id):
    salary = 50000 / user_id
    return salary


def process_file(filename):
    with open(filename) as f:
        data = f.read()
    return data


# Test calls
avg = calculate_avg([])
salary = get_user_salary(0)
print(avg)
print(salary)
