import textnode, os, shutil
def main():
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public(source,destination):
    #checks if the given path exists
    print(f"{destination}exists: {os.path.exists(destination)}")
    #removes given directory
    shutil.rmtree(destination)
    print(os.path.exists(destination))
    #makes given directory
    os.mkdir(destination)
    print(os.path.exists(destination))
    #lists contents of static directory
    static = os.listdir(source)
    for item in static:
        if "." in item:
            #adds file to given directory
            shutil.copy(f"{source}/{item}", destination)
        else:
            generate_public(f"{source}/{item}", f"{destination}/{item}")
    public = os.listdir(destination)
    print(public)


generate_public("./static","./public")
main()
