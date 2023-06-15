from bs4 import BeautifulSoup
import requests

def get_all_cards():
    # Get response from request to fetch all card data
    page = requests.post("https://en.onepiece-cardgame.com/cardlist/")
    # Parse the html to Beautiful Soup
    soup = BeautifulSoup(page.text, "html.parser")
    # Identify and create a collection of card data
    cards = soup.findAll("dl", attrs={"class":"modalCol"})

    # Initialize array to hold data
    allCards = []

    # Loop through all elements
    for card in cards:

        # Get Value of Id
        print_id = card["id"]
        # Split it to identify card set
        printSplit = print_id.split("-")
        set_id = printSplit[0]

        # Get all span element within next div with corresponding class name
        cardInfo = card.findNext("div", attrs={"class":"infoCol"}).findAll("span")
        # .text to get value inside the element / exclude html tags
        cardId = cardInfo[0].text
        cardRarity = cardInfo[1].text
        cardType = cardInfo[2].text

        cardName = card.findNext("div", attrs={"class":"cardName"}).text

        cardImg = card.findNext("div", attrs={"class":"frontCol"}).findNext("img")["src"]
        imgSplit = cardImg.split("..")
        # Build full link for image source
        defaultLink = "https://en.onepiece-cardgame.com/"
        imgLink = defaultLink + imgSplit[1]

        cardCost = card.findNext("div", attrs={"class": "cost"}).text
        # Define split params based on card type
        if cardType == 'LEADER':
            cardCostSplit = cardCost.split('Life')
            cardCost = cardCostSplit[1]
        else:
            cardCostSplit = cardCost.split('Cost')
            cardCost = cardCostSplit[1]

        cardAttribute = card.findNext("div", attrs={"class":"attribute"}).findNext("i").text

        # Start split hell because they're allergic to adding an extra div for the content smh
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

        # Build card model
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

        # append to array/dictionary
        allCards.append(output)

    # Now we have the full data we collected and can do wtv we want with it
    print(output)


if __name__ == '__main__':
    get_all_cards()
