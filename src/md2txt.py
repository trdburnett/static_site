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
    alt_text = re.findall(r"!\[\w+\]",text)
    url = re.findall(r"\(https:\/\/.*?\)",text)
    print(alt_text)
    print(url)

extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")