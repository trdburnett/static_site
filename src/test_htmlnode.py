import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def props_to_html_test_empty(self):
        testnode = HTMLNode()
        assert(testnode.props_to_html == "")

    def props_to_html_test(self):
        testnode = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        assert(testnode.__repr__ == "href\"https://www.google.com\" target=\"_blank")

if __name__ == "__main__":
    unittest.main()
