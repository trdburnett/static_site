import textnode, os, shutil
def main():
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public(source,destination):
    #checks if the given path exists
    print(f"{destination} exists: {os.path.exists(destination)}")
    #checks to see if destination directory exists if it does, the directory is removed and remade 
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)
    print(f"{destination} exists: {os.path.exists(destination)}")
    #lists contents of source directory
    source_dir = os.listdir(source)
    for item in source_dir:
        if "." in item:
            #adds file to destination directory
            shutil.copy(f"{source}/{item}", destination)
        else:
            #runs a recursive call and adds directory to destination directory
            generate_public(f"{source}/{item}", f"{destination}/{item}")
    public = os.listdir(destination)
    print(public)


generate_public("./static","./public")
main()
