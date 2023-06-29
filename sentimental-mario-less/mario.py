def main():
    height = get_height()
    j = 1
    for i in range(height):
        print(" " * (height - i - 1), end="#" * (i + 1))
        print("")


def get_height():
    while True:
        try:
            height = int(input("Height: "))
            if height > 0 and height < 9:
                return height
        except ValueError:
            print("Choose a value between 1 and 8")


main()