from cs50 import get_float
quarters = dimes = nickels = pennies = 0


while True:
    try:
        cents = get_float("Select amount of cents: ")
        if cents > 0:
            break
    except ValueError:
        print("> 0")

cents = round(cents * 100)


while cents >= 25:
    cents -= 25
    quarters += 1


while cents >= 10:
    cents -= 10
    dimes += 1


while cents >= 5:
    cents -= 5
    nickels += 1

while cents >= 1:
    cents -= 5
    pennies += 1


coins = quarters + dimes + nickels + pennies
print("Change owed:", coins)

