# Easy Event - Event booking web application

**Easy Event** is a mini web application for booking event time slots.  
Users can browse and explore events, view remaining seats, book/cancel slots and save events to favorites.  
The project focuses on UI using Bootstrap and custom CSS and backend logic was implemented by Django, database and authentication.


## Features
- Event list displayed as cards
- Date filtering (Today / This week / Custom range)
- Event details page
- Book an event/slot with seat limits
- Cancel booking
- Authentication 
## Pages 
- Landing page
- Events page with card grid 
- Event detail page with available slots
- Slot booking + cancellation
- Favorites
- Profile page which contains:
  - Favorites list
  - Bookings list
- Authentication:
  - Sign up 
  - Log in / log out


## UI/Design 
User interface is based on Figma-style layouts, implemented with:
- Bootstrap 5
- CSS: 'landing.css', 'events.css', 'auth.css'

## Algorithm of the website:

### 1) Events and slots
- An **Event** is the main object which incude title, description, location, poster
- Each Event contains **Slots**
- Each Slot has:
  - date & time
  - seats limit

### 2) Booking system
- A user can book a slot if seats are available
- Booking is stored as a **Booking** records and user can cancel a booking 

### 3) Favorites
- A user can save events in favorites
- Favorites are stored in **Favorite** table in profile page

