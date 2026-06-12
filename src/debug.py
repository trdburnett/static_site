from htmlnode import HTMLNode
testnode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
print(testnode.props_to_html())