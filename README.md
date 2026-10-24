# Smart Bus Ticket Booking & Reservation System

A Python 3 console application for a small bus company (Saylani Hackathon, Beginner Track). You use a text menu to view routes, search, book tickets, cancel bookings, check seats, and see a report.

## Requirements
- Python 3.6 or newer (no extra packages, no database, no internet).

## How to run
1. Put `main.py` in a folder, for example `smart-bus-reservation`.
2. Open Command Prompt (or the VS Code terminal) in that folder.
3. Run: `python main.py` (on some computers: `py main.py` or `python3 main.py`).
4. Type a menu number and press Enter. Choose **8** to exit.

## Menu guide
| Option | What it does |
|---|---|
| 1 View Available Routes | Shows all routes with fare, seats and status. Optionally hides full routes, and optionally shows the schedule grouped by departure city. |
| 2 Search for a Route | Search by route ID (e.g. R101) or by city (case-insensitive; matches departure or destination). |
| 3 Book a Ticket | Asks name, age, route ID and seats; validates, then confirms with a booking ID (B1001, B1002, ...) and total fare. |
| 4 View My Bookings | Lists every booking, including cancelled ones. |
| 5 Cancel a Booking | Cancels a Confirmed booking by ID and restores its seats once. |
| 6 View Seat Availability | Shows available/total seats and status (Available, Partially Booked, Fully Booked); optional filter. |
| 7 Generate Booking Report | Totals for bookings, seats reserved, confirmed revenue and fully booked routes. |
| 8 Exit | Ends the program. |

## Sample workflow
1. Choose 3, enter `Ahmed`, `24`, `R101`, `2` → Booking B1001, total Rs. 2400.
2. Choose 6 → R101 now shows 38/40 seats.
3. Choose 5, enter `B1001` → seats restored, R101 back to 40.
4. Choose 7 → 1 booking created, 0 confirmed, 1 cancelled, revenue Rs. 0.

## Rules in short
- Validation happens first; seats change only after every check passes.
- Fare = ticket price × seats. Cancelled fares are not counted as revenue.
- A booking can be cancelled only once; the record stays in history.
- Supported cities (tuple): Karachi, Hyderabad, Sukkur, Mirpur Khas, Lahore.
- Schedule by departure city is inside option 1 so that the main menu keeps the 8 options from the PRD.

## Important limitation
All data is stored **in memory only**. When you close the program, every booking is lost and the routes reset to their starting values.

## Constraints followed
Python built-ins only; `input()`/`print()` interface; no files, database, web or GUI.

## Files
`main.py` (the program) · `test_cases.txt` (12 required tests + extras) · `DEMO_GUIDE.md` (screenshot checklist and demo script)
