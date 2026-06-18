import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        testnode = HTMLNode()
        assert(testnode.props_to_html() == "")

    def test_props_to_html(self):
        testnode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert(testnode.props_to_html() == " href=\"https://www.google.com\" target=\"_blank\"")

    def test_repr(self):
        testnode = HTMLNode("p", "hello", None, {'class': 'primary'})
        expected = "HTML_Node(p, hello, children: None, {\'class\': \'primary\'})"
        self.assertEqual(repr(testnode), expected)

    def test_leaf_to_html_p(self):
        testnode = LeafNode("p", "Hello, world!")
        expected = "<p>Hello, world!</p>"
        self.assertEqual(testnode.to_html(), expected)

    def test_leaf_to_html_no_tag(self):
        testnode = LeafNode(None, "Hello, world!")
        expected = "Hello, world!"
        self.assertEqual(testnode.to_html(), expected)

    def test_leaf_to_html_no_value(self):
        testnode = LeafNode(None, None)
        with self.assertRaises(ValueError):
            testnode.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None,[child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_tag(self):
        parent_node = ParentNode("a", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_multiple_children(self):
        child_node = LeafNode("h1", "child")
        child_node2 = LeafNode("h2", "second child")
        parent_node = ParentNode("body" ,[child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<body><h1>child</h1><h2>second child</h2></body>"
        )

if __name__ == "__main__":
    unittest.main()
