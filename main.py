
import csv
import os


# Function to validate one cab booking
def validate_ride(ride):

    errors = []

    if not ride["customer_name"]:
        errors.append("Customer name is missing")

    if not ride["pickup"]:
        errors.append("Pickup location is missing")

    if not ride["drop"]:
        errors.append("Drop location is missing")

    if not ride["ride_id"]:
        errors.append("Ride ID is missing")

    # Validate fare
    try:
        fare = float(ride["fare"])

        if fare <= 0:
            errors.append("Fare must be greater than zero")

    except ValueError:
        errors.append("Fare must be a number")

    # Validate status
    if ride["status"].lower() not in ["completed", "cancelled"]:
        errors.append("Invalid ride status")

    return errors


# Main processing function
def process_rides():

    valid_rides = []
    invalid_rides = []

    try:
        with open(
            "data/rides.csv",
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("CSV file is empty!")
                return

            reader.fieldnames = [
                name.strip() if name else ""
                for name in reader.fieldnames
            ]

            required_columns = [
                "ride_id", "customer_name",
                "pickup", "drop", "fare", "status"
            ]

            if not all(
                col in reader.fieldnames
                for col in required_columns
            ):
                print("Incorrect CSV column names!")
                return

            # Read and validate records
            for ride in reader:

                ride = {
                    key: (value or "").strip()
                    for key, value in ride.items()
                    if key is not None
                }

                if not any(ride.values()):
                    continue

                errors = validate_ride(ride)

                if errors:
                    invalid_rides.append((ride, errors))
                else:
                    valid_rides.append(ride)

        # Display valid records
        print("\nVALID RECORDS")
        print("----------------")

        for ride in valid_rides:
            print(ride)

        # Display invalid records
        print("\nINVALID RECORDS")
        print("----------------")

        for ride, errors in invalid_rides:
            print("Ride ID:", ride["ride_id"])

            for error in errors:
                print("Error:", error)

        # Validation summary
        print("\nVALIDATION SUMMARY")
        print("----------------")
        print("Total valid records:", len(valid_rides))
        print("Total invalid records:", len(invalid_rides))

        # Separate completed and cancelled rides
        completed_rides = [
            ride for ride in valid_rides
            if ride["status"].lower() == "completed"
        ]

        cancelled_rides = [
            ride for ride in valid_rides
            if ride["status"].lower() == "cancelled"
        ]

        # Calculate revenue
        total_revenue = sum(
            float(ride["fare"])
            for ride in completed_rides
        )

        if completed_rides:
            average_fare = total_revenue / len(completed_rides)
        else:
            average_fare = 0

        # Revenue report
        print("\nCAB BOOKING REVENUE REPORT")
        print("--------------------------")
        print("Total rides:", len(valid_rides))
        print("Completed rides:", len(completed_rides))
        print("Cancelled rides:", len(cancelled_rides))
        print("Total revenue: Rs.", total_revenue)
        print("Average fare: Rs.", round(average_fare, 2))

        # Customer summary
        print("\nCUSTOMER BOOKING SUMMARY")
        print("------------------------")

        for ride in completed_rides:
            print(ride["customer_name"], "- Rs.", ride["fare"])

        # Final report
        print("\n========== FINAL REPORT ==========")
        print("Total Bookings:", len(valid_rides))
        print("Successful Bookings:", len(completed_rides))
        print("Cancelled Bookings:", len(cancelled_rides))
        print("Invalid Records:", len(invalid_rides))
        print("Revenue: Rs.", total_revenue)
        print("Average Fare: Rs.", round(average_fare, 2))
        print("==================================")

        # Create output folder
        os.makedirs("output", exist_ok=True)

        # Export valid records to CSV
        with open(
            "output/processed_rides.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=required_columns
            )

            writer.writeheader()
            writer.writerows(valid_rides)

        print("\nProcessed data exported successfully!")

        # Generate summary text report
        with open(
            "output/summary.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write("CAB BOOKING SUMMARY REPORT\n")
            file.write("==========================\n\n")

            file.write(f"Total Bookings: {len(valid_rides)}\n")
            file.write(f"Completed Bookings: {len(completed_rides)}\n")
            file.write(f"Cancelled Bookings: {len(cancelled_rides)}\n")
            file.write(f"Invalid Records: {len(invalid_rides)}\n")
            file.write(f"Total Revenue: Rs. {total_revenue}\n")
            file.write(f"Average Fare: Rs. {round(average_fare, 2)}\n")

        print("Summary report generated successfully!")

    except FileNotFoundError:
        print("Error: CSV file not found!")


# Main program
if __name__ == "__main__":
    process_rides()
