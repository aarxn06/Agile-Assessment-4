class CourseRegistration:
    def __init__(self):

        self.courses = {
            "DBMS": {
                "credits": 4,
                "prerequisite": "Programming",
                "slot": "A",
                "capacity": 2,
                "minimum_semester": 2
            },

            "AI": {
                "credits": 4,
                "prerequisite": "Data Structures",
                "slot": "B",
                "capacity": 2,
                "minimum_semester": 3
            },

            "ML": {
                "credits": 3,
                "prerequisite": "Statistics",
                "slot": "C",
                "capacity": 2,
                "minimum_semester": 3
            },

            "Cloud": {
                "credits": 3,
                "prerequisite": "Networking",
                "slot": "D",
                "capacity": 2,
                "minimum_semester": 2
            },

            "Testing": {
                "credits": 3,
                "prerequisite": "Programming",
                "slot": "E",
                "capacity": 2,
                "minimum_semester": 2
            }
        }

        self.registrations = {}

    def register(
        self,
        student_id,
        program,
        semester,
        selected_courses,
        completed_courses,
        max_credits=18
    ):
        if len(selected_courses) != len(
            set(selected_courses)
        ):
            raise ValueError(
                "Duplicate course selected"
            )

        already_registered = self.registrations.get(
            student_id,
            []
        )

        for course in selected_courses:

            if course not in self.courses:
                raise ValueError(
                    "Invalid course"
                )

            if course in already_registered:
                raise ValueError(
                    "Duplicate registration"
                )

            course_data = self.courses[
                course
            ]

            prerequisite = course_data[
                "prerequisite"
            ]

            if prerequisite not in completed_courses:
                raise ValueError(
                    f"Missing prerequisite: "
                    f"{prerequisite}"
                )

            if semester < course_data[
                "minimum_semester"
            ]:
                raise ValueError(
                    "Semester restriction"
                )

            if course_data["capacity"] <= 0:
                raise ValueError(
                    "Course is full"
                )

        slots = [
            self.courses[course]["slot"]
            for course in selected_courses
        ]

        if len(slots) != len(set(slots)):
            raise ValueError(
                "Timetable conflict"
            )

        total_credits = sum(
            self.courses[course]["credits"]
            for course in selected_courses
        )

        if total_credits > max_credits:
            raise ValueError(
                "Credit limit exceeded"
            )

        for course in selected_courses:
            self.courses[
                course
            ]["capacity"] -= 1

        self.registrations.setdefault(
            student_id,
            []
        ).extend(selected_courses)

        return {
            "student_id": student_id,
            "program": program,
            "semester": semester,
            "courses": selected_courses,
            "total_credits": total_credits
        }


if __name__ == "__main__":
    system = CourseRegistration()

    result = system.register(
        "S101",
        "Software Engineering",
        3,
        ["DBMS", "AI"],
        [
            "Programming",
            "Data Structures"
        ]
    )

    print(result)
