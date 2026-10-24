# Screenshot checklist and demo script

## Screenshots to take (Windows: Win + Shift + S)
1. **Route listing** - run the program, choose 1, answer `n` and `n`. Capture the full route table.
2. **Successful booking** - choose 3: `Ahmed`, `24`, `R101`, `2`. Capture "Booking confirmed!" with Booking ID B1001 and Total fare Rs. 2400.
3. **Seat update** - choose 6, answer `n`. Capture R101 showing 38/40 and Partially Booked.
4. **Cancellation** - choose 5, enter `B1001`. Capture "Seats restored: 2".
5. **Report** - choose 7. Capture the report (1 created, 0 confirmed, 1 cancelled, Rs. 0).
6. **Error handling (bonus)** - try 0 seats or a blank name and capture the rejection message.
7. **Records after cancellation (bonus)** - choose 4 and capture the Cancelled record still listed.

For a richer report screenshot: book R101 x2 and R102 x3, cancel the R101 booking, then choose 7 (Confirmed bookings 1, Seats 3, Revenue Rs. 6,000).

## 3-minute demo script
1. **Start (20s):** "This is a console bus booking system in plain Python. Data lives in memory only, so it resets when I close it."
2. **Routes and search (30s):** Option 1 shows five routes held in a **list of dictionaries**. Option 2: search `hyderabad` (3 matches) and `Atlantis` (no match).
3. **Booking (45s):** Option 3 with Ahmed, 24, R101, 2 seats. Explain validation happens first, fare = price x seats = Rs. 2400, a **set** prevents duplicate booking IDs, and seats drop only after all checks pass. Show a rejected 0-seat booking.
4. **Cancellation (30s):** Option 5 with B1001: seats come back once, the record stays as Cancelled. Try it again to show the rejection.
5. **Report (30s):** Option 7. Explain nested loops (routes outside, confirmed bookings inside) and that cancelled fares are excluded from revenue.
6. **Wrap-up (15s):** Show the schedule (option 1, answer `y` to the schedule question), type `abc` at the menu to show it doesn't crash, then choose 8.

## Where each Python concept appears
`while` + `break` + `continue` (main menu) · `enumerate` (route table, bookings list) · `for-else` (route search, cancellation) · nested `for` (schedule, report) · tuple (cities) · set (booking IDs) · list/dict (routes, bookings).
