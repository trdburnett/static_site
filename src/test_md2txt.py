import unittest
from textnode import TextNode, TextType
from md2txt import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type

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

    def test_bold_odd_delimiter(self):
        old_nodes = [TextNode("This is text with a *bold** word", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)

    def test_no_delimiter_found(self):
        old_nodes = [TextNode("This is text with a code block word", TextType.TEXT)]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, old_nodes)

    def test_invalid_delimiter(self):
        old_nodes = [TextNode("This is text with an ```invalid demiliter```", TextType.TEXT)]
        delimiter = "```"
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
        
    def test_code_1_item_already_code(self):
        old_nodes = [TextNode("`print(\"Hello World!\")`", TextType.CODE)]
        delimiter = "`"
        text_type = TextType.CODE
        new_nodes = split_nodes_delimiter(old_nodes,delimiter,text_type)
        self.assertEqual(new_nodes, [TextNode("`print(\"Hello World!\")`", TextType.CODE)])
        
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
        
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_images_missing_punctuation_1(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_images_missing_punctuation_2(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_links_missing_punctuation_1(self):
        text = "This is text with a link to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_links_missing_punctuation_2(self):
        text = "This is text with a link to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_split_nodes_image(self):
        old_nodes = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT),
                                     TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                                     TextNode(" and ", TextType.TEXT),
                                     TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_split_nodes_image_missing_puntuation_1_missing_explanation_mark(self):
        old_nodes = [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT),
                                     TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_split_nodes_image_missing_puntuation_2_both_missing_explanation_mark(self):
        old_nodes = [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_image_missing_puntuation_3_1_missing_explanation_mark_1_missing_closing_bracket(self):
        old_nodes = [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_image_missing_puntuation_4_first_missing_explanation_mark_second_missing_closing_bracket_1_correct(self):
        old_nodes = [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg and another ![third image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg and another ", TextType.TEXT),
                                     TextNode("third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")])

    def test_split_nodes_image_2_node_list_1_already_image_node_1_valid(self):
        old_nodes = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                     TextNode("This is text with an ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                                     TextNode("This is text with an ", TextType.TEXT),
                                     TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_split_nodes_image_1_missing_opening_square_bracket(self):
        old_nodes = [TextNode("This is text with a !rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a !rick roll](https://i.imgur.com/aKaOqIh.gif) and ", TextType.TEXT),
                                     TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")])
        
    def test_split_nodes_link(self):
        old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a link ", TextType.TEXT),
                                     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                                     TextNode(" and ", TextType.TEXT),
                                     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        
    def test_split_nodes_link_1_missing_opening_square_bracket(self):
        old_nodes = [TextNode("This is text with a link to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a link to boot dev](https://www.boot.dev) and ", TextType.TEXT),
                                     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        
    def test_split_nodes_link_1_missing_opening_and_closing_square_bracket(self):
        old_nodes = [TextNode("This is text with a link to boot dev(https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("This is text with a link to boot dev(https://www.boot.dev) and ", TextType.TEXT),
                                     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        
    def test_split_nodes_link_2_missing_opening_square_bracket(self):
        old_nodes = [TextNode("This is text with a link to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_link_1_node_already_link_node_1_valid(self):
        old_nodes = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                                     TextNode(" and ", TextType.TEXT),
                                     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")])
        
    def test_split_nodes_link_empty_list(self):
        old_nodes = []
        with self.assertRaises(Exception):
            new_nodes = split_nodes_link(old_nodes)

    def test_text_to_textnodes_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT),
                                     TextNode("text", TextType.BOLD),
                                     TextNode(" with an ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word and a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" and an ", TextType.TEXT),
                                     TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                     TextNode(" and a ", TextType.TEXT),
                                     TextNode("link", TextType.LINK, "https://boot.dev")])
    
    def test_text_to_textnode_missing_bold(self):
        text = "This is  with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [TextNode("This is  with an ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word and a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" and an ", TextType.TEXT),
                                     TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                     TextNode(" and a ", TextType.TEXT),
                                     TextNode("link", TextType.LINK, "https://boot.dev")])
        
    def test_text_to_textnodes_missing_image(self):
        text = "This is **text** with an _italic_ word and a `code block` and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, [TextNode("This is ", TextType.TEXT),
                                     TextNode("text", TextType.BOLD),
                                     TextNode(" with an ", TextType.TEXT),
                                     TextNode("italic", TextType.ITALIC),
                                     TextNode(" word and a ", TextType.TEXT),
                                     TextNode("code block", TextType.CODE),
                                     TextNode(" and a ", TextType.TEXT),
                                     TextNode("link", TextType.LINK, "https://boot.dev")])
        
    def test_markdown_to_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# This is a heading",
                                  "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                                  "- This is the first list item in a list block\n- This is a list item\n- This is another list item"])
    
    def test_markdown_to_blocks_added_whitespace_and_newlines(self):
        md = """# This is a heading   

   This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

                   
- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["# This is a heading",
                                  "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                                  "- This is the first list item in a list block\n- This is a list item\n- This is another list item"])

    def test_block_to_block_type_empty_string(self):
        md = ""
        with self.assertRaises(Exception):
            blocktype = block_to_block_type(md)
    
    def test_block_to_block_type_heading_1(self):
        md = "# This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)
    
    def test_block_to_block_type_heading_2(self):
        md = "## This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)    

    def test_block_to_block_type_heading_3(self):
        md = "### This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading_4(self):
        md = "#### This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading_5(self):
        md = "##### This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_heading_6(self):
        md = "###### This is a heading"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING)

    def test_block_to_block_type_code(self):
        md = "```\n This is a code block \n This is the second line in the code block```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = "> This is a quote block\n> Here is the second quote\n> Here is the third"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE)

    def test_block_to_block_type_quote_but_its_a_paragraph(self):
        md = "> This is a quote block\n Here is the second quote\n> Here is the third"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        md = "- This is an unordered list\n- This is the second list entry\n- This is the third"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_list_but_its_a_paragraph(self):
        md = "- This is an unordered list\n-This is the second list entry\n- This is the third"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        md = "1. This is and ordered list\n2. This is the second entry\n3. This is the third"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()