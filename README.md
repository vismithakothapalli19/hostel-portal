# Hostel Portal - Fixed Django Project

## Setup

1. Create/activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Apply migrations:
   python manage.py migrate

4. Create an admin/login user:
   python manage.py createsuperuser

5. Start the server:
   python manage.py runserver

6. Open:
   http://127.0.0.1:8000/login/

## Main fixes
- Added missing manage.py.
- Added missing student CRUD views.
- Fixed edit/delete URL patterns.
- Added authentication backend configuration.
- Protected dashboard and CRUD pages with login_required.
- Fixed duplicate mobile-number markup.
- Added edit/delete actions to the dashboard.
- Added requirements.txt.


## FT-IV analytics dashboard

- Open **View Analytics** from the hostel dashboard, or visit `/analytics/`.
- The main hostel charts are calculated from the live SQLite database:
  - Categorical: room-status bar chart and student-allocation doughnut chart.
  - Numerical: room-utilisation distribution histogram.
- The optional `Occupancy_Estimation.csv` sensor charts are labelled as a separate demonstration dataset. They are not treated as hostel student or room records.
- Charts use Chart.js from its CDN, so an internet connection is required for chart rendering.
