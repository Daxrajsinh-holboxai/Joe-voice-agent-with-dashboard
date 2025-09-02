import json
from datetime import datetime
from google_calendar_functions import get_busy_times, create_new_events
from zoneinfo import ZoneInfo
BOOKING_DB_FILE = 'booking_db.json'

def load_bookings():
    """Load existing bookings from the JSON file."""
    try:
        with open(BOOKING_DB_FILE, 'r') as file:
            data = json.load(file)
            return data.get("bookings", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_bookings(bookings):
    """Save the updated list of bookings to the JSON file."""
    with open(BOOKING_DB_FILE, 'w') as file:
        json.dump({"bookings": bookings}, file, indent=4)
    print("Bookings saved successfully!")

def create_booking(name, age, symptoms, treatment, email, phone, appointment_date, appointment_time):
    """Create a new booking and save it to the file."""
    if not name or not age or not symptoms or not treatment or not email or not phone or not appointment_date or not appointment_time:
        raise ValueError("All fields are required to create a booking.")

    try:
        datetime.strptime(appointment_date, '%Y-%m-%d')
        datetime.strptime(appointment_time, '%I:%M %p')
    except ValueError:
        raise ValueError("Invalid date or time format. Please use 'YYYY-MM-DD' for date and 'HH:MM AM/PM' for time.")

    bookings = load_bookings()

    new_booking = {
        "name": name,
        "age": age,
        "symptoms": symptoms,
        "treatment": treatment,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "contact_email": email
    }

    bookings.append(new_booking)

    save_bookings(bookings)

    return f"Booking for {name} has been created successfully!"

def send_email(email_address):
    return f"Email sent to {email_address} successfully"

def convert_to_iso_format(year, month, day, hour, minute, timezone_str):
    local_dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo(timezone_str))
    
    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
    
    iso_string = utc_dt.isoformat()
    
    return iso_string


def get_current_time():
    denver_tz = ZoneInfo('America/Denver')
    
    now = datetime.now(tz=denver_tz)
    
    return now.isoformat()

    
FUNCTION_MAP = {
    'create_booking' : create_booking,
    'send_email' : send_email,
    'convert_to_iso_format' : convert_to_iso_format,
    'get_current_time' : get_current_time,
    'get_busy_times' : get_busy_times
}


