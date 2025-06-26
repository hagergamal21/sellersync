import bcrypt
import re

# Function to hash the password
def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password
    return hashed_password

# Function to verify if the entered password matches the stored hashed password
def check_password(stored_hash, entered_password):
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash)


def validate_password(password):
    # Check for minimum length (e.g., 8 characters)
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    
    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return "Password must contain at least one uppercase letter."
    
    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return "Password must contain at least one lowercase letter."
    
    # Check for at least one digit
    if not re.search(r'\d', password):
        return "Password must contain at least one digit."
    
    # Check for at least one special character
    if not re.search(r'[\W_]', password):  # Matches any non-alphanumeric character
        return "Password must contain at least one special character."
    
    return "Password is valid!"  # If all checks pass
