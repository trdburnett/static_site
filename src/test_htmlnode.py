import unittest
from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()
