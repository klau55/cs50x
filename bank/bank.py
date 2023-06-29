answer = input("Greeting: ")
answer = answer.lower()
if "hello" in answer:
    print("$0")
elif "h" in answer[0]:
    print("$20")
else:
    print("$100")