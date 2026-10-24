"""
Smart Bus Ticket Booking & Reservation System
Saylani Hackathon - Beginner Track (Python 3, console only)

All data lives in memory (lists, dictionaries, a tuple and a set).
When the program closes, every booking is lost - this is by design.
"""

# ---------------------------------------------------------------
# 1. DATA (kept in memory only)
# ---------------------------------------------------------------

# Tuple: the cities the bus company serves (it never changes).
SUPPORTED_CITIES = ("Karachi", "Hyderabad", "Sukkur", "Mirpur Khas", "Lahore")

# List of dictionaries: one dictionary per route.
routes = [
    {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad",
     "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
    {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur",
     "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
    {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas",
     "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
    {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore",
     "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
    {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad",
     "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30},
]

bookings = []               # List of booking dictionaries (cancelled ones stay here too)
issued_booking_ids = set()  # Set: every booking ID already used (prevents duplicates)


# ---------------------------------------------------------------
# 2. SMALL HELPER FUNCTIONS
# ---------------------------------------------------------------

def parse_positive_int(text):
    """Return the text as a whole number greater than zero, or None if it is not valid."""
    text = text.strip()
    if text.isascii() and text.isdigit() and int(text) > 0:
        return int(text)
    return None


def ask_yes_no(question):
    """Ask a yes/no question. Returns True only for 'y' or 'yes'."""
    return input(question + " (y/n): ").strip().lower() in ("y", "yes")


def find_route(route_id):
    """Return the route dictionary with this ID, or None if it does not exist."""
    for route in routes:
        if route["route_id"] == route_id:
            return route
    return None


def get_seat_status(route):
    """Return 'Available', 'Partially Booked' or 'Fully Booked' for a route."""
    if route["available_seats"] == 0:
        return "Fully Booked"
    if route["available_seats"] == route["total_seats"]:
        return "Available"
    return "Partially Booked"


def generate_booking_id():
    """Create a booking ID (B1001, B1002, ...) that is not in the issued set yet."""
    number = 1001
    while True:
        candidate = "B" + str(number)
        if candidate not in issued_booking_ids:
            return candidate
        number += 1


def print_menu():
    print("\nSMART BUS RESERVATION SYSTEM")
    print("=" * 32)
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Exit")
    print("=" * 32)


# ---------------------------------------------------------------
# 3. FEATURES
# ---------------------------------------------------------------

def print_route_table(only_available=False):
    """Print the numbered route table. Optionally skip fully booked routes."""
    print("\nAVAILABLE BUS ROUTES")
    print(f"{'No.':<5}{'Route':<7}{'Journey':<28}{'Depart':<10}{'Fare':<9}{'Seats':<8}Status")
    shown = 0
    for number, route in enumerate(routes, start=1):
        if only_available and route["available_seats"] == 0:
            continue  # skip fully booked routes when the filter is on
        journey = route["departure_city"] + " -> " + route["destination_city"]
        fare = "Rs." + str(route["ticket_price"])
        seats = str(route["available_seats"]) + "/" + str(route["total_seats"])
        print(f"{number:<5}{route['route_id']:<7}{journey:<28}{route['departure_time']:<10}"
              f"{fare:<9}{seats:<8}{get_seat_status(route)}")
        shown += 1
    if shown == 0:
        print("No routes with seats available.")


def view_schedule():
    """Feature 10: nested loops - outer loop over cities, inner loop over routes."""
    print("\nROUTE SCHEDULE BY DEPARTURE CITY")
    for city in SUPPORTED_CITIES:
        print(city)
        has_departures = False
        for route in routes:
            if route["departure_city"] == city:
                print("  " + route["route_id"] + " -> " + route["destination_city"] + " | " + route["departure_time"])
                has_departures = True
        if not has_departures:
            print("  No scheduled departures.")


def view_available_routes():
    only_available = ask_yes_no("Show only routes that still have seats?")
    print_route_table(only_available)
    if ask_yes_no("View the schedule grouped by departure city?"):
        view_schedule()


def print_route_line(route):
    seats_text = "Fully Booked" if route["available_seats"] == 0 else str(route["available_seats"]) + " seats available"
    print(route["route_id"] + " | " + route["departure_city"] + " -> " + route["destination_city"]
          + " | Rs. " + str(route["ticket_price"]) + " | " + seats_text)


def search_route():
    term = input("Search by route ID or city: ").strip().lower()
    if term == "":
        print("Please type a route ID or a city name.")
        return

    # First try an exact route ID match. A unique ID stops the loop with break.
    for route in routes:
        if route["route_id"].lower() == term:
            print_route_line(route)
            break
    else:
        # for-else: no break happened, so no route ID matched. Try city names now.
        matches = 0
        for route in routes:
            if term == route["departure_city"].lower() or term == route["destination_city"].lower():
                print_route_line(route)
                matches += 1
        if matches == 0:
            print("No routes found for '" + term + "'.")


def book_ticket():
    print("\n--- BOOK A TICKET ---")
    # Step 1: collect and validate every field. Nothing is changed until all checks pass.
    name = input("Passenger name: ").strip()
    if name == "":
        print("Booking failed: the passenger name cannot be empty.")
        return

    age = parse_positive_int(input("Passenger age: "))
    if age is None:
        print("Booking failed: age must be a whole number greater than zero.")
        return

    print_route_table()
    route_id = input("Route ID (for example R101): ").strip().upper()
    route = find_route(route_id)
    if route is None:
        print("Booking failed: route '" + route_id + "' does not exist.")
        return

    seats = parse_positive_int(input("Number of seats: "))
    if seats is None:
        print("Booking failed: seats must be a whole number greater than zero.")
        return

    if seats > route["available_seats"]:
        print("Booking failed: only " + str(route["available_seats"]) + " seat(s) available on " + route_id + ".")
        return

    # Step 2: everything is valid, so create the record and update the seats once.
    booking_id = generate_booking_id()
    total_fare = route["ticket_price"] * seats
    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed",
    }
    bookings.append(booking)
    issued_booking_ids.add(booking_id)
    route["available_seats"] -= seats

    print("\nBooking confirmed!")
    print("Booking ID: " + booking_id)
    print("Passenger: " + name)
    print("Route: " + route_id + " (" + route["departure_city"] + " -> " + route["destination_city"] + ")")
    print("Seats booked: " + str(seats))
    print("Fare per seat: Rs. " + str(route["ticket_price"]))
    print("Total fare: Rs. " + str(total_fare))
    print("Status: Confirmed")


def view_bookings():
    print("\nBOOKING RECORDS")
    if len(bookings) == 0:
        print("No bookings found.")
        return
    for number, booking in enumerate(bookings, start=1):
        route = find_route(booking["route_id"])
        journey = route["departure_city"] + " -> " + route["destination_city"]
        print(str(number) + ". " + booking["booking_id"] + " | " + booking["passenger_name"]
              + " (age " + str(booking["passenger_age"]) + ") | " + booking["route_id"] + " " + journey
              + " | Seats: " + str(booking["seats"]) + " | Fare: Rs. " + str(booking["total_fare"])
              + " | " + booking["status"])


def cancel_booking():
    booking_id = input("Enter booking ID to cancel: ").strip().upper()
    for booking in bookings:
        if booking["booking_id"] == booking_id:
            if booking["status"] != "Confirmed":
                print("Booking " + booking_id + " is already cancelled. No seats were changed.")
            else:
                # Change the status and restore the seats together, exactly once.
                route = find_route(booking["route_id"])
                booking["status"] = "Cancelled"
                route["available_seats"] += booking["seats"]
                print("Booking " + booking_id + " has been cancelled.")
                print("Seats restored: " + str(booking["seats"]))
                print("Route " + route["route_id"] + " available seats: " + str(route["available_seats"]))
            break
    else:
        print("Booking ID '" + booking_id + "' was not found. Nothing was changed.")


def view_seat_availability():
    only_available = ask_yes_no("Show only routes with seats remaining?")
    print("\nSEAT AVAILABILITY")
    shown = 0
    for route in routes:
        if only_available and route["available_seats"] == 0:
            continue
        print(route["route_id"] + " | " + route["departure_city"] + " -> " + route["destination_city"]
              + " | " + str(route["available_seats"]) + "/" + str(route["total_seats"])
              + " seats | " + get_seat_status(route))
        shown += 1
    if shown == 0:
        print("No routes with seats available.")


def generate_report():
    # Count every record by status (cancelled records are included in the total).
    confirmed_count = 0
    cancelled_count = 0
    for booking in bookings:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
        else:
            cancelled_count += 1

    # Nested loops: outer loop = routes, inner loop = that route's CONFIRMED bookings.
    seats_reserved = 0
    confirmed_revenue = 0
    route_lines = []
    fully_booked_routes = 0
    for route in routes:
        route_count = 0
        route_seats = 0
        route_revenue = 0
        for booking in bookings:
            if booking["route_id"] == route["route_id"] and booking["status"] == "Confirmed":
                route_count += 1
                route_seats += booking["seats"]
                route_revenue += booking["total_fare"]
        seats_reserved += route_seats
        confirmed_revenue += route_revenue
        if route_count > 0:
            route_lines.append(route["route_id"] + " (" + route["departure_city"] + " -> "
                               + route["destination_city"] + "): " + str(route_count)
                               + " booking(s), " + str(route_seats) + " seat(s), Rs. " + f"{route_revenue:,}")
        if route["available_seats"] == 0:
            fully_booked_routes += 1

    print("\nBOOKING REPORT")
    print("Total bookings created: " + str(len(bookings)))
    print("Confirmed bookings: " + str(confirmed_count))
    print("Cancelled bookings: " + str(cancelled_count))
    print("Seats currently reserved: " + str(seats_reserved))
    print("Confirmed revenue: Rs. " + f"{confirmed_revenue:,}")
    print("Fully booked routes: " + str(fully_booked_routes))
    print("\nConfirmed bookings by route:")
    if len(route_lines) == 0:
        print("  None.")
    for line in route_lines:
        print("  " + line)


# ---------------------------------------------------------------
# 4. MAIN MENU LOOP
# ---------------------------------------------------------------

def main():
    print("Welcome to the Smart Bus Ticket Booking & Reservation System!")
    while True:
        print_menu()
        choice_text = input("Enter your choice: ").strip()
        if not (choice_text.isascii() and choice_text.isdigit()):
            print("Invalid input. Please enter a number from 1 to 8.")
            continue  # show the menu again

        choice = int(choice_text)
        if choice == 1:
            view_available_routes()
        elif choice == 2:
            search_route()
        elif choice == 3:
            book_ticket()
        elif choice == 4:
            view_bookings()
        elif choice == 5:
            cancel_booking()
        elif choice == 6:
            view_seat_availability()
        elif choice == 7:
            generate_report()
        elif choice == 8:
            print("Thank you for using the Smart Bus Reservation System. Goodbye!")
            break  # leave the menu loop
        else:
            print("Unsupported choice. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed. Goodbye!")
