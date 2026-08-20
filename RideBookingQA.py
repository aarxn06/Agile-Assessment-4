import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RideBookingQA {

    static int passed = 0;
    static int failed = 0;

    public static String runBooking(
            String customer,
            String pickup,
            String drop,
            String distance,
            String passengers,
            String vehicle,
            String hour,
            String driver,
            String discount) {

        try {
            ProcessBuilder processBuilder =
                    new ProcessBuilder(
                            "python",
                            "RideBooking.py",
                            customer,
                            pickup,
                            drop,
                            distance,
                            passengers,
                            vehicle,
                            hour,
                            driver,
                            discount
                    );

            Process process = processBuilder.start();

            BufferedReader reader =
                    new BufferedReader(
                            new InputStreamReader(
                                    process.getInputStream()
                            )
                    );

            String output = reader.readLine();

            process.waitFor();

            return output;

        } catch (Exception error) {
            return "ERROR|" + error.getMessage();
        }
    }

    public static void check(
            String testName,
            boolean condition) {

        if (condition) {
            System.out.println(
                    "PASS: " + testName
            );

            passed++;
        } else {
            System.out.println(
                    "FAIL: " + testName
            );

            failed++;
        }
    }

    public static double getFare(String output) {

        try {
            String[] parts = output.split("\\|");

            return Double.parseDouble(
                    parts[1]
            );

        } catch (Exception error) {
            return -1;
        }
    }

    public static void main(String[] args) {

        String normal =
                runBooking(
                        "C101",
                        "VIT",
                        "Katpadi",
                        "10",
                        "2",
                        "Sedan",
                        "12",
                        "true",
                        "0"
                );

        check(
                "Normal booking",
                normal.startsWith("OK")
        );


        String normalFare =
                runBooking(
                        "C102",
                        "A",
                        "B",
                        "10",
                        "2",
                        "Sedan",
                        "12",
                        "true",
                        "0"
                );

        String peakFare =
                runBooking(
                        "C103",
                        "A",
                        "B",
                        "10",
                        "2",
                        "Sedan",
                        "9",
                        "true",
                        "0"
                );

        check(
                "Peak-hour booking",
                getFare(peakFare)
                        >
                        getFare(normalFare)
        );


        String night =
                runBooking(
                        "C104",
                        "A",
                        "B",
                        "10",
                        "2",
                        "Sedan",
                        "23",
                        "true",
                        "0"
                );

        check(
                "Night booking",
                getFare(night)
                        >
                        getFare(normalFare)
        );


        String invalidDistance =
                runBooking(
                        "C105",
                        "A",
                        "B",
                        "0",
                        "2",
                        "Sedan",
                        "12",
                        "true",
                        "0"
                );

        check(
                "Invalid distance",
                invalidDistance.startsWith(
                        "ERROR"
                )
        );


        String invalidPassengers =
                runBooking(
                        "C106",
                        "A",
                        "B",
                        "10",
                        "10",
                        "Sedan",
                        "12",
                        "true",
                        "0"
                );

        check(
                "Invalid passenger count",
                invalidPassengers.startsWith(
                        "ERROR"
                )
        );


        String unavailable =
                runBooking(
                        "C107",
                        "A",
                        "B",
                        "10",
                        "2",
                        "Sedan",
                        "12",
                        "false",
                        "0"
                );

        check(
                "Unavailable driver",
                unavailable.startsWith(
                        "ERROR"
                )
        );


        String maximumDiscount =
                runBooking(
                        "C108",
                        "A",
                        "B",
                        "10",
                        "2",
                        "Sedan",
                        "12",
                        "true",
                        "100"
                );

        check(
                "Maximum discount",
                maximumDiscount.startsWith(
                        "OK"
                )
        );


        boolean vehiclesPassed = true;

        String[] vehicles = {
                "Bike",
                "Sedan",
                "SUV",
                "Premium"
        };

        for (String vehicle : vehicles) {

            String result =
                    runBooking(
                            "C109",
                            "A",
                            "B",
                            "5",
                            "1",
                            vehicle,
                            "12",
                            "true",
                            "0"
                    );

            if (!result.startsWith("OK")) {
                vehiclesPassed = false;
            }
        }

        check(
                "Multiple vehicle types",
                vehiclesPassed
        );


        String boundary =
                runBooking(
                        "C110",
                        "A",
                        "B",
                        "0.1",
                        "1",
                        "Bike",
                        "12",
                        "true",
                        "0"
                );

        check(
                "Boundary fare values",
                boundary.startsWith("OK")
        );


        String driverAllocation =
                runBooking(
                        "C111",
                        "A",
                        "B",
                        "5",
                        "2",
                        "Sedan",
                        "12",
                        "true",
                        "0"
                );

        check(
                "Driver allocation logic",
                driverAllocation.contains(
                        "Driver-001"
                )
        );


        System.out.println(
                "\nPassed: " + passed
        );

        System.out.println(
                "Failed: " + failed
        );

        if (failed > 0) {
            System.exit(1);
        }
    }
}
