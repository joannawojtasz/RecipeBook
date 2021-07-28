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

    return input('Enter your choice here: \n')
    


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



def run_users_choice(choice):
    """
    Starts functions according to users choice
    """
    if choice == 'add':            
        add_recipe()
    elif  choice == 'find':
        find_recipe()
    elif  choice == 'browse':
        browse_recipes() 

def add_recipe():
    """
    Creates new recipe
    """
    print('You choose to add a recipe.\n')
    print('Function is not yet implemented')

def find_recipe():
    """
    Finds a recipe within one category
    """
    print('You choose to find a recipe.')

def browse_recipes():
    """
    Displays recipes within one category
    """
    print('You choose to browse recipes.')

# def ():
#     """
#     """
def main():
    """
    Run all program functions
    """
    print("Welcome to Recipe Book!\n")
    choice = get_users_choice()
    verify_users_choice(choice)
    run_users_choice(choice.lower())

main()