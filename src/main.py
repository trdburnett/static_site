import textnode, os, shutil
from md2txt import extract_title    
def main():
    generate_public()
    dummynode = textnode.TextNode("some text", textnode.TextType.LINK, "https://www.boot.dev")
    print(dummynode)

def generate_public(source="./static",destination="./public", clean=True):
    #checks to see if destination directory exists and if a clean directory is required removes the directory 
    if clean and os.path.exists(destination):
        shutil.rmtree(destination)
    #checks to see if destination directory exists and if it does not, makes the destination directory
    if not os.path.exists(destination):
        os.makedirs(destination, exist_ok=True)
    #lists contents of source directory
    source_dir = os.listdir(source)
    #iterating over contents of source directory to add to destination directory
    for item in source_dir:
        if os.path.isfile(os.path.join(source, item)):
            #adds file to destination directory
            shutil.copy(os.path.join(source, item), destination)
        else:
            #runs a recursive call and adds directory to destination directory
            generate_public(os.path.join(source, item), os.path.join(destination, item), False)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    from_file = open(from_path)
    markdown = from_file.read()
    template_file = open(template_path)
    template = template_file.read()
    

main()
