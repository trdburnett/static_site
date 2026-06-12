import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        testnode = HTMLNode()
        assert(testnode.props_to_html() == "")

    def test_props_to_html(self):
        testnode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert(testnode.props_to_html() == "href=\"https://www.google.com\" target=\"_blank")

if __name__ == "__main__":
    unittest.main()
