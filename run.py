import gspread
from google.oauth2.service_account import Credentials
from datetime import date

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Recipe_Book')
COMMANDS = ['add', 'find', 'browse']

def show_command():
    choice = get_user_choice()
    verify_user_choice(choice)
    run_user_choice(choice.lower())


def get_user_choice():
    """
    Ask user what they want to do
    """
    print("Let me know what you want to do by typing ADD, FIND or BROWSE\n")

    return input('Enter your choice here: \n')


def verify_user_choice(user_choice):
    """
    Verifies if users choice is valid
    """
    try:
        if user_choice.lower() in COMMANDS:
            pass
        else:
            raise ValueError
        
    except ValueError:
        print(f'Invalid input: {user_choice}. Try again!\n')
        show_command()  


def run_user_choice(choice):
    """
    Starts functions according to users choice
    """
    if choice == 'add':            
        add_recipe()
    elif  choice == 'find':
        find_recipe()
    elif  choice == 'browse':
        browse_recipes()  
    show_command()


def add_recipe():
    """
    Creates new recipe
    """
    new_recipe = recipe_input()
    valid_recipe = new_recipe.validate_recipe()
    valid_recipe.recipe_print()
    if save_recipe():
        valid_recipe = valid_recipe.normalise_ingredients_per_portion()
        valid_recipe.save_to_spreadsheet()
    else:
        show_command()


def recipe_input():
    """
    Collects recipe input from the user
    """
    print('\nYou choose to add a recipe. To create new recipe entry you need to enter its the details. Please prepares title, type of a dish, number of portions, ingredients and instructions.\n')
    print("Let's start with the title!\n")
    title = input("Enter your recipe's title\n")
    print('\nWhat kind of recipe is it?')
    kind = input('Choose recipes type: main course/dessert/starter\n')
    portions = input('\nHow many portions is this recipe for\n')
    print(f'\nLets prepare ingredients list for {title}. Add each ingredient name, amount and unit separately.')
    add_ingredients = True
    ingredients = []
    while add_ingredients:
        ingredient = input('\nEnter ingredient name\n')
        amount = input('Enter the amount (use numbers)\n')
        unit = input('Enter unit: g, ml, cup, pinch, click enter if not applicable\n')
        ingredients.append([ingredient, amount, unit])
        if input("do you want to add another ingredient? Choose Y/N\n").lower() == 'n':
            add_ingredients = False
    print('Great! What should we do with this ingredients?\n')
    instructions = input('Please enter the instructions.\n')
    return  Recipe(kind, portions, title, ingredients, instructions)


class Recipe:
    """
    Recipe class
    """
    def __init__ (self, kind, portions, title, ingredients, instructions):
        self.kind = kind
        self.portions = portions
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def recipe_print(self):
        """
        print new recipe to the terminal
        """
        print(f'\nYour recipe for {self.portions} portions of {self.kind}:\n')
        print(f'{self.title}\n ------------------------')
        for i in range(0, len(self.ingredients)):
            print(f'{self.ingredients[i][1]}{self.ingredients[i][2]} {self.ingredients[i][0]}')
        print(f'\n {self.instructions}')

    def prepare_data(self):
        """
        prepare data for saving in spreadshit
        """
        today = date.today().strftime("%Y/%m/%d")
        ingredients = ''
        for ingredient in self.ingredients:
            ingredients += str(ingredient[0]) + ',' + str(ingredient[1]) + ',' + str(ingredient[2])
            ingredients += ';'

        return [self.title, today, ingredients[:-1], self.instructions]
    
    def save_to_spreadsheet(self):
        """
        Saves the recipe to the relevant spreadsheet
        """
        print(f"Saving the recipe for {self.title}...\n")
        data = self.prepare_data()
        SHEET.worksheet(self.kind).append_row(data)
        print("Recipe successfully saved\n")

    def normalise_ingredients_per_portion(self):
        """
        Calculate the amount of ingredients per one portion
        """
        for i in range(0, len(self.ingredients)):
                self.ingredients[i][1] = float(self.ingredients[i][1]) / int(self.portions)
        self.portions = 1
        return self

    def validate_recipe(self):
        """
        Validates recipe kind, portions and amount input fields.
        Allows user to correct the errors.
        """
        try:
            if self.kind.lower() in ['main course', 'dessert', 'starter']:
                pass
            else:
                raise ValueError
        except ValueError:
            print(f'Incorrect type of recipe: {self.kind}.')
            self.kind = input('Choose correct recipe type main course, dessert, starter:\n')
            self.validate_recipe()
        try:
            #Parse to int
            int(self.portions)
        except:
            print(f'Incorrect portion number: {self.portions}.')
            self.portions = input('Enter number of portions:\n')
            self.validate_recipe()
        ingredient_idx = 0
        try:
            # Check if ingredient amount is a decimal
            for i in range(0, len(self.ingredients)):
                ingredient_idx = i
                float(self.ingredients[i][1])
        except ValueError as e:
            print(f'The amount for {self.ingredients[i][0]} (unit: {self.ingredients[i][2]}) is wrong. Please reenter the the amount!\n')
            self.ingredients[ingredient_idx][1] = input(f'Input amount of {self.ingredients[ingredient_idx][0]} (unit: {self.ingredients[ingredient_idx][2]})\n')
            self.validate_recipe()
        return self


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
        print(f'Invalid input: {user_choice}. Answer Y for yes or N for no')
        save_recipe()
    return True


def find_recipe():
    """
    Finds a recipe within one category
    """
    print('You choose to find a recipe.')
    category = input('\nWhat kind of recipe are you looking for? Choose category by typing: main cours, dessert or starter\n')
    valid_category = validate_category(category)
    recipe = input('Enter name of the recipe you are looking for:\n')
    found_recipe = lookfor_recipe(recipe, valid_category)
    portions = input('\nHow many portions do you want to prepare:\n')
    print_found_recipe(valid_category, portions, found_recipe)

def validate_category(category):
    """
    Validate user category selection by user imput
    """
    try:
        if category.lower() in ['main course', 'dessert', 'starter']:
            return category
        else:
            raise ValueError
    except ValueError:
        print(f'Incorrect type of recipe: {category}.')
        category = input('Choose correct recipe type: main course, dessert or starter.\n')
        return validate_category(category)

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
    instructions = data[3]
    
    recept = Recipe(category, portions, title, ingredients_lst, instructions)
    recept.recipe_print()

def browse_recipes():
    """
    Displays recipes within one category
    """
    print('You choose to browse recipes.')
    category = input('\nWhat kind of recipe are you looking for? Choose category by typing: main cours, dessert or starter\n')
    validate_category(category)
    recipes = load_recipes(category)
    print_recipes_list(recipes)
    request = preview_recipes(recipes)


def load_recipes(category):
    """
    Imports data from spreadsheet according to selected category
    """
    print(f'Loading {category} recipes...\n')
    data = SHEET.worksheet(category)
    titles = data.col_values(1)
    return(titles[1:])

def print_recipes_list(recipes):
    """
    Prints list of recipes
    """
    i = 1
    for recipe in recipes:
        print(f'{i}. {recipe}')
        i += 1

def preview_recipes(recipes):
    """
    asks user if they want to preview recipes 
    request list of recipes to preview
    """
    preview = input("Do you want to preview recipes? Answer Y/N")
    try:
        if preview.lower() in ['y', 'yes']:
            recipes_to_preview = get_recipes_to_preview(recipes)
            return recipes_to_preview

        elif preview.lower() in ['n', 'no']:
            pass
        else:
            raise ValueError
    except ValueError:
        print(f'Invalid input: {preview}. Answer Y for yes or N for no')
        preview_recipes()
    
def get_recipes_to_preview(recipes):
    """
    Gets user input for recipes to preview
    in form of numbers
    """
    recipes_request = input('Which recipes do you want to preview? Enter numbers from the list separated by ,. Example: 1,3,5\n')
    request_ints = []
    if validate_request(recipes_request, recipes):
        request_separated = recipes_request.split(",")
        request_ints = [int(value) for value in request_separated]
        return request_ints
        
    else:
        recipes_request = []
        get_recipes_to_preview(recipes)   

def validate_request(recipes_request, recipes):
    """
    Validates if requested recipes are given in right format
    and if they are in range for the number of recipes available
    """
    n = len(recipes)
    try:
        values = recipes_request.split(",")
        for value in values:
            if int(value) <= n:
                pass
            else:
                raise ValueError
        return True
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

def main():
    """
    Run all program functions
    """
    print(
        """
        
██████╗░███████╗░█████╗░██╗██████╗░███████╗  ██████╗░░█████╗░░█████╗░██╗░░██╗
██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝
██████╔╝█████╗░░██║░░╚═╝██║██████╔╝█████╗░░  ██████╦╝██║░░██║██║░░██║█████═╝░
██╔══██╗██╔══╝░░██║░░██╗██║██╔═══╝░██╔══╝░░  ██╔══██╗██║░░██║██║░░██║██╔═██╗░
██║░░██║███████╗╚█████╔╝██║██║░░░░░███████╗  ██████╦╝╚█████╔╝╚█████╔╝██║░╚██╗
╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝╚═╝░░░░░╚══════╝  ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝
        """
    )
    print(
        """
                          ( \ 
                           \ \ 
                     __     \ \___,.-------..__       __
                    //\\ _,-' \ \              `'--._ //\\
                    \\ ;'      \ \                   `: //
                    `(          \ \                   )'
                     :.          \ \,----,         ,;
                      `.`--.___   (    /  ___.--','
                        `.     ``-----'-''     ,'
                            -.               ,-
                               `-._______.-
                            """
    )
    show_command()

main()