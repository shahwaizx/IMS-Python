# classes.py

class Product:
    def __init__(self, product_id, name, category, price, stock_quantity, threshold=10):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.threshold = threshold

    def to_line(self):
        return f"{self.product_id},{self.name},{self.category},{self.price},{self.stock_quantity},{self.threshold}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        return Product(
            product_id=parts[0],
            name=parts[1],
            category=parts[2],
            price=float(parts[3]),
            stock_quantity=int(parts[4]),
            threshold=int(parts[5])
        )

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password  # In production, passwords should be hashed!
        self.role = role

    def to_line(self):
        return f"{self.username},{self.password},{self.role}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split(',')
        return User(
            username=parts[0],
            password=parts[1],
            role=parts[2]
        )

class Inventory:
    def __init__(self):
        self.products = {}  # Key: product_id, Value: Product object

    def add_product(self, product):
        if product.product_id in self.products:
            raise Exception("Product ID already exists.")
        self.products[product.product_id] = product

    def edit_product(self, product_id, **kwargs):
        if product_id not in self.products:
            raise Exception("Product not found.")
        product = self.products[product_id]
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)

    def delete_product(self, product_id):
        if product_id not in self.products:
            raise Exception("Product not found.")
        del self.products[product_id]

    def search_product(self, name=None, category=None):
        results = []
        for product in self.products.values():
            if name and name.lower() in product.name.lower():
                results.append(product)
            elif category and category.lower() == product.category.lower():
                results.append(product)
        return results

    def filter_by_stock(self, low_stock=False):
        results = []
        for product in self.products.values():
            if low_stock and product.stock_quantity <= product.threshold:
                results.append(product)
            elif not low_stock and product.stock_quantity > product.threshold:
                results.append(product)
        return results

    def adjust_stock(self, product_id, quantity):
        if product_id not in self.products:
            raise Exception("Product not found.")
        self.products[product_id].stock_quantity += quantity
        if self.products[product_id].stock_quantity <= self.products[product_id].threshold:
            print(f"Warning: Stock for '{self.products[product_id].name}' is below threshold.")

    def to_lines(self):
        return [product.to_line() for product in self.products.values()]

    def load_from_lines(self, lines):
        for line in lines:
            product = Product.from_line(line)
            self.products[product.product_id] = product
