import textnode
def main():
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

main()
