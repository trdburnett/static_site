from htmlnode import HTMLNode, ParentNode
from md2txt import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
def markdown_to_html(markdown: str) -> HTMLNode:
    #splitting markdown in to blocks
    blocks = markdown_to_blocks(markdown)
    children_to_master_node = []
    for block in blocks:
        block_children = []
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.HEADING:
            tag = find_heading_tag(block)
            inline_text = block.lstrip(strip_by_h_tag(tag))
            children_to_master_node.append(ParentNode(tag,text_to_nodes_to_children(inline_text)))
        if blocktype == BlockType.PARAGRAPH:
            tag = "p"
            new_lines_to_spaces = block.replace("\n"," ")
            children_to_master_node.append(ParentNode(tag,text_to_nodes_to_children(new_lines_to_spaces)))
        if blocktype == BlockType.CODE:
            code_block = block.lstrip("```\n")
            code_block = code_block.rstrip("```")
            node = TextNode(code_block, TextType.CODE)
            block_children.append(text_node_to_html_node(node))
            children_to_master_node.append(ParentNode("pre",block_children))
        if blocktype == BlockType.QUOTE:
            tag = "blockquote"
            inline_text = block.lstrip("> ")
            children_to_master_node.append(ParentNode(tag,text_to_nodes_to_children(inline_text)))
        if blocktype == BlockType.UNORDERED_LIST:
            list_children = []
            outer_tag = "ul"
            inner_tag = "li"
            list_of_items = block.split("\n")
            clean_list_of_items = []
            for item in list_of_items:
                clean_list_of_items.append(item.lstrip("- "))
            for item in clean_list_of_items:
                list_children.append(ParentNode(inner_tag, text_to_nodes_to_children(item)))
            children_to_master_node.append(ParentNode(outer_tag, list_children))
        if blocktype == BlockType.ORDERED_LIST:
            list_children = []
            outer_tag = "ol"
            inner_tag = "li"
            list_of_items = block.split("\n")
            clean_list_of_items = []
            for i in range(len(list_of_items)):
                to_strip = str(i+1) + ". "
                clean_list_of_items.append(list_of_items[i].lstrip(to_strip))
            for item in clean_list_of_items:
                text_nodes = text_to_textnodes(item)
                inner_children = []
                for node in text_nodes:
                    inner_children.append(text_node_to_html_node(node))
                list_children.append(ParentNode(inner_tag, inner_children))
            children_to_master_node.append(ParentNode(outer_tag, list_children))
    return ParentNode("div", children_to_master_node)


def find_heading_tag(block: str) -> str:
    if block.startswith("######"):
        return "h6"
    if block.startswith("#####"):
        return "h5"
    if block.startswith("####"):
        return "h4"
    if block.startswith("###"):
        return "h3"
    if block.startswith("##"):
        return "h2"
    if block.startswith("#"):
        return "h1"

#returns what to lstrip from the start of a heading block by tag    
def strip_by_h_tag(tag: str) -> str:
    if tag == "h1":
        return("# ")
    if tag == "h2":
        return("## ")
    if tag == "h3":
        return("### ")
    if tag == "h4":
        return("#### ")
    if tag == "h5":
        return("##### ")
    if tag == "h6":
        return("###### ")
    
def text_to_nodes_to_children(text: str) -> list:
    children = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children