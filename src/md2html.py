from htmlnode import HTMLNode, ParentNode
from md2txt import markdown_to_blocks, block_to_block_type, BlockType, text_to_textnodes
from textnode import text_node_to_html_node
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
            text_nodes = text_to_textnodes(inline_text)
            for node in text_nodes:
                block_children.append(text_node_to_html_node(node))
            children_to_master_node.append(ParentNode(tag,block_children))
    #need to handle other block types only heading blocks handled so far
    return ParentNode("div", children_to_master_node)


def find_heading_tag(block: str) -> str:
    if block.startswith("#"):
        return "h1"
    if block.startswith("##"):
        return "h2"
    if block.startswith("###"):
        return "h3"
    if block.startswith("####"):
        return "h4"
    if block.startswith("#####"):
        return "h5"
    if block.startswith("######"):
        return "h6"

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
    

