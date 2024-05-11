# Justice Pankey-Thompson - CSC 492-01
# The Main Class is the center of this program
# It is here where the Model is loaded and used
# It is here where the class objects are created and managed
# It is here where the User will interact with the program as a whole

import os
import tkinter as tk
import requests
from PIL import ImageTk, Image
from transformers import AutoTokenizer, AutoModelForCausalLM
from Pantry import Pantry
from Profile import Profile
from SpoonacularAPIHandler import Spoonacular


#Create global references for the class objects
global pantry
global profile
global spoonacular

#Method that will load the model, and use it to get recommendations and instructions
@staticmethod
def generateRecipes():
    query = ""

    #Use the Profile class to get the Health and Tastes info on the User
    cuisine = profile.getPrefCuisine()
    
    #If there is no cuisine specified, then don't one to the query
    if cuisine != "none":
        query += f"&cuisine={cuisine}"

    diet = profile.getDiet()
    #If there is no diet specified, don't add one to the query
    if diet != "none":
        query += f"&diet={diet}"
    
    #Use ingredients from the Users pantry
    onhand = ','.join(pantry.getIng())
    if onhand != "":
        query += f"&includeIngredients={onhand}"

    #Form the query to include instructions, and be healthy
    query += "&instructionsRequired=true"
    query += "&sort=healthiness"
    query += "&sortDirection=desc"
    
    #Get Spoonacular's response into 5 recipes
    results = spoonacular.generateRecipes(query)
    dishes = results.get('results')
    
    dishNames : list[str]
    dishNames = []
    dishID = list[int]
    dishID = []

    #Format the dishes from Spoonacular for the model
    for dish in dishes:
        dishNames.append(f"Name: {dish.get('title')} Recipe")
        dishID.append(int(dish.get('id')))

    #Load the Model, and use it to get its recommendations from the list of recipes
    tokenizer = AutoTokenizer.from_pretrained('./Models/Gemma2b;2024-05-09;16-56-17/')
    model = AutoModelForCausalLM.from_pretrained('./Models/Gemma2b;2024-05-09;16-56-17/')
    
    #Cuda:0 means the GPU
    device = "cuda:0"
    
    #Put the model and inputs on the same device (GPU)
    model = model.to(device)

    #Generate the Recommendations
    recommendations = {}
    for i in range(len(dishNames)):
        inputs = tokenizer(dishNames[i], return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_new_tokens=20)
        current = tokenizer.decode(outputs[0], skip_special_tokens=True)
        if " Indian " in current:
            recommendations.update({dishNames[i][6:-7]:dishID[i]})

    #Show the User the Recommendations and ask for response
    print("Do any of these sound good?")
    i = 1
    for recommendation in recommendations.keys():
        print(f"{recommendation} : {i}")
        i += 1
    
    #The User needs to input a proper choice on the list
    while True:
            try:
                print("\nPlease type the number associated with name of the dish you would like to make: ", end='')
                choice = int(input())

                if choice < 1 or choice > len(recommendations.values()):
                    print("Not a valid response. Try again.")
                    continue
                name = list(recommendations.keys())[choice - 1]
                break

            except:
                print("Not a valid response. Try again.")
                continue
    
    #Once the User makes a selection, get the instructions for them
    print(f"Your selection is {name}. Fetching the recipe instructions.")
    
    info = spoonacular.getInstructions(recommendations.get(name))
    used = []
    recipe = info.get('analyzedInstructions')

    #Print out the instructions to the User
    for item in recipe:
        for instruction in item.get('steps'):
            print(f"Step {instruction.get('number')}: {instruction.get('step')}\n")
            for ingredient in instruction.get('ingredients'):
                used.append([ingredient.get('name'), 1])
    
    #Enjoy!
    print("Enjoy your meal!")
    
    #Update the Pantry to use up what was in the recipe
    results = spoonacular.getNutrition(recommendations.get(name))
    pantry.useUp(used)

    #Update the Profile's Daily Values so the user can monitor their nutritional intake
    info = results.get('nutrition')
    nutrients = info.get('nutrients')
    dv = []
    for nutrient in nutrients:
        dv.append(float(nutrient.get('amount')))
    profile.updateDV(dv)

    #Print out a picture of the recipe the user is going to make
    #Format: https://img.spoonacular.com/recipes/id-556x370.jpg
    #Make sure to replace the id with the id of the recipe you want to view
    image_url = f"https://img.spoonacular.com/recipes/{recommendations.get(name)}-556x370.jpg"

    #Save image to local folder to view
    img_data = requests.get(image_url).content

    #Open image file and read the bytes
    with open('curr.jpg', 'wb') as handler:
        handler.write(img_data)

    #Create tkinter window for viewing the image
    root = tk.Tk()
    root.title(f"{name}")
    img = ImageTk.PhotoImage(Image.open("curr.jpg"))
    label = tk.Label(image=img)
    label.pack()

    #Display the window
    root.mainloop()


        
#Update Health Data through Profile's survey
@staticmethod
def updateHealth(healthData):
    profile.inputData(healthData)

#Update Daily Values from the list of Daily Values consumed
@staticmethod
def updateDailyValues(dailyValues):
    profile.updateDV(dailyValues)

#Used to update the User's die
def updateDiet(self):
    print("Please input the diet you wish to change to. Type none for no diet:", end=" ")
    diet = input().lower()
    if profile.updateDiet(diet) == 1:
        print("Error: Invalid selection. Try again.")
        self.updateDiet()
        return

#Calls the Profile class to update the user's preferred cuisine
@staticmethod
def updateCuisine(cuisine):
    profile.updateCuisine(cuisine)

#Allow the user to add to their pantry (like if they went grocery shopping)
@staticmethod
def addIngredients():
    print("Please enter the name of the ingredient you wish to add (singular). Leave empty to stop:", end=" ")
    name = input()
    
    #Let the user continue adding until they've added everything
    while name != "":
        print(f"How many {name}s do you want to add?:", end=" ")
        quantity = int(input())
        pantry.addIngredients((name, quantity))
        
        #Start next loop
        print("Please enter the name of the ingredient you wish to add (singular). Leave empty to stop:", end=" ")
        name = input()

    print("Finished adding ingredients.")

#Allow the user to remove from their pantry (like if they cooked themselves, or food spoiled)
@staticmethod
def manualRemoveIng():
    print("Please enter the name of the ingredient you wish to use (singular). Leave empty to stop:", end=" ")
    name = input()
    ingList : list
    ingList = []
    
    #Let the user continue removing all they need to remove
    while name != "":
        print(f"How many {name}s did you use?:", end=" ")
        quantity = int(input())
        ingList.append([name, quantity])
        
        #Start next loop
        print("Please enter the name of the ingredient you wish to use (singular). Leave empty to stop:", end=" ")
        name = input()

    print("Finished removing ingredients.")
    #Update Pantry
    pantry.useUp(ingList)

#Similar to manualRemoveIng, but made for one ingredient at a time from recipes
@staticmethod
def useIng(ingredients):
    pantry.useUp(ingredients)

#Retrieve all of the user's pantry and profile information
@staticmethod
def getUserInfo():
    #Create a string and fill it with the all of the user's information
    info : str
    
    info = f"Health: {profile.getIntolerances()}\n"
    
    info += f"Preferred Cuisine: {profile.getPrefCuisine()}\n"
    
    info += f"Diet: {profile.getDiet()}\n"
    
    info += f"Daily Values:\n"

    #Daily Values is a list of different nutrients
    for dv in profile.getDV():
        info += "\t" + dv + "\n"

    info += f"\nIngredients in Pantry:\n"
    
    #Pantry has a list of ingredients and quantities
    ings = pantry.getIngFull()

    for i in range(len(ings[0])):
        info += f"\t{ings[0][i]} : {ings[1][i]}\n"
    
    #Return complete info
    return info

#Main handles the main menu the user interacts with 
#Main also creates and deletes the different class objects
def main():
    #Greet user and create objects
    print("Welcome to the Recipe Recommender!\n")
    
    global profile, pantry, spoonacular

    profile = Profile()
    pantry = Pantry()
    spoonacular = Spoonacular()

    #Until the user selects Quit (7), keep the program running
    while True:
        print("""\nWhat would you like to do?
        Recommend me a Recipe : 1
        View all of my Info   : 2
        View my Pantry Items  : 3
        View my Health/Taste  : 4
        Update Pantry Items   : 5
        Update My Profile     : 6
        Quit                  : 7""")

        #The user needs to input a valid response. Keep asking them to retry until they put one in
        while True:
            try:
                print("\nPlease type the number associated with the action you wish to take: ", end="")
                choice = int(input())
                if choice < 1 or choice > 7:
                    print("Not a valid response. Try again.")
                    continue
                break
            except:
                print("Not a vailid response. Try again.")
                continue

        #Depending what the user selected, run their selection
        match choice:
            case 1:
                print("Recommending recipes...\n")
                generateRecipes()

            case 2:
                #All user info
                print("Fetching Information...\n")
                print(getUserInfo())

            case 3:
                #Just pantry
                print("Fetching Pantry Information...\n")
                for ingredients in pantry.getIng():
                    print(ingredients)
            
            case 4:
                #Just profile
                print("Fetching User Profile...\n")
                print(f"Diet: {profile.getDiet()}")
                print(f"Intolerances: {profile.getIntolerances()}")
                print(f"Preferred Cuisine: {profile.getPrefCuisine()}")
                print(f"Daily Values:")
                for dv in profile.getDV():
                    print(f"\t{dv}")

            case 5:
                #Update the pantry
                #Need to determine if user is adding or deleting first
                print("Okay. Let's update the pantry.\n")
                #Make sure the user gives an appropriate answer
                while True:
                    print("Type 1 to add ingredients. Type 2 to remove ingredients: ", end="")
                    try:    
                        response = int(input())
                        
                        if response == 1:
                            addIngredients()
                        
                        elif response == 2:
                            manualRemoveIng()
                        
                        else:
                            print("Invalid response. Try again.")
                            continue
                        
                        break
                    
                    except:
                        print("Invalid response. Try again.")
                        continue
            
            case 6:
                #Have the user take the quiz to update their health and preferences
                print("Okay. Let's update your profile.\n")
                profile.quiz()
            
            case 7:
                #Delete class objects, and say goodbye. End the program
                del(profile, pantry, spoonacular)
                print("Thank you for using this program. Goodbye.")
                break

#Start the program
main()