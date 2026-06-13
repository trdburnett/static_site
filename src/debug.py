from htmlnode import HTMLNode, LeafNode
testnode = LeafNode("p", "Hello, world!")
print(testnode.tag)
print(testnode.value)