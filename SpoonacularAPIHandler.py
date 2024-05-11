#This class handles all requests from SpoonacularAPI
#The API has a limit on how many times a key can call per day, so be careful
import requests

global spoonacular_key

class Spoonacular:
    #Initialize the class, and set the api key
    def __init__(self) -> None:
        global spoonacular_key 
        spoonacular_key= "2badc30033bf439fa3f0946976d49a11"

        print("Spoonacular initialized successfully.")
    
    #Gets 5 recipes from Spoonacular based on the user's health and pantry fed to the query
    @staticmethod
    def generateRecipes(param):
        url = "https://api.spoonacular.com/recipes/complexSearch"
        
        #Limit to 5 for testing as to not deplete point limit
        query = url + "?" + "apiKey=" + spoonacular_key + "&number=5" + param
        response = requests.get(query)
        return response.json()
    
    #Gets the nutritional information of a recipe from Spoonacular based on the recipe ID 
    @staticmethod
    def getNutrition(id):
        url = f"https://api.spoonacular.com/recipes/{id}/information"
        
        #Must make sure to only use recipes with instructions, there is no need for wine pairing or taste data right now
        param = "&includeNutrition=true&addWinePairing=false&addTasteData=false"
        query = url + "?" + "apiKey=" + spoonacular_key + param
        response = requests.get(query)
        return response.json()
    
    #Gets the instructions on how to make a recipe
    @staticmethod
    def getInstructions(id):
        url = f"https://api.spoonacular.com/recipes/{id}/information"
        
        #We would have received Nutrition data already, there is no need for wine pairing or taste data right now
        param = "&includeNutrition=false&addWinePairing=false&addTasteData=false"
        query = url + "?" + "apiKey=" + spoonacular_key + param
        response = requests.get(query)
        return response.json()