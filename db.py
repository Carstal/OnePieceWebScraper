import certifi
from bs4 import BeautifulSoup
import requests
import pymongo

connection = 'mongodb+srv://carstaltari:Pablo__545@iot2-carlo.ijsiznf.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())
db = client["OP-TCG-DB"]
#cardDB = db["card"]


def get_all_cards():
    page = requests.post("https://en.onepiece-cardgame.com/cardlist/")
    soup = BeautifulSoup(page.text, "html.parser")
    cards = soup.findAll("dl", attrs={"class":"modalCol"})

    allCards = []

    for card in cards:
        #firstCard = cards[2]

        print_id = card["id"]
        printSplit = print_id.split("-")
        set_id = printSplit[0]

        cardInfo = card.findNext("div", attrs={"class":"infoCol"}).findAll("span")
        cardId = cardInfo[0].text
        cardRarity = cardInfo[1].text
        cardType = cardInfo[2].text
        cardName = card.findNext("div", attrs={"class":"cardName"}).text

        cardImg = card.findNext("div", attrs={"class":"frontCol"}).findNext("img")["src"]

        imgSplit = cardImg.split("..")
        defaultLink = "https://en.onepiece-cardgame.com/"
        imgLink = defaultLink + imgSplit[1]

        cardCost = card.findNext("div", attrs={"class": "cost"}).text

        if cardType == 'LEADER':
            cardCostSplit = cardCost.split('Life')
            cardCost = cardCostSplit[1]
        else:
            cardCostSplit = cardCost.split('Cost')
            cardCost = cardCostSplit[1]

        cardAttribute = card.findNext("div", attrs={"class":"attribute"}).findNext("i").text

        cardPower = card.findNext("div", attrs={"class":"power"}).text
        cardPowerSplit = cardPower.split('Power')
        cardPower = cardPowerSplit[1]

        cardCounter = card.findNext("div", attrs={"class":"counter"}).text
        cardCounterSplit = cardCounter.split('Counter')
        cardCounter = cardCounterSplit[1]

        cardColor = card.findNext("div", attrs={"class":"color"}).text
        cardColorSplit = cardColor.split('Color')
        cardColor = cardColorSplit[1]

        cardFeature = card.findNext("div", attrs={"class":"feature"}).text
        cardFeatureSplit = cardFeature.split('Type')
        cardFeature = cardFeatureSplit[1]

        cardText = card.findNext("div", attrs={"class":"text"}).text
        cardTextSplit = cardText.split('Effect')
        cardText = cardTextSplit[1]
        output = {
            "print_id": print_id,
            "card_id": cardId,
            "set_id": set_id,
            "rarity": cardRarity,
            "type": cardType,
            "name": cardName,
            "cost": cardCost,
            "attr": cardAttribute,
            "power": cardPower,
            "counter": cardCounter,
            "color": cardColor,
            "feature": cardFeature,
            "text": cardText,
            "img": imgLink
        }

        allCards.append(output)

    return allCards


def insert_many(cards):
    db.card.insert_many(cards)


# def update_many(cards):
#     db.card.update_many(cards)


# def update_one(card):
#     db.card.update_one(card)


def get_card_count():
    cardCount = db.card.count_documents({})
    return cardCount


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Cards in DB: {0}".format(get_card_count()))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
