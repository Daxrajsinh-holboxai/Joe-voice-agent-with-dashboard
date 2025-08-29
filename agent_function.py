import json
from datetime import datetime

# File path for the booking database
BOOKING_DB_FILE = 'booking_db.json'

def load_bookings():
    """Load existing bookings from the JSON file."""
    try:
        with open(BOOKING_DB_FILE, 'r') as file:
            data = json.load(file)
            return data.get("bookings", [])
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # If the file is corrupted or empty, return an empty list

def save_bookings(bookings):
    """Save the updated list of bookings to the JSON file."""
    with open(BOOKING_DB_FILE, 'w') as file:
        json.dump({"bookings": bookings}, file, indent=4)
    print("Bookings saved successfully!")

def create_booking(name, age, symptoms, treatment, email, phone, appointment_date, appointment_time):
    """Create a new booking and save it to the file."""
    # Validate the input data
    if not name or not age or not symptoms or not treatment or not email or not phone or not appointment_date or not appointment_time:
        raise ValueError("All fields are required to create a booking.")

    # Format the booking date and time to ensure it's consistent
    try:
        # Ensure the date is in the correct format (YYYY-MM-DD)
        datetime.strptime(appointment_date, '%Y-%m-%d')
        # Ensure the time is in the correct format (HH:MM AM/PM)
        datetime.strptime(appointment_time, '%I:%M %p')
    except ValueError:
        raise ValueError("Invalid date or time format. Please use 'YYYY-MM-DD' for date and 'HH:MM AM/PM' for time.")

    # Load existing bookings
    bookings = load_bookings()

    # Create the new booking entry
    new_booking = {
        "name": name,
        "age": age,
        "symptoms": symptoms,
        "treatment": treatment,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "contact_email": email
    }

    # Add the new booking to the list
    bookings.append(new_booking)

    # Save the updated bookings to the file
    save_bookings(bookings)

    return f"Booking for {name} has been created successfully!"

# Example usage:
# Uncomment to test the create_booking function
# create_booking('John Doe', 34, 'Knee pain, limited mobility', 'PRP', 'john.doe@example.com', '+1234567890', '2025-08-28', '10:00 AM')
def send_email(email_address):
    return f"Email sent to {email_address} successfully"

FUNCTION_MAP = {
    'create_booking' : create_booking,
    'send_email' : send_email
}


# print(get_user_data("USR001"))
# {
#   "functions": [
    # {
    #   "name": "get_user_data",
    #   "description": "Retrieve the details of a user based on their user ID. Use this function when: A user requests their personal details or when an agent needs to verify a user's information.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "user_id": {
    #         "type": "string",
    #         "description": "The unique ID of the user whose data is being requested."
    #       }
    #     },
    #     "required": ["user_id"]
    #   }
    # },
    # {
    #   "name": "get_session_of_user",
    #   "description": "Get all the sessions associated with a user. Use this function when: A user asks for their session history or when an agent needs to know how many sessions a user has attended.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "user_id": {
    #         "type": "string",
    #         "description": "The unique ID of the user whose sessions are being requested."
    #       }
    #     },
    #     "required": ["user_id"]
    #   }
    # },
    # {
    #   "name": "add_new_user",
    #   "description": "Add a new user to the membership database. Use this function when: A new user wants to register for a membership. This function will require details like the user's name, contact information, and membership plan.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "firstname": {
    #         "type": "string",
    #         "description": "The first name of the new user."
    #       },
    #       "lastname": {
    #         "type": "string",
    #         "description": "The last name of the new user."
    #       },
    #       "email": {
    #         "type": "string",
    #         "description": "The email address of the new user."
    #       },
    #       "contact_number": {
    #         "type": "string",
    #         "description": "The contact number of the new user."
    #       },
    #       "membership_plan": {
    #         "type": "object",
    #         "description": "The membership plan the user selects. This includes plan type, session duration, and pricing details."
    #       },
    #       "reason_for_joining": {
    #         "type": "string",
    #         "description": "The reason the user is joining the membership (e.g., flexibility improvement, pain relief)."
    #       }
    #     },
    #     "required": ["firstname", "lastname", "email", "contact_number", "membership_plan", "reason_for_joining"]
    #   }
    # },
    # {
    #   "name": "add_new_session",
    #   "description": "Add a new session for a user to the session database. Use this function when: A user schedules a new session or when an agent needs to schedule a session for a user.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "user_id": {
    #         "type": "string",
    #         "description": "The unique ID of the user scheduling the session."
    #       },
    #       "session_type": {
    #         "type": "string",
    #         "description": "The type of session the user is booking (e.g., '50-Minute Stretch')."
    #       },
    #       "session_date": {
    #         "type": "string",
    #         "description": "The date of the session in YYYY-MM-DD format."
    #       },
    #       "session_time": {
    #         "type": "string",
    #         "description": "The time of the session in HH:MM AM/PM format."
    #       },
    #       "location": {
    #         "type": "string",
    #         "description": "The location where the session is scheduled to take place."
    #       },
    #       "trainer": {
    #         "type": "string",
    #         "description": "The name of the trainer who will be conducting the session."
    #       },
    #       "status": {
    #         "type": "string",
    #         "description": "The status of the session (e.g., 'Scheduled', 'Completed').",
    #         "default": "Scheduled"
    #       }
    #     },
    #     "required": ["user_id", "session_type", "session_date", "session_time", "location", "trainer"]
    #   }
    # },
    # {
    #   "name": "get_current_time",
    #   "description": "Get the current time in the format HH:MM AM/PM. Use this function when: An agent needs to know the current time or when a user asks about the current time.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {},
    #     "required": []
    #   }
    # },
    # {
    #   "name": "get_categories",
    #   "description": "Get the available categories of membership plans (e.g., '25-Minute Sessions', '50-Minute Sessions'). Use this function when: A user asks about the types of membership plans or when an agent needs to provide options to a user.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {},
    #     "required": []
    #   }
    # },
    # {
    #   "name": "get_plans_in_category",
    #   "description": "Get the details of the plans available in a selected category (e.g., '25-Minute Sessions'). Use this function when: A user selects a category and asks for the available plans or when an agent needs to show the user the specific plans available in a category.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "category": {
    #         "type": "string",
    #         "description": "The category name the user has chosen (e.g., '25-Minute Sessions', '50-Minute Sessions')."
    #       }
    #     },
    #     "required": ["category"]
    #   }
    # }

