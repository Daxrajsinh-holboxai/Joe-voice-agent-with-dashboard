from datetime import datetime, timedelta
import json


with open("membership_db.json", "r") as f:
    membership_data = json.load(f)

with open("session_db.json", "r") as f:
    session_data = json.load(f)

with open("membership_plan.json", "r") as f:
    membership_plan = json.load(f)


def get_user_data(user_id):
    user_list = membership_data['users']
    for user in user_list:
        if user_id == user['user_id']:
            return user
    return "User Not Found"

def get_session_of_user(user_id):
    session_list = session_data['sessions']
    user_session_list = []
    for session in session_list:
        if user_id == session['user_id']:
            user_session_list.append(session)
    return user_session_list

def add_new_user(firstname, lastname, email, contact_number, membership_plan, reason_for_joining):
    new_user_id = f"USR{len(membership_data['users']) + 1:03d}"

    new_user = {
        "user_id": new_user_id,
        "first_name": firstname,
        "last_name": lastname,
        "email": email,
        "contact_number": contact_number,
        "membership_plan": membership_plan,
        "reason_for_joining": reason_for_joining
    }
    
    membership_data["users"].append(new_user)
    
    with open("membership_db.json", "w") as f:
        json.dump(membership_data, f, indent=4)

    return f"New user {firstname} {lastname} successfully registered with user ID {new_user_id}."

def add_new_session(user_id, session_type, session_date, session_time, trainer, trainee, status="Scheduled"):
    new_session_id = f"SES{len(session_data['sessions']) + 1:03d}"

    new_session = {
        "session_id": new_session_id,
        "user_id": user_id,
        "session_date": session_date,
        "session_time": session_time,
        "session_type": session_type,
        "trainer": trainer,
        "trainee": trainee,
        "status": status
    }

    session_data["sessions"].append(new_session)
    
    with open("session_db.json", "w") as f:
        json.dump(session_data, f, indent=4)

    return f"New session scheduled successfully with session ID {new_session_id}."

def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    
    return f"The current time is: {formatted_time}"

def get_categories():
    return list(membership_plan["membership_plans"].keys())

def get_plans_in_category(category):
    if category in membership_plan["membership_plans"]:
        return membership_plan["membership_plans"][category]
    else:
        return f"Category '{category}' not found."

FUNCTION_MAP = {
    'get_user_data': get_user_data,
    'get_session_of_user': get_session_of_user,
    'add_new_user': add_new_user,
    'add_new_session' : add_new_session,
    'get_current_time' :  get_current_time,
    'get_categories' : get_categories,
    'get_plans_in_category' : get_plans_in_category
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

