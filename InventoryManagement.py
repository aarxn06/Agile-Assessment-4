import threading


class InventoryManagement:
    def __init__(self):
        self.warehouses = {
            "Warehouse A": {},
            "Warehouse B": {},
            "Warehouse C": {}
        }

        self.suppliers = {}
        self.reorder_level = 10
        self.lock = threading.Lock()

    def check_warehouse(self, warehouse):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

    def add_product(self, warehouse, product, quantity):
        self.check_warehouse(warehouse)

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        with self.lock:
            current_quantity = self.warehouses[
                warehouse
            ].get(product, 0)

            self.warehouses[warehouse][product] = (
                current_quantity + quantity
            )

    def remove_product(self, warehouse, product, quantity):
        self.check_warehouse(warehouse)

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        with self.lock:
            if product not in self.warehouses[warehouse]:
                raise ValueError("Invalid product")

            available = self.warehouses[
                warehouse
            ][product]

            if quantity > available:
                raise ValueError(
                    "Insufficient inventory"
                )

            self.warehouses[
                warehouse
            ][product] -= quantity

    def transfer_stock(
        self,
        source,
        destination,
        product,
        quantity
    ):
        self.check_warehouse(source)
        self.check_warehouse(destination)

        if quantity <= 0:
            raise ValueError(
                "Quantity must be positive"
            )

        with self.lock:
            if product not in self.warehouses[source]:
                raise ValueError("Invalid product")

            if self.warehouses[source][product] < quantity:
                raise ValueError(
                    "Insufficient inventory"
                )

            self.warehouses[source][product] -= quantity

            current = self.warehouses[
                destination
            ].get(product, 0)

            self.warehouses[
                destination
            ][product] = current + quantity

    def add_supplier(self, product, supplier_name):
        self.suppliers[product] = supplier_name

    def low_stock_products(self):
        low_stock = []

        for warehouse, products in self.warehouses.items():

            for product, quantity in products.items():

                if quantity <= self.reorder_level:
                    low_stock.append(
                        (warehouse, product, quantity)
                    )

        return low_stock

    def reorder(self, warehouse, product, quantity=50):
        if product not in self.suppliers:
            raise ValueError(
                "No supplier registered"
            )

        self.add_product(
            warehouse,
            product,
            quantity
        )

        return self.suppliers[product]

    def select_warehouse(self, product, quantity):
        suitable = []

        for warehouse, products in self.warehouses.items():

            available = products.get(
                product,
                0
            )

            if available >= quantity:
                suitable.append(
                    (warehouse, available)
                )

        if not suitable:
            return None

        suitable.sort(
            key=lambda item: item[1]
        )

        return suitable[0][0]

    def fulfill_order(self, product, quantity):
        warehouse = self.select_warehouse(
            product,
            quantity
        )

        if warehouse is None:
            raise ValueError(
                "Insufficient inventory"
            )

        self.remove_product(
            warehouse,
            product,
            quantity
        )

        return warehouse


if __name__ == "__main__":
    inventory = InventoryManagement()

    inventory.add_product(
        "Warehouse A",
        "Laptop",
        50
    )

    inventory.add_product(
        "Warehouse B",
        "Laptop",
        20
    )

    selected = inventory.fulfill_order(
        "Laptop",
        10
    )

    print("Order fulfilled from:", selected)
