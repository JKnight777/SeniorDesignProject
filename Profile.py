#Class used to store and retrieve intolerances and preference data on the user
#The class has functions used for assisting the model and user on the user's health and tastes
#The profile info is stored as a csv file.
import os
import csv

global intolerances
global prefCuisine
global dietCode
global dietCodes
global dailyValues

intolerances : list[str]
prefCuisine : str
dietCode : int
dietCodes : dict[int, str]
dailyValues : list[float]

class Profile:
    #Profile Constructor
    def __init__(self) -> None:
        global intolerances
        global prefCuisine
        global dietCode
        global dietCodes
        global dailyValues

        #Spoonacular provides information about 40 nutrients
        #They are always in the same order, so no need to store names or units
        dailyValues = [0] * 40
        intolerances = []
        
        #Spoonacular recognizes 10 specific diets. Users must choose from the following list
        dietCodes = {
            0 : "none",
            1 : "vegan",
            2 : "vegetarian",
            3 : "ovo-vegetarian",
            4 : "lacto-vegetarian",
            5 : "ketogenic",
            6 : "gluten free",
            7 : "pescetarian",
            8 : "paleo",
            9 : "low fodmap",
            10 : "whole 30",
        }
        
        #Check if there already is a Profile.csv file from previous session
        try:
            #If there is a Profile.csv file, read its contents and add it to the Profile object's variables
            with open("Profile.csv", "r", newline='') as file:
                info = csv.reader(file)

                intolerances = next(info)
                prefCuisine = next(info)[0]
                dietCode = int(next(info)[0])

                #The remaining values will always be the 40 nutrients
                nutrients = []
                for nutrient in info:
                    nutrients.append(nutrient[0])
                
                #Add them to the dv list
                i = 0
                for dv in nutrients:
                    dailyValues[i] = (float(dv))
                    i += 1
                file.close()


        #If no Profile.csv is found, then this is the first session on this device
        #No file is needed for now, and the Profile stays empty until the user quits
        except:
            print("Profile.csv file not found, must take quiz!")
            self.quiz()
        print("Profile initialized successfully.")
            

    #Used to update the daily values from when a user consumes a meal
    @staticmethod
    def updateDV(dv: list[float])->None:
        i = 0
        for nutrient in dv:
            dailyValues[i] = float(nutrient)
            i += 1
            if i == 40:
                break

    #When the user or program needs to update the entire profile
    def inputData(self, data: list)->None:
        self.updateIntolerances(data[0])
        self.updateCuisine(str(data[1]))
        self.updateDiet(str(data[2]))
        self.updateDV(data[3])

    #When the user cooks something on their own, and/or goes shopping, they can call this to update the list
    @staticmethod
    def getIntolerances()->list[str]:
        return intolerances
    
    #Get Preferred Cuisine
    @staticmethod
    def getPrefCuisine()->str:
        return prefCuisine
    
    #Get the user's diet from the dictionary using their dietCode
    @staticmethod
    def getDiet()->int:
        return dietCodes.get(dietCode)

    #Used to retrieve the list of nutrients and their current values
    @staticmethod
    def getDV()->list[str]:
        dv = ["Calories: " + str(dailyValues[0])]
        dv.append("Fat: " + str(dailyValues[1]))
        dv.append("Trans Fat: " + str(dailyValues[2]))
        dv.append("Saturated Fat: " + str(dailyValues[3]))
        dv.append("Mono Unsaturated Fat: " + str(dailyValues[4]))
        dv.append("Poly Unsaturated Fat: " + str(dailyValues[5]))
        dv.append("Protien: " + str(dailyValues[6]))
        dv.append("Cholesterol: " + str(dailyValues[7]))
        dv.append("Carbohydrates: " + str(dailyValues[8]))
        dv.append("Net Carbohydrates: " + str(dailyValues[9]))
        dv.append("Alcohol: " + str(dailyValues[10]))
        dv.append("Fiber: " + str(dailyValues[11]))
        dv.append("Sugar: " + str(dailyValues[12]))
        dv.append("Sodium: " + str(dailyValues[13]))
        dv.append("Caffiene: " + str(dailyValues[14]))
        dv.append("Managnese: " + str(dailyValues[15]))
        dv.append("Potassium: " + str(dailyValues[16]))
        dv.append("Magnesium: " + str(dailyValues[17]))
        dv.append("Calcium: " + str(dailyValues[18]))
        dv.append("Copper: " + str(dailyValues[19]))
        dv.append("Zinc: " + str(dailyValues[20]))
        dv.append("Phosphorus: " + str(dailyValues[21]))
        dv.append("Flouride: " + str(dailyValues[22]))
        dv.append("Choline: " + str(dailyValues[23]))
        dv.append("Iron: " + str(dailyValues[24]))
        dv.append("Vitamin A: " + str(dailyValues[25]))
        dv.append("Vitamin B1: " + str(dailyValues[26]))
        dv.append("Vitamin B2: " + str(dailyValues[27]))
        dv.append("Vitamin B3: " + str(dailyValues[28]))
        dv.append("Vitamin B5: " + str(dailyValues[29]))
        dv.append("Vitamin B6: " + str(dailyValues[30]))
        dv.append("Vitamin B12: " + str(dailyValues[31]))
        dv.append("Vitamin C: " + str(dailyValues[32]))
        dv.append("Vitamin D: " + str(dailyValues[33]))
        dv.append("Vitamin E: " + str(dailyValues[34]))
        dv.append("Vitamin K: " + str(dailyValues[35]))
        dv.append("Folate: " + str(dailyValues[36]))
        dv.append("Folic Acid: " + str(dailyValues[37]))
        dv.append("Iodine: " + str(dailyValues[38]))
        dv.append("Selenium: " + str(dailyValues[39]))
        return dv
    
    #Changes Intolerances
    @staticmethod
    def updateIntolerances(intolerancesData: list[str])->None:
        global intolerances
        intolerances = intolerancesData
    
    #Changes Preferred Cuisine
    @staticmethod
    def updateCuisine(cuisine: str)->None:
        global prefCuisine
        prefCuisine = cuisine

    #Changes the user's diet based on their new diet code
    @staticmethod
    def updateDiet(diet: int)->None:
        global dietCode
        codes = list(dietCodes.keys())
        diets = list(dietCodes.values())
        dietCode = codes[diets.index(diet)]

    #When the user needs to create a profile, or update their own, this will be called
    def quiz(self)->None:
        #Ask the user to provide information
        global intolerances, dietCode, prefCuisine
        print("Please take a short survey to help us better understand your health and tastes:\n")
        print("Do you have any intolerances from the following list?")

        #These are all the intolerances Spoonacular recognizes
        intolDict = {
            0 : "None",
            1 : "Egg",
            2 : "Gluten",
            3 : "Grain",
            4 : "Peanut",
            5 : "Seafood",
            6 : "Sesame",
            7 : "Shellfish",
            8 : "Soy",
            9 : "Sulfite",
            10 : "Tree Nut",
            11 : "Wheat",
            12 : "Dairy"
        }

        #List the selections to the user
        for key in intolDict:
            print(f"{intolDict.get(key)} : {key}")

        intolerances = []
        
        #Users can have more than one intolerance
        while True:
            print("Please type the number associated with your next intolerance: ", end="")
            
            #Needs to be an intolerance on the list. Keep asking till the user provides one
            try:
                response = int(input())
                if (response != 0):
                    if (response < 13):
                        print(intolDict.get(response))
                        intolerances.append(intolDict.get(response))
                        print(f"{intolDict.get(response)} intolerance recorded.")
                        continue
                    else:
                        print("Invalid response. Try again.")
                        continue
                else:
                    print("Finished recording intolerances.\n")
                    break
            except:
                print("Invalid response. Try again.")
                continue
        
        #Show the user all available diets
        print("Please select your diet from the following list:")
        for diet in dietCodes:
            print(f"{dietCodes.get(diet)} : {diet}")

        #The user must enter a valid diet code. Keep asking till they give one
        while True:
            print("Please type the number associated with your diet: ", end="")
            try:
                dietCode = int(input())

                if dietCode > 10:
                    print("Invalid response. Try again.")
                    continue

                print(f"Recorded {dietCodes.get(dietCode)} diet.\n")
                break

            except:
                print("Invalid response. Try again.")
                continue
        
        #Spoonacular only recognizes 26 cuisines. The user must choose a favorite from them
        print("Please select your favorite cuisine from the following list:")
        cuisinesDict = {
            0 : "African",
            1 : "Asian",
            2 : "American",
            3 : "British",
            4 : "Cajun",
            5 : "Caribbean",
            6 : "Chinese",
            7 : "Eastern European",
            8 : "European",
            9 : "French",
            10 : "German",
            11 : "Greek",
            12 : "Indian",
            13 : "Irish",
            14 : "Italian",
            15 : "Japanese",
            16 : "Jewish",
            17 : "Korean",
            18 : "Latin American",
            19 : "Mediterranean",
            20 : "Mexican",
            21 : "Middle Eastern",
            22 : "Nordic",
            23 : "Southern",
            24 : "Spanish",
            25 : "Thai",
            26 : "Vietnamese",
            27 : "none"
        }

        #Present choices to user
        for cuisine in cuisinesDict:
            print(f"{cuisinesDict.get(cuisine)} : {cuisine}")

        #User needs to submit a valid cuisine, keep asking till they provide one
        while True:
            print("Please type the number associated with your favorite cuisine: ", end="")
            try:
                response = int(input())
                if response > 27:
                    print("Invalid response. Try again.")
                    continue

                prefCuisine = cuisinesDict.get(response)
                print(f"{prefCuisine} food saved as favorite cuisine.\n")
                break

            except:
                print("Invalid response. Try again.")
                continue

        #Now the user is all set-up
        print("That concludes our survey, thank you very much for setting up your profile!")

    #Before the program terminates, the variables need to be saved to the Profile.csv file
    @staticmethod
    def saveToFile()->None:
        
        #If this is the first time using the program, the file won't exist, so it needs to be checked for first
        if os.path.exists("Profile.csv"):
            os.remove("Profile.csv")

        with open('Profile.csv', 'w') as file:
            if intolerances != []:
                for intolerance in intolerances[:-1]:
                    file.write(f"{intolerance},")
                file.write(f"{intolerances[-1]}\n")
            else:
                file.write("\n")
            file.write(prefCuisine + "\n")
            file.write(str(dietCode) + "\n")
            for dv in dailyValues:
                file.write(str(dv) +"\n")
            file.close()

        print("Saved Profile data.")
    
    #Before deleting, make sure to save important info!
    def __del__(self):
        self.saveToFile()
        print("Profile terminated.")