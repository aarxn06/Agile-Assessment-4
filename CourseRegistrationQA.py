import unittest
from CourseRegistration import CourseRegistration


class CourseRegistrationQA(unittest.TestCase):

    def setUp(self):
        self.system = CourseRegistration()

    def test_valid_registration(self):
        result = self.system.register(
            "S101",
            "Software Engineering",
            3,
            ["DBMS", "AI"],
            [
                "Programming",
                "Data Structures"
            ]
        )

        self.assertEqual(
            result["total_credits"],
            8
        )

    def test_missing_prerequisite(self):
        with self.assertRaises(ValueError):
            self.system.register(
                "S102",
                "Software Engineering",
                3,
                ["AI"],
                []
            )

    def test_credit_limit_violation(self):
        with self.assertRaises(ValueError):
            self.system.register(
                "S103",
                "Software Engineering",
                3,
                ["DBMS", "AI"],
                [
                    "Programming",
                    "Data Structures"
                ],
                max_credits=7
            )

    def test_timetable_conflict(self):
        self.system.courses[
            "AI"
        ]["slot"] = "A"

        with self.assertRaises(ValueError):
            self.system.register(
                "S104",
                "Software Engineering",
                3,
                ["DBMS", "AI"],
                [
                    "Programming",
                    "Data Structures"
                ]
            )

    def test_full_course(self):
        self.system.courses[
            "DBMS"
        ]["capacity"] = 0

        with self.assertRaises(ValueError):
            self.system.register(
                "S105",
                "Software Engineering",
                3,
                ["DBMS"],
                ["Programming"]
            )

    def test_duplicate_registration(self):
        self.system.register(
            "S106",
            "Software Engineering",
            3,
            ["DBMS"],
            ["Programming"]
        )

        with self.assertRaises(ValueError):
            self.system.register(
                "S106",
                "Software Engineering",
                3,
                ["DBMS"],
                ["Programming"]
            )

    def test_invalid_course(self):
        with self.assertRaises(ValueError):
            self.system.register(
                "S107",
                "Software Engineering",
                3,
                ["UnknownCourse"],
                ["Programming"]
            )

    def test_semester_restriction(self):
        with self.assertRaises(ValueError):
            self.system.register(
                "S108",
                "Software Engineering",
                1,
                ["AI"],
                ["Data Structures"]
            )

    def test_boundary_credit_value(self):
        result = self.system.register(
            "S109",
            "Software Engineering",
            3,
            ["DBMS", "AI"],
            [
                "Programming",
                "Data Structures"
            ],
            max_credits=8
        )

        self.assertEqual(
            result["total_credits"],
            8
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
