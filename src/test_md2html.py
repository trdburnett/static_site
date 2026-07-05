import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from md2html import markdown_to_html
class TestHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_heading(self):
        md = """
# This is a **h1** heading

## This is a _h2_ heading

### This is a h3 heading

#### This is a h4 heading

##### This is a h5 heading

###### This is a h6 heading
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>h1</b> heading</h1><h2>This is a <i>h2</i> heading</h2><h3>This is a h3 heading</h3><h4>This is a h4 heading</h4><h5>This is a h5 heading</h5><h6>This is a h6 heading</h6></div>"
        )

    def test_blockquote(self):
        md = """
> This is a **blockquote** 
"""
        node = markdown_to_html(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>blockquote</b></blockquote></div>"
        )

if __name__ == "__main__":
    unittest.main()