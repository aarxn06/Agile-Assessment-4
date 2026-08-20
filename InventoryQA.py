import unittest
import threading
from InventoryManagement import InventoryManagement


class InventoryQA(unittest.TestCase):

    def setUp(self):
        self.inventory = InventoryManagement()

        self.inventory.add_product(
            "Warehouse A",
            "Laptop",
            50
        )

        self.inventory.add_product(
            "Warehouse B",
            "Laptop",
            30
        )

        self.inventory.add_product(
            "Warehouse C",
            "Mouse",
            5
        )

    def test_stock_availability(self):
        warehouse = self.inventory.select_warehouse(
            "Laptop",
            20
        )

        self.assertIsNotNone(warehouse)

    def test_insufficient_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.fulfill_order(
                "Laptop",
                500
            )

    def test_warehouse_transfer(self):
        self.inventory.transfer_stock(
            "Warehouse A",
            "Warehouse B",
            "Laptop",
            10
        )

        self.assertEqual(
            self.inventory.warehouses[
                "Warehouse B"
            ]["Laptop"],
            40
        )

    def test_concurrent_orders(self):

        def order():
            try:
                self.inventory.fulfill_order(
                    "Laptop",
                    5
                )
            except ValueError:
                pass

        threads = []

        for _ in range(4):
            thread = threading.Thread(
                target=order
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        total = (
            self.inventory.warehouses[
                "Warehouse A"
            ].get("Laptop", 0)
            +
            self.inventory.warehouses[
                "Warehouse B"
            ].get("Laptop", 0)
        )

        self.assertEqual(total, 60)

    def test_reorder_threshold(self):
        result = self.inventory.low_stock_products()

        self.assertTrue(
            any(
                product == "Mouse"
                for _, product, _ in result
            )
        )

    def test_invalid_product(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product(
                "Warehouse A",
                "Phone",
                1
            )

    def test_negative_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product(
                "Warehouse A",
                "Laptop",
                100
            )

    def test_multiple_warehouses(self):
        self.assertEqual(
            len(self.inventory.warehouses),
            3
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
