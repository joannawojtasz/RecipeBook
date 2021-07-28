import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS =Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Recipe_Book')

# cakes = SHEET.worksheet('cakes')

def get_users_choice():
    """
    Ask user what they want to do
    """
    print("Let me know what you want to do")
    print("by writing add, find or browse\n")

    choice = input('Enter your choice here: \n')
    verify_users_choice(choice)


def verify_users_choice(users_choice):
    """
    Verifies if users choice is valid
    """
    try:
        if users_choice.lower() in ['add', 'find', 'browse']:
            pass
        else:
            raise ValueError
        
    except ValueError:
        print(f'Invalid input: {users_choice}. Try again!\n')
        get_users_choice()       

def run():
    print("Welcome to Recipe Book!\n")
    get_users_choice()


run()
