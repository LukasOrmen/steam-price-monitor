import json
import requests

def getappid(url):
    #getting the appid and checking if the url is valid
    if url[0:35] == "https://store.steampowered.com/app/":
        return url.split("/")[4]
    else:
        print("Invalid url.")
        exit()


def listgames():
    with open("games.json", "r") as f:
        jdata = json.loads(f.read())
    for key in jdata["games"]:
        desc = requests.get("https://store.steampowered.com/api/appdetails?appids=" + key)
        r = json.loads(desc.text)
        if r[key]["data"]["is_free"] == True:
            print(r[key]["data"]["name"] + ", is free.")
        else:
            name = r[key]["data"]["name"]
            price = r[key]["data"]["price_overview"]["final"]
            discount = r[key]["data"]["price_overview"]["discount_percent"]
            currency = r[key]["data"]["price_overview"]["currency"]
            if int(discount) > 0:
                print("{Name}, is currently {Price}{Currency} and {discount_percent}% off.".format(Name = name, Price = str(int(price) / 100), Currency = currency, discount_percent = discount))
            else:
                print("{Name}, is currently {Price}{Currency}.".format(Name = name, Price = str(int(price) / 100), Currency = currency))


def addgame(appid):
    #loading the secription of the game
    descurl = "https://store.steampowered.com/api/appdetails?appids=" + appid
    response = json.loads(requests.get(descurl).text)

    #parsing the description dict
    gamename = response[appid]["data"]["name"]

    with open("games.json", "r") as f:
        jdata = json.loads(f.read())
    jdata["games"] += [appid]
    with open("games.json", "w") as f:
        f.write(json.dumps(jdata))
        print(gamename + ", was successfully added to the list of games that will be monitored!")

def removegame():
    with open("games.json", "r") as f:
        jdata = json.loads(f.read())
    for value in jdata["games"]:
        name = json.loads(requests.get("https://store.steampowered.com/api/appdetails?appids=" + value).text)
        print("{Value} - {Jdata}".format(Value = value, Jdata = name[value]["data"]["name"]))
    game = input("Enter the id of the game you want to remove from the monitor list: ")
    jdata["games"].remove(game)
    with open("games.json", "w") as f:
        f.write(json.dumps(jdata))
    print(game + ", successfully deleted")


start = input("[1] List games\n[2] Add a game\n[3] Remove a game")
if start == "1":
    listgames()
if start == "2":
    addgame(getappid(input("Enter the steam game url: ")))
if start == "3":
    removegame()
