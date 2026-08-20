from datetime import datetime, timedelta
import threading


class DigitalWallet:
    def __init__(self, account_id, pin, opening_balance=0, daily_limit=50000):
        self.account_id = account_id
        self.pin = str(pin)
        self.balance = opening_balance
        self.daily_limit = daily_limit

        self.daily_spent = 0
        self.failed_pin_attempts = 0

        self.transaction_history = []
        self.transaction_ids = set()
        self.fraud_flags = []

        self.lock = threading.Lock()

    def verify_pin(self, entered_pin):
        if str(entered_pin) == self.pin:
            self.failed_pin_attempts = 0
            return True

        self.failed_pin_attempts += 1

        if self.failed_pin_attempts >= 3:
            self.fraud_flags.append("Multiple failed PIN attempts")

        return False

    def check_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

    def check_duplicate(self, transaction_id):
        if transaction_id in self.transaction_ids:
            raise ValueError("Duplicate transaction")

    def check_fraud(self, amount):
        now = datetime.now()

        recent_transactions = [
            transaction
            for transaction in self.transaction_history
            if now - transaction["time"] <= timedelta(minutes=10)
        ]

        if len(recent_transactions) >= 5:
            if "More than 5 transactions in 10 minutes" not in self.fraud_flags:
                self.fraud_flags.append(
                    "More than 5 transactions in 10 minutes"
                )

        if amount >= 25000:
            if "Large transaction" not in self.fraud_flags:
                self.fraud_flags.append("Large transaction")

        previous_amounts = [
            transaction["amount"]
            for transaction in self.transaction_history
            if transaction["amount"] > 0
        ]

        if len(previous_amounts) >= 3:
            average = sum(previous_amounts) / len(previous_amounts)

            if average > 0 and amount > average * 5:
                if "Unusual transaction amount" not in self.fraud_flags:
                    self.fraud_flags.append("Unusual transaction amount")

    def record_transaction(self, transaction_id, transaction_type, amount):
        self.transaction_ids.add(transaction_id)

        self.transaction_history.append({
            "id": transaction_id,
            "type": transaction_type,
            "amount": amount,
            "time": datetime.now()
        })

        self.check_fraud(amount)

    def deposit(self, amount, transaction_id):
        with self.lock:
            self.check_amount(amount)
            self.check_duplicate(transaction_id)

            self.balance += amount
            self.record_transaction(transaction_id, "Deposit", amount)

            return self.balance

    def withdraw(self, amount, entered_pin, transaction_id):
        with self.lock:
            self.check_amount(amount)
            self.check_duplicate(transaction_id)

            if not self.verify_pin(entered_pin):
                raise ValueError("Incorrect PIN")

            if amount > self.balance:
                raise ValueError("Insufficient balance")

            if self.daily_spent + amount > self.daily_limit:
                raise ValueError("Daily transaction limit exceeded")

            self.balance -= amount
            self.daily_spent += amount

            self.record_transaction(
                transaction_id,
                "Withdrawal",
                amount
            )

            return self.balance

    def transfer(self, receiver, amount, entered_pin, transaction_id):
        with self.lock:
            self.check_amount(amount)
            self.check_duplicate(transaction_id)

            if not self.verify_pin(entered_pin):
                raise ValueError("Incorrect PIN")

            if amount > self.balance:
                raise ValueError("Insufficient balance")

            if self.daily_spent + amount > self.daily_limit:
                raise ValueError("Daily transaction limit exceeded")

            self.balance -= amount
            self.daily_spent += amount
            receiver.balance += amount

            self.record_transaction(
                transaction_id,
                "Transfer",
                amount
            )

            return True

    def check_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history

    def is_suspicious(self):
        return len(self.fraud_flags) > 0


if __name__ == "__main__":
    wallet = DigitalWallet("ACC101", "1234", 10000)

    print("Account created successfully")
    print("Balance:", wallet.check_balance())

    wallet.deposit(2000, "TXN001")
    print("Balance after deposit:", wallet.check_balance())
