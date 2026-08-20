import unittest
from ICUAllocation import ICUAllocation


def patient(
    patient_id="P101",
    age=30,
    oxygen=98,
    heart_rate=80,
    blood_pressure=120,
    temperature=37,
    conditions=None,
    emergency=False
):
    return {
        "patient_id": patient_id,
        "age": age,
        "oxygen": oxygen,
        "heart_rate": heart_rate,
        "blood_pressure": blood_pressure,
        "temperature": temperature,
        "medical_conditions": (
            conditions or []
        ),
        "emergency": emergency
    }


class ICUAllocationQA(unittest.TestCase):

    def test_critical_patient(self):
        system = ICUAllocation(1)

        critical = patient(
            oxygen=85,
            heart_rate=140,
            blood_pressure=80
        )

        system.allocate_patient(
            critical
        )

        self.assertEqual(
            system.admitted[0]["priority"],
            "CRITICAL"
        )

    def test_normal_patient(self):
        system = ICUAllocation(1)

        normal = patient()

        system.allocate_patient(
            normal
        )

        self.assertEqual(
            system.admitted[0]["priority"],
            "LOW"
        )

    def test_emergency_case(self):
        system = ICUAllocation(1)

        normal = patient(
            "P1"
        )

        emergency = patient(
            "P2",
            emergency=True
        )

        system.allocate_patients(
            [normal, emergency]
        )

        self.assertEqual(
            system.admitted[0]["patient_id"],
            "P2"
        )

    def test_no_icu_beds(self):
        system = ICUAllocation(0)

        result = system.allocate_patient(
            patient()
        )

        self.assertEqual(
            result,
            "WAITING LIST"
        )

    def test_duplicate_patient(self):
        system = ICUAllocation(2)

        first = patient("P50")

        system.allocate_patient(
            first
        )

        with self.assertRaises(ValueError):
            system.allocate_patient(
                first
            )

    def test_invalid_oxygen(self):
        system = ICUAllocation(1)

        with self.assertRaises(ValueError):
            system.allocate_patient(
                patient(
                    oxygen=120
                )
            )

    def test_invalid_heart_rate(self):
        system = ICUAllocation(1)

        with self.assertRaises(ValueError):
            system.allocate_patient(
                patient(
                    heart_rate=500
                )
            )

    def test_priority_boundary(self):
        system = ICUAllocation(1)

        test_patient = patient(
            oxygen=93,
            heart_rate=130
        )

        score = system.calculate_priority(
            test_patient
        )

        self.assertEqual(
            system.classify(score),
            "MEDIUM"
        )

    def test_multiple_patients_one_bed(self):
        system = ICUAllocation(1)

        low = patient(
            "P1"
        )

        critical = patient(
            "P2",
            oxygen=80,
            heart_rate=140,
            blood_pressure=80
        )

        system.allocate_patients(
            [low, critical]
        )

        self.assertEqual(
            system.admitted[0]["patient_id"],
            "P2"
        )

        self.assertEqual(
            len(system.waiting_list),
            1
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
