import hashlib
import random

def hash_password(password: str) -> list:
    # List of hashing algorithms
    algorithms = [hashlib.sha256, hashlib.sha512, hashlib.md5]
    
    # Randomly select one algorithm
    chosen_algorithm = random.choice(algorithms)
    
    # Create a hash object using the chosen algorithm
    hash_object = chosen_algorithm()
    
    # Update the hash object with the bytes of the password
    hash_object.update(password.encode('utf-8'))
    
    # Prepare the result as a list
    result = [hash_object.hexdigest(), password, chosen_algorithm.__name__]
    
    return result

# Example usage
if __name__ == "__main__":
    password = "my_secure_password"
    hashed_info = hash_password(password)
    print(f"Hashed Password: {hashed_info[0]}\nOriginal Password: {hashed_info[1]}\nHashing Algorithm: {hashed_info[2]}")
