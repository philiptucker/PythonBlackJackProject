import db
from decimal import Decimal
from decimal import ROUND_HALF_UP


def deckBuild():
    # deck of cards [Suit, Rank, point value]
    deck = [
        ["Hearts\u2665", 2, 2],
        ["Hearts\u2665", 3, 3],
        ["Hearts\u2665", 4, 4],
        ["Hearts\u2665", 5, 5],
        ["Hearts\u2665", 6, 6],
        ["Hearts\u2665", 7, 7],
        ["Hearts\u2665", 8, 8],
        ["Hearts\u2665", 9, 9],
        ["Hearts\u2665", 10, 10],
        ["Hearts\u2665", "Jack", 10],
        ["Hearts\u2665", "Queen", 10],
        ["Hearts\u2665", "King", 10],
        ["Hearts\u2665", "Ace", 11],

        ["Diamonds\u2666", 2, 2],
        ["Diamonds\u2666", 3, 3],
        ["Diamonds\u2666", 4, 4],
        ["Diamonds\u2666", 5, 5],
        ["Diamonds\u2666", 6, 6],
        ["Diamonds\u2666", 7, 7],
        ["Diamonds\u2666", 8, 8],
        ["Diamonds\u2666", 9, 9],
        ["Diamonds\u2666", 10, 10],
        ["Diamonds\u2666", "Jack", 10],
        ["Diamonds\u2666", "Queen", 10],
        ["Diamonds\u2666", "King", 10],
        ["Diamonds\u2666", "Ace", 11],

        ["Spades\u2660", 2, 2],
        ["Spades\u2660", 3, 3],
        ["Spades\u2660", 4, 4],
        ["Spades\u2660", 5, 5],
        ["Spades\u2660", 6, 6],
        ["Spades\u2660", 7, 7],
        ["Spades\u2660", 8, 8],
        ["Spades\u2660", 9, 9],
        ["Spades\u2660", 10, 10],
        ["Spades\u2660", "Jack", 10],
        ["Spades\u2660", "Queen", 10],
        ["Spades\u2660", "King", 10],
        ["Spades\u2660", "Ace", 11],

        ["Clubs\u2663", 2, 2],
        ["Clubs\u2663", 3, 3],
        ["Clubs\u2663", 4, 4],
        ["Clubs\u2663", 5, 5],
        ["Clubs\u2663", 6, 6],
        ["Clubs\u2663", 7, 7],
        ["Clubs\u2663", 8, 8],
        ["Clubs\u2663", 9, 9],
        ["Clubs\u2663", 10, 10],
        ["Clubs\u2663", "Jack", 10],
        ["Clubs\u2663", "Queen", 10],
        ["Clubs\u2663", "King", 10],
        ["Clubs\u2663", "Ace", 11]
    ]
    return deck


def startDeal(deck, dealerHand, playerHand):
    print("\nDEALER'S SHOW CARD:")
    dealCard = deck.pop(0)
    dealerPoints = dealCard[2]
    dealerHand.append(dealCard)

    dealCard = deck.pop(0)
    if dealCard[2] == 11 and dealerPoints > 10:
        dealCard.pop(2)
        dealCard.append(1)
    dealerHand.append(dealCard)

    dealerCard = dealerHand[0]
    print(f"{dealerCard[1]} of {dealerCard[0]}")

    print("\nYOUR CARDS:")
    playerPoints = 0

    dealCard = deck.pop(0)
    print(f"{dealCard[1]} of {dealCard[0]}")
    aceCheck(dealCard, playerPoints)
    playerPoints += dealCard[2]
    playerHand.append(dealCard)

    dealCard = deck.pop(0)
    print(f"{dealCard[1]} of {dealCard[0]}")
    aceCheck(dealCard, playerPoints)
    playerPoints += dealCard[2]
    playerHand.append(dealCard)


def hitStand(deck, playerHand):
    playerPoints = 0
    for card in playerHand:
        playerPoints += card[2]
    while playerPoints < 21:
        draw = input("\nHit or stand? (hit/stand): ")
        if draw.lower() == "hit":
            playerPoints = 0
            dealCard = deck.pop(0)
            print("\nYOUR CARDS:")
            for card in playerHand:
                print(f"{card[1]} of {card[0]}")
                playerPoints += card[2]
            print(f"{dealCard[1]} of {dealCard[0]}")

            aceCheck(dealCard, playerPoints)
            playerPoints += dealCard[2]
            playerHand.append(dealCard)

            if playerPoints > 21:
                print("BUST!")

        elif draw.lower() == "stand":
            break
        else:
            print("Invalid response. Please try again.")


def dealerHitStand(deck, dealerHand, playerHand):
    print("\nDEALER'S CARDS:")
    dealerPoints = 0
    playerPoints = 0
    for card in dealerHand:
        print(f"{card[1]} of {card[0]}")
        dealerPoints += card[2]
    for card in playerHand:
        playerPoints += card[2]

    while dealerPoints < 17 and playerPoints <= 21:
        print("\nDealer Hits")
        dealCard = deck.pop(0)
        if dealCard[2] == 11 and dealerPoints > 10:
            dealCard.pop(2)
            dealCard.append(1)
        dealerPoints += dealCard[2]
        dealerHand.append(dealCard)
        print("\nDEALER'S CARDS:")
        for card in dealerHand:
            print(f"{card[1]} of {card[0]}")
        if dealerPoints > 21:
            print("DEALER BUST!")


def aceCheck(dealCard, playerPoints):
    if dealCard[2] == 11 and playerPoints > 10:
        dealCard.pop(2)
        dealCard.append(1)
        print("Ace will be treated as a 1")
    elif dealCard[2] == 11:
        choice = int(input("Would you like this Ace to be a 1 or an 11? "))
        while choice != 1 and choice != 11:
            print("Must select 1 or 11. Please try again")
            choice = int(input("Would you like this to be a 1 or an 11? "))
        if choice == 1:
            dealCard.pop(2)
            dealCard.append(1)
            print("Ace will be treated as a 1")
        else:
            print("Ace will be treated as an 11")


def playerBlackJack(playerHand):
    playerPoints = 0
    for card in playerHand:
        playerPoints += card[2]
    if playerPoints == 21:
        print("PLAYER'S BLACKJACK!")
        return True
    else:
        return False


def dealerBlackJack(dealerHand):
    dealerCard = dealerHand[0]
    if dealerCard[2] >= 10:
        dealerPoints = 0
        for card in dealerHand:
            dealerPoints += card[2]
        if dealerPoints == 21:
            print("\nDEALER'S CARDS:")
            for card in dealerHand:
                print(f"{card[1]} of {card[0]}")
            print("DEALER'S BLACKJACK!")
            return True
        else:
            return False
    else:
        return False


def blackJackPointCheck(playerHand, dealerHand, money, betAmount):
    playerPoints = 0
    dealerPoints = 0
    for card in playerHand:
        playerPoints += card[2]
    for card in dealerHand:
        dealerPoints += card[2]
    print(f"\nYOUR POINTS: \t\t{playerPoints}"
          f"\nDEALER'S POINTS: \t{dealerPoints}\n")

    if playerPoints > dealerPoints:
        print("Congrats, you win!")
        money += betAmount * Decimal(1.5)
        money = money.quantize(Decimal("1.00"), ROUND_HALF_UP)
    elif playerPoints == dealerPoints:
        print("Tie game. Return bet.")
    else:
        print("Sorry. You lose.")
        money -= betAmount
    db.saveMoney(money)
    print(f"Money: {money}")


def pointCheck(playerHand, dealerHand, money, betAmount):
    playerPoints = 0
    dealerPoints = 0
    for card in playerHand:
        playerPoints += card[2]
    for card in dealerHand:
        dealerPoints += card[2]
    print(f"\nYOUR POINTS: \t\t{playerPoints}"
          f"\nDEALER'S POINTS: \t{dealerPoints}\n")

    if (dealerPoints > 21) or (playerPoints > dealerPoints and playerPoints <= 21):
        print("Congrats, you win!")
        money += betAmount
    elif playerPoints == dealerPoints:
        print("Tie game. Return bet.")
    else:
        print("Sorry. You lose.")
        money -= betAmount
    db.saveMoney(money)
    print(f"Money: {money}")
