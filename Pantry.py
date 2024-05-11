#Class used to store and retrieve ingredient data for the model to use
#The class has 5 functions used for assisting the model and user with anything ingredient related
#The pantry info is stored as a csv file.
import csv
import os

#All ingredients and quantities are stored in a dictionary
#The dictionary's keys are the names, and the values are the quantities of the ingredients
global ingredients
ingredients : dict

class Pantry:
    #Pantry Constructor
    def __init__(self) -> None:
        
        #Check if there already is a Pantry.csv file from previous session
        global ingredients
        ingredients = {}
        try:
            
            #If there is a Pantry.csv file, read its contents and add it to the Pantry object's ingredient variable
            with open("Pantry.csv", "r", newline='') as file:
                storedIng = csv.reader(file)
                for row in storedIng:
                    ingredients.update({row[0]:int(row[1])})

        #If no Pantry.csv is found, then this is the first session on this device
        #No file is needed for now, and the pantry stays empty
        except:
            print("Pantry.csv file not found, pantry is empty and needs to be filled.")
            self.manualRestock()

        print("Pantry initialized successfully.")

    #When the user agrees to use a recipe, this function will update the ingredient from what was used
    @staticmethod
    def useUp(used:list[tuple[str, int]]):
        for ing in used:
            
            #Remember the number of an item left after what the recipe used
            try:
                leftover = ingredients.get(ing[0]) - ing[1]
            
            #Remove the ingredient from the dictionary
                ingredients.pop(ing[0])
                #If the number leftover is 0 or less, there is no need to add it back to the ingredient list
                if leftover >= 1:
                    ingredients.update({ing[0]: leftover})
            except:
                #Couldn't find the ingredient in the pantry
                print(f"No {ing[0]}s in the pantry. You will need to aquire {ing[1]} of them.")
    
    #When the user goes shopping, or aquires ingredients, they can call this function to add it to the list
    @staticmethod
    def addIngredients(ing):
        
        #Check if there already is some there. If there is, add to it
        try:
            onhand = ingredients.get(ing[0])
            ingredients.update({ing[0]: ing[1] + onhand})
        except:
            
            #New ingredient not in pantry
            ingredients.update({ing[0]: ing[1]})
    
    #When the user cooks something on their own, and/or goes shopping, they can call this to update the list
    def update(self, used, newIngs):
        self.useUp(used)
        self.addIngredients(newIngs)

    #Used to retrieve the list of keys and values from the dictionary
    @staticmethod
    def getIngFull():
        
        #Ingredient Names are the keys, Quantities are the values
        ingredientNames = list(ingredients.keys())
        ingredientQuantities = list(ingredients.values())
        return (ingredientNames, ingredientQuantities)
    
    #Return list of ingredient names in pantry
    @staticmethod
    def getIng():
        ingredientNames = list(ingredients.keys())
        return (ingredientNames)
    
    #When the user wants to add more items to their pantry, they can do so here
    @staticmethod
    def manualRestock():
        print("Please enter the name of the first ingredient you have in your pantry (Type \"end\" when you have no more ingredients): ", end="")
        name = ""
        
        #First get name of ingredient
        while True:
            name = input()
            if name == "end":
                break
            
            #Then make sure user adds a real number of them to add
            while True:
                print(f"Please enter the number of {name}s you have: ", end="")
                
                try:
                    quantity = int(input())
                    if quantity < 1:
                        print("Value not valid. Try again")
                        continue
                    
                    break
                
                except:
                    print("Need a whole number. Try again.")
                    continue
            
            #Add their selection to the ingredient dictionary
            ingredients.update({name : quantity})
            print(f"Added {quantity} {name}s to the pantry")
            
            #Continue the loop
            print("Please enter the name of the next ingredient you have in your pantry (Type \"end\" when you have no more ingredients): ", end="")

        print("Done adding ingredients.")

    
    #Before the program terminates, the ingredient list needs to be saved to the Pantry.csv file
    @staticmethod
    def saveToFile():
        
        #If this is the first time using the program, the file won't exist, so it needs to be checked for first
        if os.path.exists("Pantry.csv"):
            os.remove("Pantry.csv")

        #Write down ingredients to Pantry.csv
        with open("Pantry.csv", "w", newline='') as file:

            for item in ingredients.items():
                (name, quantity) = item
                file.write(name + "," + str(quantity) + "\n")
            print("Saved Pantry data.")
            file.close()
    
    #Before deleting, make sure to save important info!
    def __del__(self):
        self.saveToFile()
        print("Pantry terminated.")