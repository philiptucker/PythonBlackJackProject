import db
import random
import BlackJackRules as BJR
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


def main():
    print("BlackJack Program\nBlackjack payout is 3:2")

    deck = BJR.deckBuild()
    random.shuffle(deck)

    keepGoing = 'y'
    while keepGoing.lower() == 'y':
        if len(deck) < 26:
            print("\nDeck running low, reloading deck.")
            deck = BJR.deckBuild()
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

        BJR.startDeal(deck, dealerHand, playerHand)

        if BJR.playerBlackJack(playerHand) is False \
                and BJR.dealerBlackJack(dealerHand) is False:

            BJR.hitStand(deck, playerHand)
            BJR.dealerHitStand(deck, dealerHand, playerHand)
            BJR.pointCheck(playerHand, dealerHand, money, betAmount)
        else:
            BJR.blackJackPointCheck(playerHand, dealerHand, money, betAmount)

        keepGoing = input("\nPlay again? (y/n): \t")
        while keepGoing != 'y' and keepGoing != 'n':
            print("Invalid entry, try again.")
            keepGoing = input("\nPlay again? (y/n): \t")

    print("\nCome back soon!\nBye!")


if __name__ == '__main__':
    main()
