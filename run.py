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
    print("Let me know what you want to do!")
    print("Write add, find or browse\n")

    users_choice = input('Enter your choice here: \n')
    print(f"You want to {users_choice} recipe")

def run():
    get_users_choice()


run()
