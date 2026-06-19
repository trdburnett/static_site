from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
node = TextNode("This is a faulty text node", TextType.INVALID)
print(node.text_type)
print(str(node.text_type))