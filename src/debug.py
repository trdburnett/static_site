from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
text_types = []
for text_type in TextType:
    text_types.append(text_type)
print(text_types)