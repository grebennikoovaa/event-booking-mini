# Event Booking Mini

A mini web app for booking events: event list, seats/time slots, registration and cancellation.  
Tech stack: Python + Django + Templates + TailwindCSS + HTMX + SQLite.

---

## Features (MVP)
- Event list displayed as cards
- Date filtering (Today / This week / Custom range)
- Event details page
- Book an event/slot with seat limits
- Cancel booking
- Authentication 
## Pages
- `/events` — event list + date filter (cards, “seats left”)
- `/events/<id>` — event details + slot list + Book/Cancel button
- `/login` — login (if using Django auth)
- `/logout` — logout (if using Django auth)

---

## UI Components
- `EventCard` — event card (title, date, “seats left”, View button)
- `DateFilter` — date filter (Today / This week / Range)
- `SlotList` — list of available time slots (if using slots)
- `BookingButton` — Book/Cancel button with dynamic updates (“seats left”)

---

## Data Model
### Slot-based version (recommended)
- `Event` — event information (title, description, location, dates)
- `Slot` — time slot for an event (event, start_datetime, capacity)
- `Booking` — user booking (slot, user, created_at)

**Seats left** = `Slot.capacity - number_of_bookings`

---

## Development workflow (Team rules)
- Do NOT push directly to `main`
- Work only in feature branches:
  - Backend: `backend/*` (e.g. `backend/models`, `backend/views`)
  - UI: `ui/*` (e.g. `ui/layout`, `ui/pages`, `ui/htmx`)
- Create a Pull Request for every feature
- Require at least 1 approval before merging

---

## Suggested task split (2 people)
**Person A (Backend):**
- Django setup + models + booking logic + routes/views

**Person B (UI/UX):**
- Tailwind design + templates + HTMX interactivity

---

## How to run (local)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
