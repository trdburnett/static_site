from htmlnode import HTMLNode, LeafNode, ParentNode
child_node = LeafNode("span", "child")
parent_node = ParentNode("div", [child_node])
print(parent_node.children)
print(parent_node.to_html())