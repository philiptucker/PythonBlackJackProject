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


def pointCheck(playerHand, dealerHand, money, betAmount):
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
        money += betAmount
    else:
        print("Sorry. You lose.")
        money -= betAmount
    db.saveMoney(money)
    print(f"Money: {money}")


def main():
    print("BlackJack Program\nBlackjack payout is 3:2")

    deck = deckBuild()
    keepGoing = 'y'
    random.shuffle(deck)

    while keepGoing.lower() == 'y':
        dealerHand = []
        playerHand = []
        money = Decimal(db.loadMoney())
        money = money.quantize(Decimal("1.00"), ROUND_HALF_UP)
        print(f"Money: {money}")
        betAmount = betAccept(money)

        print("\nDEALER'S SHOW CARD:")
        dealCard = deck.pop(0)
        dealerHand.append(dealCard)
        dealCard = deck.pop(0)
        dealerHand.append(dealCard)
        card = dealerHand[0]
        print(f"{card[1]} of {card[0]}")

        print("\nYOUR CARDS:")
        dealCard = deck.pop(0)
        playerHand.append(dealCard)
        dealCard = deck.pop(0)
        playerHand.append(dealCard)
        for card in playerHand:
            print(f"{card[1]} of {card[0]}")

        pointCheck(playerHand, dealerHand, money, betAmount)

        keepGoing = input("\nPlay again? (y/n): \t")

    print("\nCome back soon!\nBye!")


if __name__ == '__main__':
    main()
