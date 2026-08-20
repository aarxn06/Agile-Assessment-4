import unittest
from InsuranceClaim import InsuranceClaim


class InsuranceClaimQA(unittest.TestCase):

    def setUp(self):
        self.system = InsuranceClaim()

    def test_valid_claim(self):
        result = self.system.process_claim(
            "POL1001",
            "C101",
            "Health",
            100000,
            "2026-01-01",
            "2026-05-10",
            0,
            30,
            "Hospitalization",
            True
        )

        self.assertEqual(
            result["status"],
            "APPROVED"
        )

    def test_expired_policy(self):
        result = self.system.process_claim(
            "POL1002",
            "C102",
            "Health",
            50000,
            "2024-01-01",
            "2026-01-10",
            0,
            30,
            "Hospitalization",
            True
        )

        self.assertEqual(
            result["status"],
            "REJECTED"
        )

    def test_claim_before_policy_start(self):
        result = self.system.process_claim(
            "POL1003",
            "C103",
            "Vehicle",
            50000,
            "2026-05-01",
            "2026-04-20",
            0,
            25,
            "Accident",
            True
        )

        self.assertEqual(
            result["status"],
            "REJECTED"
        )

    def test_excessive_claim_amount(self):
        result = self.system.process_claim(
            "POL1004",
            "C104",
            "Vehicle",
            500000,
            "2026-01-01",
            "2026-06-01",
            0,
            25,
            "Accident",
            True
        )

        self.assertIn(
            result["status"],
            [
                "MANUAL REVIEW",
                "FRAUD SUSPECTED"
            ]
        )

    def test_missing_documents(self):
        result = self.system.process_claim(
            "POL1005",
            "C105",
            "Health",
            50000,
            "2026-01-01",
            "2026-04-01",
            0,
            30,
            "Hospitalization",
            False
        )

        self.assertEqual(
            result["status"],
            "MANUAL REVIEW"
        )

    def test_multiple_previous_claims(self):
        result = self.system.process_claim(
            "POL1006",
            "C106",
            "Health",
            50000,
            "2026-01-01",
            "2026-04-01",
            5,
            30,
            "Hospitalization",
            True
        )

        self.assertGreaterEqual(
            result["fraud_score"],
            2
        )

    def test_fraud_scenario(self):
        result = self.system.process_claim(
            "POL1007",
            "C107",
            "Vehicle",
            500000,
            "2026-01-01",
            "2026-01-03",
            5,
            25,
            "Accident",
            False
        )

        self.assertEqual(
            result["status"],
            "FRAUD SUSPECTED"
        )

    def test_boundary_claim_amount(self):
        result = self.system.process_claim(
            "POL1008",
            "C108",
            "Vehicle",
            300000,
            "2026-01-01",
            "2026-06-01",
            0,
            25,
            "Accident",
            True
        )

        self.assertEqual(
            result["maximum_payable"],
            300000
        )

    def test_invalid_policy_number(self):
        with self.assertRaises(ValueError):
            self.system.process_claim(
                "1009",
                "C109",
                "Health",
                50000,
                "2026-01-01",
                "2026-06-01",
                0,
                30,
                "Hospitalization",
                True
            )

    def test_invalid_incident_date(self):
        result = self.system.process_claim(
            "POL1010",
            "C110",
            "Health",
            50000,
            "2026-05-01",
            "2026-04-01",
            0,
            30,
            "Hospitalization",
            True
        )

        self.assertEqual(
            result["status"],
            "REJECTED"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
