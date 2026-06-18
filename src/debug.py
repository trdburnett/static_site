from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
node = TextNode("This is a text node", TextType.TEXT)
html_node = text_node_to_html_node(node)
print(node.text_type)
#print(html_node)