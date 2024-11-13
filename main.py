# main.py

from classes import User, Inventory, Product
from data_handler import load_users, save_users, load_inventory, save_inventory
import getpass

def main():
    users_file = 'users.txt'
    inventory_file = 'inventory.txt'

    users = load_users(users_file)
    inventory = load_inventory(inventory_file)

    # If no users exist, create a default admin
    if not users:
        print("No users found. Creating default admin user.")
        admin = User('admin', 'admin123', 'Admin')
        users[admin.username] = admin
        save_users(users_file, users)

    # Login or Signup
    user = None
    while not user:
        print("\nWelcome to the Inventory Management System")
        print("1. Login")
        print("2. Signup")
        choice = input("Select an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            if username in users and users[username].password == password:
                user = users[username]
            else:
                print("Invalid username or password. Please try again.")
        elif choice == '2':
            # Signup process for Users
            print("\nUser Signup")
            username = input("Choose a username: ")
            if username in users:
                print("Username already exists. Please choose a different username.")
                continue
            password = getpass.getpass("Choose a password: ")
            confirm_password = getpass.getpass("Confirm password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            new_user = User(username, password, 'User')
            users[new_user.username] = new_user
            save_users(users_file, users)
            print("Signup successful! You can now log in.")
        else:
            print("Invalid option. Please try again.")

    print(f"\nWelcome, {user.username} ({user.role})!")

    while True:
        if user.role == 'Admin':
            print("\nAdmin Menu:")
            print("1. Add Product")
            print("2. Edit Product")
            print("3. Delete Product")
            print("4. View Products")
            print("5. Search Products")
            print("6. Adjust Stock")
            print("7. Logout")
            choice = input("Select an option: ")

            if choice == '1':
                # Add Product
                try:
                    product_id = input("Enter product ID: ")
                    if product_id in inventory.products:
                        raise Exception("Product ID already exists.")
                    name = input("Enter product name: ")
                    category = input("Enter product category: ")
                    price = float(input("Enter product price: "))
                    stock_quantity = int(input("Enter stock quantity: "))
                    threshold = int(input("Enter stock threshold: "))
                    product = Product(product_id, name, category, price, stock_quantity, threshold)
                    inventory.add_product(product)
                    save_inventory(inventory_file, inventory)
                    print("Product added successfully.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == '2':
                # Edit Product
                try:
                    product_id = input("Enter product ID to edit: ")
                    if product_id not in inventory.products:
                        raise Exception("Product not found.")
                    print("Leave fields blank to keep current values.")
                    name = input("Enter new product name: ")
                    category = input("Enter new product category: ")
                    price = input("Enter new product price: ")
                    stock_quantity = input("Enter new stock quantity: ")
                    threshold = input("Enter new stock threshold: ")

                    kwargs = {}
                    if name:
                        kwargs['name'] = name
                    if category:
                        kwargs['category'] = category
                    if price:
                        kwargs['price'] = float(price)
                    if stock_quantity:
                        kwargs['stock_quantity'] = int(stock_quantity)
                    if threshold:
                        kwargs['threshold'] = int(threshold)

                    inventory.edit_product(product_id, **kwargs)
                    save_inventory(inventory_file, inventory)
                    print("Product updated successfully.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == '3':
                # Delete Product
                try:
                    product_id = input("Enter product ID to delete: ")
                    inventory.delete_product(product_id)
                    save_inventory(inventory_file, inventory)
                    print("Product deleted successfully.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == '4':
                # View Products
                print("\nAll Products:")
                for product in inventory.products.values():
                    print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                          f"Price: {product.price}, Stock: {product.stock_quantity}")
            elif choice == '5':
                # Search Products
                name = input("Enter product name to search: ")
                category = input("Enter product category to search: ")
                results = inventory.search_product(name=name, category=category)
                print("\nSearch Results:")
                for product in results:
                    print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                          f"Price: {product.price}, Stock: {product.stock_quantity}")
            elif choice == '6':
                # Adjust Stock
                try:
                    product_id = input("Enter product ID to adjust stock: ")
                    if product_id not in inventory.products:
                        raise Exception("Product not found.")
                    quantity = int(input("Enter quantity to adjust (use negative numbers to reduce stock): "))
                    inventory.adjust_stock(product_id, quantity)
                    save_inventory(inventory_file, inventory)
                    print("Stock adjusted successfully.")
                except Exception as e:
                    print(f"Error: {e}")
            elif choice == '7':
                # Logout
                print("Logging out...")
                main()
                break
            else:
                print("Invalid option. Please try again.")

        elif user.role == 'User':
            print("\nUser Menu:")
            print("1. View Products")
            print("2. Search Products")
            print("3. Logout")
            choice = input("Select an option: ")

            if choice == '1':
                # View Products
                print("\nAll Products:")
                for product in inventory.products.values():
                    print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                          f"Price: {product.price}, Stock: {product.stock_quantity}")
            elif choice == '2':
                # Search Products
                name = input("Enter product name to search: ")
                category = input("Enter product category to search: ")
                results = inventory.search_product(name=name, category=category)
                print("\nSearch Results:")
                for product in results:
                    print(f"ID: {product.product_id}, Name: {product.name}, Category: {product.category}, "
                          f"Price: {product.price}, Stock: {product.stock_quantity}")
            elif choice == '3':
                # Logout
                print("Logging out...")
                main()
                break
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
