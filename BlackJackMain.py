import db
from decimal import Decimal
from decimal import ROUND_HALF_UP


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


def main():
    print("BlackJack Program\nBlackjack payout is 3:2")
    money = Decimal(db.loadMoney())
    money = money.quantize(Decimal("1.00"), ROUND_HALF_UP)
    print(f"Money: {money}")
    deck = deckBuild()
    dealerHand = []
    playerHand = []
    keepGoing = 'y'

    while keepGoing.lower() == 'y':
        while True:
            try:
                betAmount = round(float(input("Bet amount: \t")), 2)
                break
            except ValueError:
                print("Bet amount must be an integer or float value please try again.")

        betAmount = Decimal(betAmount)
        betAmount = betAmount.quantize(Decimal("1.00"))
        print(f"{betAmount}")

        keepGoing = input("\nPlay again? (y/n): \t")

    print("\nCome back soon!\nBye!")


if __name__ == '__main__':
    main()
