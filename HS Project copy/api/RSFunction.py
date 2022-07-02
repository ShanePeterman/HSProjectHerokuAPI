import pymongo
from pymongo import MongoClient
import requests

cluster = MongoClient("mongodb+srv://stpeterman0131:shaner11@cluster0.1nunq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["testdb"]
collection = db["testcollection"]



#global skills and activities list
skills = [
    "overall", "attack", "defence", "strength", "hitpoints",
    "ranged", "prayer", "magic", "cooking", "woodcutting", 
    "fletching", "fishing", "firemaking", "crafting", "smithing", 
    "mining", "herblore", "agility", "thieving", "slayer", "farming", 
    "runecraft", "hunter", "construction", "leaguepoints", "bountyhunterhunter",
    "bountyhunterrogue", "cluescrollsall", "cluescrollsbeginner", 
    "cluescrollseasy", "cluescrollsmedium", "cluescrollshard",
    "cluescrollselite", "cluescrollsmaster", "lmsrank", "soulwarszeal",
    "riftsclosed", "abyssalsire", "alchemicalhydra", "barrowschests", "bryophyta",
    "callisto", "cerberus", "chambersofxeric", "chambersofxericchallengemode", "chaoselemental",
    "chaosfanatic", "commanderzilyana", "corporealbeast", "crazyarchaeologist",
    "dagannothprime", "dagannothrex", "dagannothsupreme", "derangedarchaeologist",
    "generalgraardor", "giantmole", "grotesqueguardians", "hespori",
    "kalphitequeen", "kingblackdragon", "kraken", "kreearra", "kriltsutsaroth",
    "mimic", "nex", "nightmare", "phosanisnightmare", "obor", "sarachnis",
    "scorpia", "skotizo", "tempoross", "thegauntlet", "thecorruptedgauntlet", 
    "theatreofblood", "theatreofbloodhardmode", "thermonuclearsmokedevil",
    "tzkalzuk", "tztokjad", "venenatis", "vetion", "vorkath", "wintertodt", 
    "zalcano", "zulrah"
    ]



#global list for name component of Skill/Activity data
skillNames = [
    "Overall", "Attack", "Defence", "Strength", "Hitpoints",
    "Ranged", "Prayer", "Magic", "Cooking", "Woodcutting", 
    "Fletching", "Fishing", "Firemaking", "Crafting", "Smithing", 
    "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming", 
    "Runecraft", "Hunter", "Construction", "League Points", "Bounty Hunter: Hunter",
    "Bounty Hunter: Rogue", "Clue Scrolls (All)", "Clue Scrolls (Beginner)", 
    "Clue Scrolls (Easy)", "Clue Scrolls (Medium)", "Clue Scrolls (Hard)",
    "Clue Scrolls (Elite)", "Clue Scrolls (Master)", "LMS Rank", "Soul Wars Zeal",
    "Rifts Closed", "Abyssal Sire", "Alchemical Hydra", "Barrows Chests", "Bryophyta",
    "Callisto", "Cerberus", "Chambers Of Xeric", "Chambers Of Xeric: CM", "Chaos Elemental",
    "Chaos Fanatic", "Commander Zilyana", "Corporeal Beast", "Crazy Archaeologist",
    "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme", "Deranged Archaeologist",
    "General Graardor", "Giant Mole", "Grotesque Guardians", "Hespori",
    "Kalphite Queen", "King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth",
    "Mimic", "Nex", "Nightmare", "Phosani's Nightmare", "Obor", "Sarachnis",
    "Scorpia", "Skotizo", "Tempoross", "The Gauntlet", "The Corrupted Gauntlet", 
    "Theatre Of Blood", "Theatre Of Blood: Hard Mode", "Thermonuclear Smoke Devil",
    "TzKal-Zuk", "TzTok-Jad", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt", 
    "Zalcano", "Zulrah"
    ]



def CheckDatabase(name):
    '''Check if item is already in database. returns boolean'''

    # variable to hold response from checking database
    result = collection.count_documents({"_id": name})

    #if found in database
    if result == 1:
        return True
    
    return False



def MakeAPICall(name):
    '''Make API Call to oldschool runescape HiScores API and check to see if player exists in hiscores'''
    #Variable for request url + name var
    hiscores_request = 'https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player=' + name
    
    #make api get request
    apiResponse = requests.get(hiscores_request)

    isInHS = apiResponse.ok

    if isInHS == True:
        return apiResponse
    return False

    

def DeletePlayerData(name):
    myQuery = {"_id": name}
    collection.delete_one(myQuery)

    return
        


def MakePlayerDictionary(name, response):
    '''convert response from API Call to dictionary'''

    #get text from api call and store into variable
    text = response.text

    #intialize list one with first element as player name
    list_one = []

    #Create list from comma seperated values in text and append to list_one
    list_one.extend(text.splitlines(True))
    playerData = {"_id":name,
            "userData": {}}

    #loop to format data and populate dictionary
    for i in range(85):

        #assign each individual skill to corresponding value in list 2

        #assign each individual list element to string mystring
        mystring = list_one[i]

        #split values in string by comma and turn into list #2
        list_two = mystring.split(",")

        #remove newline characters from list_two elements
        if len(list_two) == 3: 
            list_two[2]= list_two[2].replace('\n','')
        elif len(list_two) == 2:
            list_two[1]= list_two[1].replace('\n','')

        #populate dictionary with keys based on list skills and values based on list list_two
        if len(list_two) == 2:
            playerData["userData"][skills[i]] = {"rank":list_two[0], "score":list_two[1], "name":skillNames[i]}
        elif len(list_two) == 3:
            playerData["userData"][skills[i]] = {"rank":list_two[0], "level":list_two[1], "xp":list_two[2], "name":skillNames[i]}
    
    # return the dictionary
    return playerData



def StoreDataInDB(playerData):
    '''inserts data into mongoDB'''
    # to insert the players data into the database
    collection.insert_one(playerData)

def GetDataFromDB(name):
    '''Gets data from mongoDB database'''
    
    #store results in variable results
    results = collection.find_one({"_id": name})

    playerData = {"_id": results["_id"],
            "userData": {}}

    #lop through results and assign data to new dictionary
    for i in skills:
        
        if len(results["userData"][i]) == 3:
            playerData["userData"][i] = {"rank": results["userData"][i]["rank"], "score": results["userData"][i]["score"], "name":results["userData"][i]["name"]}
        elif len(results["userData"][i]) == 4:
            playerData["userData"][i] = {"rank": results["userData"][i]["rank"], "level": results["userData"][i]["level"], "xp": results["userData"][i]["xp"], "name":results["userData"][i]["name"]}

    
    return playerData



def GetPlayerData(name):
    '''Get player data from DB/Hiscore API and return as dictionary'''
    #initiate isFound to False
    isFound = False

    #check to see if player is in database
    isFound = CheckDatabase(name)

    #if player is in database
    if isFound == True:
        
        #gets data from mongoDB and stores it in dictionary
        playerData = GetDataFromDB(name)
        return playerData

    #if player is not in database
    elif isFound == False:

        #check to see if player exists
        response = MakeAPICall(name)

        #if player does not exist
        if response is None:
            print("Player not found")
            return

        #if player does exist    
        else:
            playerData = MakePlayerDictionary(name, response)

            #store data in database
            StoreDataInDB(playerData)

            return playerData



def UpdatePlayerData(name):

    response = MakeAPICall(name)

    if response is None:
        
        return
    
    else:
        
        DeletePlayerData(name)

        playerData = MakePlayerDictionary(name, response)

        StoreDataInDB(playerData)

        return playerData
