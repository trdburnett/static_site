from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
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
                print("length of delimiter is 2")
                check_next_char = False
                for char in node.text:
                    if check_next_char:
                        if char == delimiter[1]:
                            delimiter_count +=1
                            print("found second half of delimiter")
                        check_next_char = False
                        print("set check next char to false")
                    if not check_next_char: 
                        if char == delimiter[0]:
                            check_next_char = True
                            print("found first half of delimiter")
            if len(delimiter) == 1:
                print("length of delimiter is 1")        
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

old_nodes = [TextNode("This is text with a *bold** word", TextType.BOLD)]
delimiter = "**"
text_type = TextType.BOLD
new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
print(new_nodes)

