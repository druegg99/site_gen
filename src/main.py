from textnode import *

#print("hello world")
def main():
    #text = TextNode("Some text", TextType.LINK, "httpsomethingsomething")
    #print(text)
    lines = "this *is a test*".split("*")
    for line in lines:
        print(line + ".")

main()
