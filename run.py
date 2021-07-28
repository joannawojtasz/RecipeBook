import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    new_recipe = recipe_input()
    new_recipe.recipe_print()

def recipe_input():
    """
    Collects recipe input from the user
    """
    print('You choose to add a recipe.')
    print("Let's start with the title\n")
    title = input('Enter your recipes title\n')
    print('What kind of recipe is it?')
    kind = input('Choose recipes type: cake\salad\dinner\n')
    portions = input('How many portions is this recipe for\n')
    print(f'Lets prepare ingredients list for {title}')
    add_ingredients = True
    ingredients = []
    while add_ingredients:
        ingredient = input('Enter ingredient name\n')
        amount = input('Enter the amount\n')
        unit = input('Enter unit: g, ml, cup, pinch, click enter if not applicable\n')
        ingredients.append([ingredient, amount, unit])
        if input("do you want to add another ingredient? Choose Y/N\n").lower() == 'n':
            add_ingredients = False
    print('Great! What should we do with this ingredients?')
    to_do = input('Please enter the recipe.\n')
    return  recipe(kind, portions, title, ingredients, to_do)
    

class recipe:
    """
    Recipe class
    """
    def __init__ (self, kind, portions, title, ingredients, to_do):
        self.kind = kind
        self.portions = portions
        self.title = title
        self.ingredients = ingredients
        self.to_do = to_do

    def recipe_print(self):
        """
        print new recipe to the terminal
        """
        print(f'\nYour recipe for {self.portions} portions of {self.kind}:\n')
        print(f'{self.title}\n ------------------------')
        for i in range(0, len(self.ingredients)):
            print(f'{self.ingredients[i][1]}{self.ingredients[i][2]} {self.ingredients[i][0]}')
        print(f'\n {self.to_do}')

def validate_recipe():
    """
    """


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