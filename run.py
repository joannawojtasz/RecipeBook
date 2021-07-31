import gspread
from google.oauth2.service_account import Credentials
from datetime import date
from time import sleep

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Recipe_Book')
ADD_COMMAND = 'add'
FIND_COMMAND = 'find'
BROWSE_COMMAND = 'browse'
COMMANDS = [ADD_COMMAND, FIND_COMMAND, BROWSE_COMMAND]
MAIN_COURSE_CATEGORY = 'main course'
DESSERT_CATEGORY = 'dessert'
BREAKFAST_CATEGORY = 'breakfast'
CATEGORIES = [MAIN_COURSE_CATEGORY, DESSERT_CATEGORY, BREAKFAST_CATEGORY]


def show_command():
    """
    show initial commands
    """
    choice = get_user_choice()
    verify_user_choice(choice)
    run_user_choice(choice.lower())


def get_user_choice():
    """
    Ask user what they want to do
    """
    print('\n')
    msg = 'Decide what you want to do by entering ADD, FIND or BROWSE here:\n'
    return input(msg)


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
    if choice == ADD_COMMAND:
        add_recipe()
    elif choice == FIND_COMMAND:
        find_recipe()
    elif choice == BROWSE_COMMAND:
        browse_recipes()
    show_command()


def add_recipe():
    """
    Creates new recipe
    """
    new_recipe = recipe_input()
    valid_recipe = new_recipe.validate_recipe()
    valid_recipe.recipe_print()
    save_recipe(valid_recipe)


def save_recipe(valid_recipe):
    """
    Validate saving recipe with the user
    Call for seving the recipe to spreadsheet or going back
    """
    print('Do you want to save the recipe?')
    if yes_no_choice():
        valid_recipe = valid_recipe.normalise_ingredients_per_portion()
        valid_recipe.save_to_spreadsheet()
    else:
        print('Do you want to try again?')
        if yes_no_choice():
            add_recipe()
        else:
            show_command()


def recipe_input():
    """
    Collects recipe input from the user
    """
    print('\n\n\n\nYou chose to add a recipe!')
    print('..........................\n')
    print('To create new recipe entry you need to enter its the details.',
          'Please prepares title, type of a dish, number of portions,',
          'ingredients and instructions.')
    print("Let's start with the title!\n")
    title = input("Enter your recipe's title\n").lower()
    print('\nWhat kind of recipe is it?')
    kind = input('Choose recipes type: main course/dessert/breakfast\n')
    portions = input('\nHow many portions is this recipe for\n')
    print(f'\nLets prepare ingredients list for {title}. Add each',
          'ingredient name, amount and unit separately.')
    add_ingredients = True
    ingredients = []
    while add_ingredients:
        ingredient = input('\nEnter ingredient name\n')
        amount = input('Enter the amount (use numbers)\n')
        msg = 'Enter unit: g, ml, cup, pinch, click enter if not applicable\n'
        unit = input(msg)
        ingredients.append([ingredient, amount,
                            unit])
        print("Do you want to add another ingredient?")
        if yes_no_choice():
            pass
        else:
            add_ingredients = False
    print('Great! What should we do with this ingredients?\n')
    instructions = input('Please enter the instructions.\n')
    return Recipe(kind, portions, title, ingredients, instructions)


def yes_no_choice():
    """
    Handles Y/N input from the user
    """
    preview = input("\nPlease answer Y/N\n")
    try:
        if preview.lower() in ['y', 'yes']:
            return True
        elif preview.lower() in ['n', 'no']:
            return False
        else:
            raise ValueError
    except ValueError:
        print(f'Invalid input: {preview}. Answer Y for yes or N for no')
        return yes_no_choice()


class Recipe:
    """
    Recipe class
    """
    def __init__(self, kind, portions, title, ingredients, instructions):
        self.kind = kind
        self.portions = portions
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def recipe_print(self):
        """
        print new recipe to the terminal
        """
        print(f'\nYour recipe for {self.portions} portions of {self.title}',
              f'({self.kind}):\n')
        print('------------------------------------------------')
        print(f'                {self.title.capitalize()}')
        print('------------------------------------------------\n')
        for i in range(0, len(self.ingredients)):
            print(f'{self.ingredients[i][1]}{self.ingredients[i][2]}',
                  f'{self.ingredients[i][0]}')
        print(f'\n{self.instructions} \n\n')

    def prepare_data(self):
        """
        prepare data for saving in spreadshit
        """
        today = date.today().strftime("%Y/%m/%d")
        ingredients = ''
        for ingredient in self.ingredients:
            ingredients += (str(ingredient[0]) + ',' + str(ingredient[1]) +
                            ',' + str(ingredient[2]))
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
            self.ingredients[i][1] = (float(self.ingredients[i][1]) /
                                      int(self.portions))
        self.portions = 1
        return self

    def validate_recipe(self):
        """
        Validates recipe input fields.
        verify if title, ingredient name and instructions are not empty
        and checks if kind, portions and amount are correct.
        Allows user to correct the errors.
        """
        try:
            if self.kind.lower() in CATEGORIES:
                pass
            else:
                raise ValueError
        except ValueError:
            print(f'Incorrect type of recipe:{self.kind}.')
            msg = 'Choose correct category: main course, dessert, breakfast:\n'
            self.kind = input(msg)
            self.validate_recipe()
        try:
            if self.title:
                pass
            else:
                raise ValueError
        except ValueError:
            print('Recipe title cannot be empty!')
            self.title = input("Enter your recipe's title\n").lower()
            self.validate_recipe()
        try:
            if int(self.portions) != 0:  # Parse to int and check value
                pass
            else:
                raise ValueError
        except ValueError:
            print(f'Incorrect portion number: {self.portions}.')
            self.portions = input('Enter number of portions:\n')
            self.validate_recipe()
        ingredient_idx = 0
        try:  # Check if ingredient amount is a decimal
            for i in range(0, len(self.ingredients)):
                if self.ingredients[i][0]:
                    ingredient_idx = i
                    float(self.ingredients[i][1])
                else:
                    print('\n\nIngredients must have names. Try again!')
                    add_recipe()
        except ValueError:
            ing_title = f'{self.ingredients[i][0]}'
            ing_unit = f'{self.ingredients[i][2]}'
            print(f'The amount for {ing_title}',
                  f'(unit: {self.ingredients[i][2]}) is wrong.',
                  'Please reenter the the amount!\n')
            msg = f'The amount of {ing_title} (unit: {ing_unit})\n'
            self.ingredients[ingredient_idx][1] = input(msg)
            self.validate_recipe()
        try:
            if self.instructions:
                pass
            else:
                raise ValueError
        except ValueError:
            print('Instructions field cannot be empty!')
            self.instructions = input("Enter recipes instructions\n")
            self.validate_recipe()
        return self


def find_recipe():
    """
    Finds a recipe within one category
    """
    print('\n\n\n\nYou chose to look for a recipe!')
    print('..............................\n')
    print('What kind of recipe are you looking for? Please select one of the',
          'categories: maine cours, dessert or breakfast.')
    category = get_category()
    recipe = get_recipe(category)
    portions = get_portions()
    print_found_recipe(category, portions, recipe)


def get_category():
    """
    gets and verifies user input returns chosen category
    """
    msg = '\nChoose category by typing: main cours, dessert or breakfast\n'
    category = input(msg)
    category = validate_category(category)
    return category


def get_recipe(category):
    """
    gets and verifies user input returns chosen recipe title to look for
    """
    recipe = input('Enter name of the recipe you are looking for:\n')
    recipe_details = look_for_recipe(recipe, category)
    return recipe_details


def get_portions():
    """
    gets and verifies user input, returns chosen number of portions
    """
    portions = input('\nHow many portions do you want to prepare:\n')
    try:
        if int(portions) != 0:  # Parse to int
            pass
        else:
            raise ValueError
    except ValueError:
        print(f'Incorrect portion number: {portions}.')
        portions = input('Enter number of portions:\n')
        get_portions()
    return portions


def validate_category(category):
    """
    Validate user category selection by user imput
    """
    try:
        if category.lower() in CATEGORIES:
            return category.lower()
        else:
            raise ValueError
    except ValueError:
        print(f'Incorrect type of recipe: {category}.')
        msg = f'Choose correct recipe type: {MAIN_COURSE_CATEGORY.lower()},'
        + f'{DESSERT_CATEGORY.lower()} or {BREAKFAST_CATEGORY.lower()}\n'
        category = input(msg)
        return validate_category(category)


def look_for_recipe(recipe, category):
    """
    Imports data from spreadsheet and checks if requested recipe exists
    withn choosen category
    """
    print(f'Looking for {recipe} in {category} category...\n')
    try:
        data = SHEET.worksheet(category)
        titles = data.col_values(1)
        try:
            index = titles.index(recipe.lower())
            print('\nLoading the recipe...')
            return data.row_values(index + 1)
        except ValueError:
            print(f'There is no recipe for {recipe} in the chosen category.\n')
            print('Do you want to try again?')
            if yes_no_choice():
                return get_recipe(category)
            else:
                show_command()
    except ValueError:
        show_command()


def print_found_recipe(category, portions, data):
    """
    imports data and prints the found recipe
    """
    ingredients = data[2].split(";")
    ingredients_lst = []

    for ingredient in ingredients:
        ingredient = ingredient.split(',')
        ingredients_lst.append(ingredient)
    for ingredient in ingredients_lst:
        ingredient[1] = float(ingredient[1]) * int(portions)

    title = data[0]
    instructions = data[3]

    recipe = Recipe(category, portions, title, ingredients_lst, instructions)
    recipe.recipe_print()


def browse_recipes():
    """
    Displays recipes within one category
    """
    print('\n\n\n\nYou chose to browse recipes!')
    print('............................\n')
    print('What kind of recipe are you looking for?\nPlease select category',
          'to browse: main course, dessert or breakfast')
    msg = f'\nChoose category by typing: {MAIN_COURSE_CATEGORY.lower()},'
    + f'{DESSERT_CATEGORY.lower()} or {BREAKFAST_CATEGORY.lower()}\n'
    category = input(msg)
    category = validate_category(category)
    recipes = load_recipes(category)
    print_recipes_list(recipes)
    preview_recipes(recipes, category)


def load_recipes(category):
    """
    Imports data from spreadsheet according to selected category
    """
    print(f'\nLoading {category} recipes...\n')
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


def preview_recipes(recipes, category):
    """
    asks user if they want to preview recipes
    request list of recipes to preview
    """
    print("\nDo you want to preview recipes?")
    if yes_no_choice():
        pass
    else:
        show_command()
    recipes_indexes_to_preview = get_recipes_indexes_to_preview(recipes)
    portions = get_portions()
    print_chosen_recipes(recipes_indexes_to_preview, category, portions)


def get_recipes_indexes_to_preview(recipes):
    """
    Gets user input for recipes to preview
    in form of numbers
    """
    print('Which recipes do you want to preview?')
    print('Please choose recipe by typing the corresponding numbers.',
          'Use following format: 1,3,5)')
    recipes_index_request = input('\nEnter your choice\n')
    return validate_request(recipes_index_request, recipes)


def validate_request(recipes_index_request, recipes):
    """
    Validates if requested recipes are given in right format
    and if they are in range for the number of recipes available
    """
    try:
        request_indexes = []
        recipes_indexes_request_list = recipes_index_request.split(",")
        for value in recipes_indexes_request_list:
            if int(value) <= len(recipes):
                pass
                request_indexes.append(int(value))
            else:
                print('One of the values is out of range!')
                raise ValueError
        return request_indexes
    except ValueError:
        msg = f"Invalid data: {recipes_indexes_request_list}. Try again!\n"
        print(msg)
        return get_recipes_indexes_to_preview(recipes)


def print_chosen_recipes(recipes_indexes, category, portions):
    """
    imports data and prints the recipes selected for preview
    """
    print('\nLoading recipes...\n')
    data = SHEET.worksheet(category)
    for recipe_index in recipes_indexes:
        index_in_sheet = recipe_index + 1
        recipe_data = data.row_values(index_in_sheet)
        print_found_recipe(category, portions, recipe_data)


def main():
    """
    Run all program functions
    """
    print("""
██████╗░███████╗░█████╗░██╗██████╗░███████╗  ██████╗░░█████╗░░█████╗░██╗░░██╗
██╔══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝
██████╔╝█████╗░░██║░░╚═╝██║██████╔╝█████╗░░  ██████╦╝██║░░██║██║░░██║█████═╝░
██╔══██╗██╔══╝░░██║░░██╗██║██╔═══╝░██╔══╝░░  ██╔══██╗██║░░██║██║░░██║██╔═██╗░
██║░░██║███████╗╚█████╔╝██║██║░░░░░███████╗  ██████╦╝╚█████╔╝╚█████╔╝██║░╚██╗
╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝╚═╝░░░░░╚══════╝  ╚═════╝░░╚════╝░░╚════╝░╚═╝░░╚═╝\n
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
                            """)
    sleep(0.5)
    print('Recipe book stores your recipes and allows you to access')
    sleep(0.1)
    print('them wheneveryou need. Add the recipe and whenever you want')
    sleep(0.1)
    print('to read it it will berecalculated into the number of portions')
    sleep(0.1)
    print('you declare to be interested in. You can add new recipes,')
    sleep(0.)
    print('find recipe by its title or browse through the recipes')
    sleep(0.1)
    print('of selected category. Good luck!')

    sleep(0.5)
    show_command()


main()
