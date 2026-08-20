class ICUAllocation:
    def __init__(self, available_beds):
        self.available_beds = available_beds
        self.patient_ids = set()
        self.admitted = []
        self.waiting_list = []

    def validate_patient(self, patient):
        if not 0 <= patient["oxygen"] <= 100:
            raise ValueError(
                "Invalid oxygen level"
            )

        if not 20 <= patient["heart_rate"] <= 250:
            raise ValueError(
                "Invalid heart rate"
            )

        if patient["age"] < 0:
            raise ValueError(
                "Invalid age"
            )

    def calculate_priority(self, patient):
        self.validate_patient(patient)

        score = 0

        if patient["oxygen"] < 90:
            score += 4
        elif patient["oxygen"] <= 94:
            score += 2

        if (
            patient["heart_rate"] < 50
            or
            patient["heart_rate"] > 120
        ):
            score += 2

        systolic = patient["blood_pressure"]

        if systolic < 90 or systolic > 180:
            score += 2

        if (
            patient["temperature"] < 35
            or
            patient["temperature"] > 39
        ):
            score += 2

        if patient["age"] >= 65:
            score += 1

        if patient["medical_conditions"]:
            score += min(
                len(patient["medical_conditions"]),
                2
            )

        if patient.get("emergency", False):
            score += 5

        return score

    def classify(self, score):
        if score >= 8:
            return "CRITICAL"

        if score >= 5:
            return "HIGH"

        if score >= 3:
            return "MEDIUM"

        return "LOW"

    def prepare_patient(self, patient):
        if patient["patient_id"] in self.patient_ids:
            raise ValueError(
                "Duplicate patient ID"
            )

        self.patient_ids.add(
            patient["patient_id"]
        )

        score = self.calculate_priority(
            patient
        )

        patient = patient.copy()

        patient["priority_score"] = score
        patient["priority"] = self.classify(
            score
        )

        return patient

    def allocate_patients(self, patients):
        prepared = []

        for patient in patients:
            prepared.append(
                self.prepare_patient(patient)
            )

        prepared.sort(
            key=lambda patient: (
                patient.get(
                    "emergency",
                    False
                ),
                patient["priority_score"]
            ),
            reverse=True
        )

        for patient in prepared:

            if self.available_beds > 0:
                self.available_beds -= 1
                self.admitted.append(patient)

            else:
                self.waiting_list.append(patient)

        return self.admitted

    def allocate_patient(self, patient):
        patient = self.prepare_patient(
            patient
        )

        if self.available_beds > 0:
            self.available_beds -= 1
            self.admitted.append(patient)

            return "ALLOCATED"

        self.waiting_list.append(patient)

        return "WAITING LIST"


if __name__ == "__main__":
    system = ICUAllocation(1)

    patient = {
        "patient_id": "P101",
        "age": 70,
        "oxygen": 85,
        "heart_rate": 130,
        "blood_pressure": 85,
        "temperature": 39.5,
        "medical_conditions": [
            "Condition A"
        ],
        "emergency": True
    }

    result = system.allocate_patient(
        patient
    )

    print(result)
    print(system.admitted)
