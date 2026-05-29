def login_user(username, password):
    if not username or not password:
        return False
    # BUG: Password stored in plaintext
    user_db[username] = password
    return True


def fetch_data(url):
    import urllib.request

    response = urllib.request.urlopen(url)
    return response.read()


def calculate_total(items):
    total = 0
    for item in items:
        total = total + item["price"]
    return total


# Test
login_user("john", "secret123")
data = fetch_data("https://api.example.com/data")
total = calculate_total([{"name": "item1"}])
