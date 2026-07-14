import textnode, os, shutil, sys
from md2txt import extract_title
from md2html import markdown_to_html
from htmlnode import HTMLNode    

#get the base path. IMPORTANT sys.argv[1] is the first CLI argument NOT sys.argv[0] which is the script itself
def get_base_path():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return "/"

def main():
    base_path = get_base_path()
    generate_public()
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages("./content","./template.html","./docs", base_path)

def generate_public(source="./static",destination="./docs", clean=True):
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

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path}, to {dest_path} using {template_path}")
    #opens file from path
    from_file = open(from_path)
    #reads from the open file assigned to from_file and copies the contents to the variable markdown
    markdown = from_file.read()
    #closes the open file assigne to from_file
    from_file.close()
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    content = markdown_to_html(markdown)
    content_html = content.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content_html)
    template = template.replace("href=\"/", f"href=\"{base_path}")
    template = template.replace("src=\"/", f"src=\"{base_path}")
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    if not os.path.isfile(dest_path):
        dest_file = open(dest_path, 'x')
        dest_file.close()
    dest_file = open(dest_path, 'w')
    dest_file.write(template)
    dest_file.close()

def generate_pages(dir_path_content, template_path, dest_dir_path, base_path):
    content_list = os.listdir(dir_path_content)
    for content in content_list:
        if os.path.isfile(os.path.join(dir_path_content, content)):
            #print(os.path.join(dir_path_content, content))
            from_path = os.path.join(dir_path_content, content)
            root, ext = os.path.splitext(content)
            new_content = root + ".html"
            dest_path = os.path.join(dest_dir_path, new_content)
            generate_page(from_path, template_path, dest_path, base_path)
        else:
            generate_pages(os.path.join(dir_path_content, content), template_path, os.path.join(dest_dir_path, content), base_path)

main()
