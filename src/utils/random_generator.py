import random
import string

def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{random_string}@example.com"

def generate_random_name():
    return ''.join(random.choices(string.ascii_letters, k=5)).capitalize()

def get_random_gender():
    return random.choice(["male", "female"])

def get_random_status():
    return random.choice(["active", "inactive"])
