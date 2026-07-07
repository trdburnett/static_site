import textnode, os, shutil
def main():
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public():
    #checks if the given path exists
    print(os.path.exists("./public"))
    #removes given directory
    shutil.rmtree("./public")
    print(os.path.exists("./public"))
    #makes given directory
    os.mkdir("./public")
    print(os.path.exists("./public"))
    #lists contents of static directory
    static = os.listdir("./static")
    for item in static:
        if "." in item:
            print("found a file")
        else:
            print("found a directory")


generate_public()
main()
