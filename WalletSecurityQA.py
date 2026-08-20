import unittest
import threading
from DigitalWallet import DigitalWallet


class WalletSecurityQA(unittest.TestCase):

    def setUp(self):
        self.wallet = DigitalWallet(
            "ACC101",
            "1234",
            10000,
            daily_limit=15000
        )

    def test_normal_transaction(self):
        self.wallet.deposit(1000, "T001")
        self.assertEqual(self.wallet.check_balance(), 11000)

    def test_insufficient_balance(self):
        with self.assertRaises(ValueError):
            self.wallet.withdraw(
                20000,
                "1234",
                "T002"
            )

    def test_daily_limit(self):
        with self.assertRaises(ValueError):
            self.wallet.withdraw(
                16000,
                "1234",
                "T003"
            )

    def test_multiple_failed_pins(self):
        for number in range(3):
            try:
                self.wallet.withdraw(
                    100,
                    "9999",
                    f"FAIL{number}"
                )
            except ValueError:
                pass

        self.assertIn(
            "Multiple failed PIN attempts",
            self.wallet.fraud_flags
        )

    def test_suspicious_transaction(self):
        for number in range(6):
            self.wallet.deposit(
                10,
                f"TX{number}"
            )

        self.assertTrue(self.wallet.is_suspicious())

    def test_duplicate_transaction(self):
        self.wallet.deposit(100, "DUP001")

        with self.assertRaises(ValueError):
            self.wallet.deposit(
                100,
                "DUP001"
            )

    def test_negative_amount(self):
        with self.assertRaises(ValueError):
            self.wallet.deposit(
                -100,
                "NEG001"
            )

    def test_concurrent_transactions(self):

        def add_money(number):
            self.wallet.deposit(
                100,
                f"CON{number}"
            )

        threads = []

        for number in range(5):
            thread = threading.Thread(
                target=add_money,
                args=(number,)
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            self.wallet.check_balance(),
            10500
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
