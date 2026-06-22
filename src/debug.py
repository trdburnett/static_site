from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
text = "This is text with a *bold** word"
delimiter = "**"
delimiter_count = 0
print(delimiter[0])
print(delimiter[1])
if len(delimiter) == 2:
    check_next_char = False
    for char in text:
        if not check_next_char: 
            if char == delimiter[0]:
                check_next_char = True
                print("Found first half of delimiter")
            if check_next_char:
                if char == delimiter[1]:
                    print("Found second hald of delimiter")
                    delimiter_count +=1
                print("setting check next char to false")    
                check_next_char = False
print(delimiter_count)
if len(delimiter) == 1:        
    for char in text:
        if char == delimiter:
            delimiter_count += 1
print(delimiter_count)
if delimiter_count % 2 != 0:
    print("Hi!")
