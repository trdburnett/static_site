import textnode, os, shutil
def main():
    generate_public()
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public(source="./static",destination="./public"):
    #checks if the given path exists
    print(f"{destination} exists: {os.path.exists(destination)}")
    #checks to see if destination directory exists if it does it is removed 
    if os.path.exists(destination):
        shutil.rmtree(destination)
    #makes destination directory
    os.mkdir(destination)
    print(f"{destination} exists: {os.path.exists(destination)}")
    #lists contents of source directory
    source_dir = os.listdir(source)
    #iterating over contents of source directory to add to destination directory
    for item in source_dir:
        if "." in item:
            #adds file to destination directory
            shutil.copy(f"{source}/{item}", destination)
        else:
            #runs a recursive call and adds directory to destination directory
            generate_public(f"{source}/{item}", f"{destination}/{item}")
    #performs a check to see if the files and directories in the source and destination directories match
    #raises an error if they do not match
    if os.listdir(source) != os.listdir(destination):
        raise Exception("Generation Error")

main()
