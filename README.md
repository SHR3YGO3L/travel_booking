

# Travel Booking Django App

This is a travel booking application built with Django, allowing users to browse travel options, book tickets, manage bookings, and filter travel options dynamically.

## Features
- User registration and authentication
- Browse and filter travel options by source, destination, date, and type
- Book travel tickets and manage bookings
- Cancel bookings with seat availability update
- Responsive UI with Bootstrap 5

---

## Local Setup Instructions

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.8 or higher installed
- pip package manager
- Git (optional, for cloning the repo)

### 1. Clone the repository

If using Git:

```

git clone https://github.com/your-username/travel_booking.git
cd travel_booking

```

Or download the source ZIP and extract.

### 2. Create and activate a virtual environment

On Windows:

```

python -m venv venv
venv\Scripts\activate

```

On macOS/Linux:

```

python3 -m venv venv
source venv/bin/activate

```

### 3. Install required packages

```

pip install -r requirements.txt

```
Update settings.py database configuration accordingly:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travel_booking_db',
        'USER': 'travel_user',#change
        'PASSWORD': 'your_password',#change 
        'HOST': 'localhost',
        'PORT': '3306',#if docker thenvchange the port or shutdown the local server for port issue
    }
}
```

### 4. Apply migrations

```

python manage.py migrate

```

### 5. Create a superuser (optional, for admin access) for addding touring routes

```

python manage.py createsuperuser

```
### For adding data via csv(routes.csv)[optional]
```
chmod +x routes.sh
./routes.sh

```
### 6. Run the development server

```

python manage.py runserver

```

Open your browser at http://127.0.0.1:8000/ to access the app.

### 7. Available URLs

- `/register/` - User registration
- `/login/` - User login
- `/logout/` - Logout
- `/travel/` - Browse travel options
- `/my-bookings/` - View and manage your bookings

---

## Notes

- 
- Static files are served automatically in development mode.
- Customize settings in `settings.py` as needed.

---








***



