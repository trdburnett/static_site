from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
node = TextNode("This is a link node", TextType.LINK, url="www.google.co.uk")
print(node)
html_node = LeafNode(tag="a", value="This is a link node", props={"href": "www.google.co.uk"})
print(html_node)
