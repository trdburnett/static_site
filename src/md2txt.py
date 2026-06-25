import re
from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiter_count = 0
            if len(delimiter) > 2:
                raise Exception("Invalid Delimiter")
            if len(delimiter) == 2:
                check_next_char = False
                for char in node.text:
                    if check_next_char:
                        if char == delimiter[1]:
                            delimiter_count +=1
                        check_next_char = False
                    if not check_next_char: 
                        if char == delimiter[0]:
                            check_next_char = True
            if len(delimiter) == 1:        
                for char in node.text:
                    if char == delimiter:
                        delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception("Invalid Markdown Syntax")
            elif delimiter_count == 0:
                raise Exception("Delimiter not found")
            else:
                text = node.text.split(delimiter,maxsplit=(delimiter_count))
                for i in range(0,len(text)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_images(node.text)
            if extracted == []:
                if node.text != "":
                    new_nodes.append(node)
            else:
                split_text = node.text.split("!")
                for item in split_text:
                    if ")" in item:
                        split_item = item.split(")")
                        for item in split_item:
                            if item != "" and not "[" in item:
                                    new_nodes.append(TextNode(item, TextType.TEXT))
                            else:
                                for info in extracted:
                                    if info[0] in item and info[1] in item:
                                        new_nodes.append(TextNode(info[0], TextType.IMAGE, info[1]))                            
                    else:
                        new_nodes.append(TextNode(item, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_links(node.text)
            if extracted == []:
                if node.text != "":
                    new_nodes.append(node)
            else:
                split_text = node.text.split("[")
                for item in split_text:
                    if ")" in item:
                        split_item = item.split(")")
                        for item in split_item:
                            if item != "" and not "]" in item:
                                new_nodes.append(TextNode(item, TextType.TEXT))
                            else:
                                for info in extracted:
                                    if info[0] in item and info[1] in item:
                                        new_nodes.append(TextNode(info[0], TextType.LINK, info[1]))
                    else:
                        new_nodes.append(TextNode(item, TextType.TEXT))
    return new_nodes            

def text_to_textnodes(text: str) -> list[TextNode]:
    check_for_bold = split_nodes_delimiter([TextNode("text", TextType.TEXT)], "**", TextType.BOLD)
    print(check_for_bold)

text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")