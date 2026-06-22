import unittest
from textnode import TextNode, TextType
from md2txt import split_nodes_delimiter

class Testmd2txt(unittest.TestCase):
    def test_empty_list(self):
        old_nodes = []
        delimiter = "`"
        text_type = TextType.CODE
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)

    def test_odd_delimiter(self):
        old_nodes = [TextNode("This is text with a `code block word", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)

    def test_no_delimiter_found(self):
        old_nodes = [TextNode("This is text with a code block word", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)

    def test_code_valid_1_item(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT)])
    
    def test_code_valid_2_items_1_with_2_blocks(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT),
                     TextNode("This is text with a `code block` here and a `code block` there", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),
                                     TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" here and a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" there", TextType.TEXT)])
        
    def test_code_2_items_1_valid_1_already_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT),
                             TextNode("`print(\"Hello World!\")`", TextType.CODE)]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" word", TextType.TEXT),
                                     TextNode("`print(\"Hello World!\")`", TextType.CODE)])
        
    def test_bold_valid_1_item(self):
        old_nodes = [TextNode("This is text with a **bold** word", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("bold", TextType.BOLD),
                                     TextNode(" word", TextType.TEXT)])
        
    def test_italic_valid_1_item(self):
        old_nodes = [TextNode("This is text with an _italic_ word", TextType.TEXT)]
        delimiter = "_"
        text_type = TextType.ITALIC
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("This is text with an ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word", TextType.TEXT)])

if __name__ == "__main__":
    unittest.main()