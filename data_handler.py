# data_handler.py

from classes import User, Inventory

def load_users(filename):
    users = {}
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                user = User.from_line(line)
                users[user.username] = user
    except FileNotFoundError:
        pass  # No users file exists yet
    return users

def save_users(filename, users):
    with open(filename, 'w') as f:
        for user in users.values():
            f.write(user.to_line() + '\n')

def load_inventory(filename):
    inventory = Inventory()
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            inventory.load_from_lines(lines)
    except FileNotFoundError:
        pass  # No inventory file exists yet
    return inventory

def save_inventory(filename, inventory):
    with open(filename, 'w') as f:
        for line in inventory.to_lines():
            f.write(line + '\n')
