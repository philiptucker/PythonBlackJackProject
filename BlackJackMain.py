import db
import random
from decimal import Decimal
from decimal import ROUND_HALF_UP


def betAccept(money):
    while True:
        try:
            betAmount = round(float(input("Bet amount: \t")), 2)
            if betAmount > money:
                print("Bet cannot be larger than current funds. Please try again")
            elif betAmount > 1000:
                print("Maximum bet is 1000. Please try again")
            elif betAmount < 5:
                print("Minimum bet is 5. Please try again")
            else:
                break
        except ValueError:
            print("Bet amount must be an integer or float value please try again.")

    betAmount = Decimal(betAmount)
    betAmount = betAmount.quantize(Decimal("1.00"))
    return betAmount


def deckBuild():
    # deck of cards [Suit, Rank, point value]
    deck = [
        ["Hearts", 2, 2],
        ["Hearts", 3, 3],
        ["Hearts", 4, 4],
        ["Hearts", 5, 5],
        ["Hearts", 6, 6],
        ["Hearts", 7, 7],
        ["Hearts", 8, 8],
        ["Hearts", 9, 9],
        ["Hearts", 10, 10],
        ["Hearts", "Jack", 10],
        ["Hearts", "Queen", 10],
        ["Hearts", "King", 10],
        ["Hearts", "Ace", 11],

        ["Diamonds", 2, 2],
        ["Diamonds", 3, 3],
        ["Diamonds", 4, 4],
        ["Diamonds", 5, 5],
        ["Diamonds", 6, 6],
        ["Diamonds", 7, 7],
        ["Diamonds", 8, 8],
        ["Diamonds", 9, 9],
        ["Diamonds", 10, 10],
        ["Diamonds", "Jack", 10],
        ["Diamonds", "Queen", 10],
        ["Diamonds", "King", 10],
        ["Diamonds", "Ace", 11],

        ["Spades", 2, 2],
        ["Spades", 3, 3],
        ["Spades", 4, 4],
        ["Spades", 5, 5],
        ["Spades", 6, 6],
        ["Spades", 7, 7],
        ["Spades", 8, 8],
        ["Spades", 9, 9],
        ["Spades", 10, 10],
        ["Spades", "Jack", 10],
        ["Spades", "Queen", 10],
        ["Spades", "King", 10],
        ["Spades", "Ace", 11],

        ["Clubs", 2, 2],
        ["Clubs", 3, 3],
        ["Clubs", 4, 4],
        ["Clubs", 5, 5],
        ["Clubs", 6, 6],
        ["Clubs", 7, 7],
        ["Clubs", 8, 8],
        ["Clubs", 9, 9],
        ["Clubs", 10, 10],
        ["Clubs", "Jack", 10],
        ["Clubs", "Queen", 10],
        ["Clubs", "King", 10],
        ["Clubs", "Ace", 11]
    ]
    return deck


def moneyCheck(money):
    if money < 5:
        print("Cannot afford minimum bet amount.")
        poor = input("Would you like more funds? (y/n): ")
        if poor.lower() != 'y':
            return True
        else:
            print("Here is a 100.00 loan.")
            money += Decimal(100.00)
            db.saveMoney(money)
            print(f"Money: {money}")


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


def main():
    print("BlackJack Program\nBlackjack payout is 3:2")

    deck = deckBuild()
    random.shuffle(deck)

    keepGoing = 'y'
    while keepGoing.lower() == 'y':
        if len(deck) < 26:
            print("\nDeck running low, reloading deck.")
            deck = deckBuild()
        random.shuffle(deck)

        dealerHand = []
        playerHand = []
        money = Decimal(db.loadMoney())
        money = money.quantize(Decimal("1.00"), ROUND_HALF_UP)
        print(f"\nMoney: {money}")
        poor = moneyCheck(money)
        if poor is True:
            break
        money = Decimal(db.loadMoney())
        money = money.quantize(Decimal("1.00"), ROUND_HALF_UP)
        betAmount = betAccept(money)

        startDeal(deck, dealerHand, playerHand)

        if playerBlackJack(playerHand) is False \
                and dealerBlackJack(dealerHand) is False:

            hitStand(deck, playerHand)
            dealerHitStand(deck, dealerHand, playerHand)
            pointCheck(playerHand, dealerHand, money, betAmount)
        else:
            blackJackPointCheck(playerHand, dealerHand, money, betAmount)

        keepGoing = input("\nPlay again? (y/n): \t")
        while keepGoing != 'y' and keepGoing != 'n':
            print("Invalid entry, try again.")
            keepGoing = input("\nPlay again? (y/n): \t")

    print("\nCome back soon!\nBye!")


if __name__ == '__main__':
    main()
