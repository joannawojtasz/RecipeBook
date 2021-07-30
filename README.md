# Recipe book

Recipe Book is an data automation aplication for amatour and proffessional cooks enabling storing, browsing and rescaling essencial recipes. The application oushes and pulls data from google sheets containing the recipe and recalculates the precipe proportions accordingly to demanded number of portions.

## UX

###  Rationale

* Storing and accessing recipes is vital for work in the kitchen.

* Easy scaling of the recipes according to the number of portions allows avoidingmistakes in the kitchen.

### Clients

Recipe Book is designed for both for amatour and proffessional cooks who want to store and acces their recipes digitally.

### User stories

* It happens to me very often that I attempt to do a double portion of a recipe and in the middle of the preparation forget to dubble the ingredients messign up theproportions. I need an easy way to scale up my recipes.

* I need to store my recipes and be able to acces them without looking through many pages or a complicated search system.

* Sometimes I want to bake something but don't know precisely what that should be. I want to be able to browse some ideas within one category. 

### Design

Recipe Book is a terminal based application and therefore has a limited design options. 


### Flowchart

![Flowchart](images/RecipeBook.png)

A flowchart was created to visualize the planned functions within the aplication.

## Features

* Start screen

![Start screen]](images/start1.PNG)
![Start screen cont.]](images/start2.PNG)
A ASCII graphics showing a pot and decorative title were chosen for the front page to create positive user experiance. User is also offered a description of the aplication and guided through it by questions printed to the terminal.

* Add recipe

![Add recipe]](images/add.PNG)

Add recipe allows adding new record to the Recipe Book. Program asks user to give the title, category, number of portions, ingredients (name, amount, unit) and instructions. The input is validated and user is asked to confirm the data before the entry is saved.

* Find recipe

![Find recipe]](images/find.PNG)

Find recipe allows searchong through selected category and request displaying a recipe with given name. If the name is misspelled or recipe is not found user can re-enter the recipe to ook for.

* Browse

![Browse recipes]](images/browse.PNG)
![Browse recipes]](images/browse2.PNG)

The browse option allows to display list of recipes within a chosen category. User can choose between the recipes in the list and print them to the terminal.

## Testing

### Checking against [PEP8 requirements](http://pep8online.com/)

[x] too long lines and all were resolved
[x] trailing white spaces removed
[] trailing whitespaces in lines 442 and 443 within ASCII graphics remained to preserve graphics

### Manual testing

Manual testing included entering correct and wrong values to the code to check program response. Encountered bugs listed below.

#### Encountered bugs

[x] Extra ';' character in ingredient list

Problem: Empty ingredient created upon loading the recipe due to ';' at the end of ingredient list. 
Solution: The last character is removed before saving the recipe.

[x] Program breaks when entering new choice at second attempt

Problem: 'verify_users_choice' is not defined erroe. The choice is not updated when new value is entered, as the returned is not returned to the value 
Solution: As it is the first input, simpliest solution is to call the show_command() and restat the choice

[x] Program breaks at second attempt of entering new category within find function

Problem: validate_category takes new imput but does not return the value
Solution: Return validate_category(category) from the validate_category after getting new input.

[x] Program breaks at second attempt of entering new recipe within find function

Problem: function takes new imput but does not return the value
Solution: The function was re-writen, get_recipe(category) was returned from the look_for_recipe after getting new input.

## Deployment

The site was deployed to Heroku. The steps to deploy are as follows:

1. Add requirements for Heroku in the gitpod, commit and push to github.
2. Go to Heroku dashboard and click Add New App.
3. Select region: Europe and clicl set up app button.
4. Adjust settings in the settings tab:
* Create Config Var keys with value of the content of creds.json
* Add buildpacks by clicking on the add buildpack button and selecting heroku/python and heroku/nodejs follows by save buildpack.
5. Go to the deploy tab. Select Github as the diploy method. Select depository RecipeBook and click serach. Connect the repositiory with heroku.
6. Deploy manually to look through deploy logs.

The live link can be found here - [Recipe Book Page](https://recipe-book-by-joanna.herokuapp.com/)

The deployment of the page did not provide any errors.

## Credits 

* The ascii art comes from [asciiart.eu](https://www.asciiart.eu/)


