import textnode, os, shutil
def main():
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public():
    print(os.path.exists("./public"))
    shutil.rmtree("./public")
    print(os.path.exists("./public"))

generate_public()
main()
