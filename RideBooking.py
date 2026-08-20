import sys


VEHICLES = {
    "Bike": {
        "base": 30,
        "per_km": 8,
        "capacity": 1
    },

    "Sedan": {
        "base": 50,
        "per_km": 12,
        "capacity": 4
    },

    "SUV": {
        "base": 80,
        "per_km": 16,
        "capacity": 6
    },

    "Premium": {
        "base": 120,
        "per_km": 22,
        "capacity": 4
    }
}


def calculate_booking(
    customer_id,
    pickup,
    drop,
    distance,
    passengers,
    vehicle_type,
    booking_hour,
    driver_available,
    promotional_discount=0
):
    if not customer_id:
        raise ValueError("Invalid customer ID")

    if distance <= 0:
        raise ValueError("Invalid distance")

    if vehicle_type not in VEHICLES:
        raise ValueError("Invalid vehicle type")

    if booking_hour < 0 or booking_hour > 23:
        raise ValueError("Invalid booking time")

    vehicle = VEHICLES[vehicle_type]

    if passengers <= 0:
        raise ValueError(
            "Invalid passenger count"
        )

    if passengers > vehicle["capacity"]:
        raise ValueError(
            "Excessive passengers"
        )

    if not driver_available:
        raise ValueError(
            "Driver unavailable"
        )

    base_fare = vehicle["base"]
    distance_fare = distance * vehicle["per_km"]

    fare = base_fare + distance_fare

    peak_surcharge = 0

    if (
        8 <= booking_hour <= 10
        or
        17 <= booking_hour <= 20
    ):
        peak_surcharge = fare * 0.20

    night_surcharge = 0

    if booking_hour >= 22 or booking_hour < 5:
        night_surcharge = fare * 0.15

    passenger_surcharge = 0

    if passengers > 2:
        passenger_surcharge = (
            passengers - 2
        ) * 20

    fare += (
        peak_surcharge
        + night_surcharge
        + passenger_surcharge
    )

    promotional_discount = max(
        0,
        min(promotional_discount, 30)
    )

    discount_amount = (
        fare
        * promotional_discount
        / 100
    )

    final_fare = fare - discount_amount

    return {
        "customer_id": customer_id,
        "pickup": pickup,
        "drop": drop,
        "vehicle": vehicle_type,
        "base_fare": round(base_fare, 2),
        "distance_fare": round(distance_fare, 2),
        "peak_surcharge": round(
            peak_surcharge,
            2
        ),
        "night_surcharge": round(
            night_surcharge,
            2
        ),
        "passenger_surcharge": round(
            passenger_surcharge,
            2
        ),
        "discount": round(
            discount_amount,
            2
        ),
        "final_fare": round(
            final_fare,
            2
        ),
        "driver": "Driver-001"
    }


def command_line_booking():
    try:
        customer_id = sys.argv[1]
        pickup = sys.argv[2]
        drop = sys.argv[3]

        distance = float(sys.argv[4])
        passengers = int(sys.argv[5])
        vehicle = sys.argv[6]
        hour = int(sys.argv[7])

        driver_available = (
            sys.argv[8].lower()
            == "true"
        )

        discount = float(sys.argv[9])

        result = calculate_booking(
            customer_id,
            pickup,
            drop,
            distance,
            passengers,
            vehicle,
            hour,
            driver_available,
            discount
        )

        print(
            "OK"
            + "|"
            + str(result["final_fare"])
            + "|"
            + result["driver"]
        )

    except Exception as error:
        print(
            "ERROR"
            + "|"
            + str(error)
            + "|"
        )


if __name__ == "__main__":

    if len(sys.argv) == 10:
        command_line_booking()

    else:
        result = calculate_booking(
            "C101",
            "VIT",
            "Katpadi",
            10,
            2,
            "Sedan",
            12,
            True,
            10
        )

        print(result)
