import gspread
from google.oauth2.service_account import Credentials
from datetime import date

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
    valid_recipe = validate_recipe(new_recipe)
    valid_recipe.recipe_print()
    if save_recipe():
        recipe = calculate_1portion(valid_recipe)
        save_to_spreadshit(recipe)

def recipe_input():
    """
    Collects recipe input from the user
    """
    print('You choose to add a recipe.')
    print("Let's start with the title\n")
    title = input('Enter your recipes title\n')
    print('What kind of recipe is it?')
    kind = input('Choose recipes type: main course/dessert/starter\n')
    portions = input('How many portions is this recipe for\n')
    print(f'Lets prepare ingredients list for {title}')
    add_ingredients = True
    ingredients = []
    while add_ingredients:
        ingredient = input('Enter ingredient name\n')
        amount = input('Enter the amount (use numbers)\n')
        unit = input('Enter unit: g, ml, cup, pinch, click enter if not applicable\n')
        ingredients.append([ingredient, amount, unit])
        if input("do you want to add another ingredient? Choose Y/N\n").lower() == 'n':
            add_ingredients = False
    print('Great! What should we do with this ingredients?\n')
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

    def prepare_data(self):
        """
        prepare data for saving in spreadshit
        """
        today = date.today().strftime("%Y/%m/%d")
        ingredients = ''
        for ingredient in self.ingredients:
            ingredients += str(ingredient[0]) + ',' + str(ingredient[1]) + ',' + str(ingredient[2])
            ingredients += ';'

        return [self.title, today, ingredients[:-1], self.to_do]

def validate_recipe(recipe):
    """
    Validates recipe kind, portions and amount input fields.
    Allows user to correct the errors.
    """
    try: 
        if recipe.kind.lower() in ['main course', 'dessert', 'starter']:
            pass
        else:
            raise ValueError
    except ValueError:
        print(f'Incorrect type of recipe: {recipe.kind}.')
        recipe.kind = input('Choose correct rexipe type main course, dessert, starter:\n')
        validate_recipe(recipe)

    try:
        int(recipe.portions)
    except:
        print(f'Incorrect portion number: {recipe.portions}.')
        recipe.portions = input('Enter number of portions:\n')
        validate_recipe(recipe)
    
    try:
        for i in range(0, len(recipe.ingredients)):
            float(recipe.ingredients[i][1])
    except ValueError as e:
        print("One of the ingredients has wrong amount. Please reenter the the amounts!\n")
        for i in range(0, len(recipe.ingredients)):
            recipe.ingredients[i][1] = input(f'Input amount of {recipe.ingredients[i][0]} (unit: {recipe.ingredients[i][2]})\n')
        validate_recipe(recipe)
    
    return recipe

def save_recipe():
    """
    Asks user to validate recipe
    """
    save = input('Do you want to save the recipe? Answer Y / N\n')
    try:
        if save.lower() in ['y', 'yes']:
            pass
        elif save.lower() in ['n', 'no']:
            print('Please try again!\n')
            add_recipe()
        else:
            raise ValueError
    except ValueError:
        print(f'Invalid input: {users_choice}. Answer Y for yes or N for no')
        save_recipe()
    return True

def calculate_1portion(recipe):
    """
    Calculate the amount of ingredients per one portion
    """
    for i in range(0, len(recipe.ingredients)):
            recipe.ingredients[i][1] = float(recipe.ingredients[i][1]) / int(recipe.portions)
    recipe.portions = 1
    return recipe

def save_to_spreadshit(recipe):
    """
    Saves the recipe to the relevant spreadsheet
    """
    print(f"Saving the recipe for {recipe.title}...\n")
    data = recipe.prepare_data()
    SHEET.worksheet(recipe.kind).append_row(data)
    print("Recipe successfully saved\n")

def find_recipe():
    """
    Finds a recipe within one category
    """
    print('You choose to find a recipe.')
    category = input('What type of recipe are you looking for? Choose category main cours, dessert, starter\n')
    validate_category(category)    
    recipe = input('Enter name of the recipe you are looking for:\n')
    found_recipe = lookfor_recipe(recipe, category)
    portions = input('How many portions do you want to prepare:\n')
    print_found_recipe(category, portions, found_recipe)

def validate_category(category):
    """
    Validate user category selection by user imput
    """
    try: 
        if category.lower() in ['main course', 'dessert', 'starter']:
            pass
        else:
            raise ValueError
    except ValueError:
        print(f'Incorrect type of recipe: {category}.')
        category = input('Choose correct recipe type: main course, dessert or starter.\n')
        validate_category(category)



    # get_data(category)

def lookfor_recipe(recipe, category):
    """
    Imports data from spreadsheet according to selected category
    """
    print(f'Looking for {recipe} in {category}...\n')
    data = SHEET.worksheet(category)
    titles = data.col_values(1)
    try:
        index = titles.index(recipe)
        print('Loading the recipe...')
    except: 
        print(f'There is no recipe for {recipe} in the chosen category')
    return data.row_values(index + 1)
    
def print_found_recipe(category, portions, data):

    ingredients = data[2].split(";")
    ingredients_lst = []
    
    for ingredient in ingredients:
        ingredient = ingredient.split(',')
        ingredients_lst.append(ingredient)
    for ingredient in ingredients_lst:
        ingredient[1] = float(ingredient[1]) * int(portions)
    
    title = data[0]
    to_do = data[3]
    
    recept = recipe(category, portions, title, ingredients_lst, to_do)
    recept.recipe_print()


def browse_recipes():
    """
    Displays recipes within one category
    """
    print('You choose to browse recipes.')

def main():
    """
    Run all program functions
    """
    print("Welcome to Recipe Book!\n")
    choice = get_users_choice()
    verify_users_choice(choice)
    run_users_choice(choice.lower())

main()