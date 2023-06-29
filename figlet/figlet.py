from pyfiglet import Figlet
from sys import argv, exit
import random

figlet = Figlet()
figlet.getFonts()

if len(argv) == 1:
    RandomFont = True
elif len(argv) == 3 and (argv[1] == '-f' or argv[1] == '--font'):
    RandomFont = False
else:
    print("Invalid usage")
    exit(1)

text = input("Input: ")

if RandomFont == False:
    try:
        figlet.setFont(font=argv[2])
    except:
        print("Invalid usage")
        exit(1)
if RandomFont == True:
    PickRandomFont = random.choice(figlet.getFonts())
    figlet.setFont(font=PickRandomFont)
print("Output: ")
print(figlet.renderText(text))