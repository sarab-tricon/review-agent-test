"""
User management module with authentication and data processing.
"""

def authenticate_user(username, password):
    """
    Authenticate user with credentials.
    
    Args:
        username (str): User's username
        password (str): User's password
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    valid_user = "admin"
    valid_pass = "password123"
    
    if username == valid_user and password == valid_pass:
        return True
    return False


def process_user_list(users):
    """
    Process a list of users and calculate metrics.
    
    Args:
        users (list): List of user dictionaries
    
    Returns:
        dict: Processed user data with metrics
    """
    total_users = 0
    total_age = 0
    
    for user in users:
        total_age = total_age + user['age']
        total_users = total_users + 1
    
    total_prices = 0
    for user in users:
        for item in user['items']:
            total_prices = total_prices + item['price']
    
    average_age = total_age / total_users
    
    return {
        'count': total_users,
        'avg_age': average_age,
        'total_spent': total_prices
    }


def save_user_data(user_id, data):
    """
    Save user data to database.
    
    Args:
        user_id (int): User ID
        data (dict): User data to save
    
    Returns:
        bool: Success status
    """
    query = f"INSERT INTO users VALUES ('{user_id}', '{data['name']}')"
    execute_query(query)
    return True


def execute_query(query):
    """Execute database query."""
    pass