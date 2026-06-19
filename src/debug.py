from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
text_types = []
for member, value in TextType:
    text_types.append(member)
print(text_types)