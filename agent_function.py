import json
from datetime import datetime
from google_calendar_functions import get_busy_times, create_new_booking
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

def get_phone_number(phone_number):
    return f"Customers Phone Number is {phone_number}"

def create_booking(name, age, symptoms, treatment, email, phone_number, appointment_date, appointment_time):
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

    if phone_number not in bookings:
        bookings[phone_number] = []
    
    booking[phone_number].append(new_booking)

    save_bookings(bookings)

    try:
        date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        time_obj = datetime.strptime(appointment_time, '%I:%M %p').time()

        naive_dt = datetime.combine(date_obj, time_obj)

        start_dt = naive_dt.replace(ZoneInfo("America/Denver"))

        start_time = start_dt.isoformat()

        if new_booking["name"] and new_booking["contact_email"]:
            create_new_booking(new_booking["name"], start_time, new_booking["contact_email"])
        
    except Exception as e:
        return f"Error while processing booking: {e}"    

    return f"Booking for {name} has been created successfully!"

def send_email(email_address):
    return f"Email sent to {email_address} successfully"

def convert_to_iso_format(year, month, day, hour, minute):
    local_dt = datetime(year, month, day, hour, minute, tzinfo=ZoneInfo("America/Denver"))
    
    iso_string = local_dt.isoformat()
    
    return iso_string


def get_current_time():
    denver_tz = ZoneInfo('America/Denver')
    
    now = datetime.now(tz=denver_tz)
    
    return now.isoformat()

    
FUNCTION_MAP = {
    'create_booking': create_booking,
    'send_email': send_email,
    'convert_to_iso_format': convert_to_iso_format,
    'get_current_time': get_current_time,
    'get_busy_times': get_busy_times,
    'get_phone_number': get_phone_number
}

# {
#             "name": "Jane Smith",
#             "age": 45,
#             "symptoms": "Chronic back pain",
#             "treatment": "Lasers",
#             "appointment_date": "2025-08-29",
#             "appointment_time": "2:00 PM",
#             "contact_email": "jane.smith@example.com",
#             "contact_phone": "+1234567891"
# }

