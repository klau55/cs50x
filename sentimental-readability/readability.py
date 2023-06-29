

def main():
    text = input("Text:")
    L = float(count_letters(text)) / float(count_words(text)) * 100
    S = float(count_sentenses(text)) / float(count_words(text)) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print("Grade:", index)


def count_letters(text):
    letters = 0
    for i in text:
        if i.isalpha():
            letters += 1
    return letters


def count_words(text):
    words = 1  # BECAUSE I NEED TO OUNT LAST WORD
    for i in text:
        if i == ' ':
            words += 1
    return words


def count_sentenses(text):
    sentenses = 0
    for i in text:
        if i == "." or i == "!" or i == "?":
            sentenses += 1
    return sentenses


main()