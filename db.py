import sys


def loadMoney():
    try:
        with open("money.txt") as file:
            for line in file:
                line = line.replace("\n", "")
                money = line
            return money
    except FileNotFoundError:
        print("\nCould not find previous funds, here is a new wallet.")
        money = 100.00
        return money
    except Exception as e:
        print("\nAn unexpected error has occurred, closing Program.")
        print(type(e), e)
        sys.exit(1)


def saveMoney(money):
    with open("money.txt", "w") as file:
        file.write(f"{money}\n")
