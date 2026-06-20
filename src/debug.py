from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
print(TextType.__members__)
text_types = []
for k,v in TextType.__members__:
    text_types.append(k)
print(text_types)
