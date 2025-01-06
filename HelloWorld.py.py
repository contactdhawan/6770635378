print('Hello World!')
print('What is your name?')
person = input()
print('Hello,', person)
print("How are you? Tell me if you are sad, angry, happy, or fine. Type your answer below. Anything that starts with the letter of any of the words you are asked to type will work.")
feelings = input()
if feelings.lower() == 'sad' or feelings.lower() == 'angry' or feelings[:1].lower() == 's' or feelings[:1].lower() == 'a':
    print('I hope you feel better soon. Would you like a link to a reading website called Libby so you can read a little bit?')
    libbyLink = input()
    if libbyLink[:1].lower() == "y":
        print ('Here is your Libby link. https://libbyapp.com/   Would you like a few author reccomandations?')
        authorIntereset = input()
        if authorIntereset[:1].lower() == "y":
            print('A few good authors are J.K. Rowling, Kate DiCammilo, Jeff Kinney, and Tui T. Sutherland')
        else:
            print("Have a good day!!!")
    else:
        print ("Have a good day!!")
elif feelings[:1].lower() == "h" or feelings[:1].lower() == "f":
    print('Glad to hear about it!')
else:
    print ('Please respond with one of the options obove or restart the project')
