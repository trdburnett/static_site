import re
from enum import Enum
from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiter_count = 0
            if len(delimiter) > 2:
                raise Exception("Invalid Delimiter")
            if len(delimiter) == 2:
                check_next_char = False
                for char in node.text:
                    if check_next_char:
                        if char == delimiter[1]:
                            delimiter_count +=1
                        check_next_char = False
                    if not check_next_char: 
                        if char == delimiter[0]:
                            check_next_char = True
            if len(delimiter) == 1:        
                for char in node.text:
                    if char == delimiter:
                        delimiter_count += 1
            if delimiter_count % 2 != 0:
                raise Exception("Invalid Markdown Syntax")
            elif delimiter_count == 0:
                new_nodes.append(node)
            else:
                text = node.text.split(delimiter,maxsplit=(delimiter_count))
                for i in range(0,len(text)):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(text[i], text_type))
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text: str) -> list[tuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_images(node.text)
            if extracted == []:
                if node.text != "":
                    new_nodes.append(node)
            else:
                split_node = node.text.split(f"![{extracted[0][0]}]({extracted[0][1]})", maxsplit=1)
                if split_node[0] != "":
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(extracted[0][0], TextType.IMAGE, extracted[0][1]))
                if split_node[1] != "":
                    new_nodes.append(TextNode(split_node[1], TextType.TEXT))
            if len(extracted) > 1:
                return split_nodes_image(new_nodes)
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if old_nodes == []:
        raise Exception("Empty Input List")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted = extract_markdown_links(node.text)
            if extracted == []:
                if node.text != "":
                    new_nodes.append(node)
            else:
                split_node = node.text.split(f"[{extracted[0][0]}]({extracted[0][1]})", maxsplit=1)
                if split_node[0] != "":
                    new_nodes.append(TextNode(split_node[0], TextType.TEXT))
                new_nodes.append(TextNode(extracted[0][0], TextType.LINK, extracted[0][1]))
                if split_node[1] != "":
                    new_nodes.append(TextNode(split_node[1], TextType.TEXT))
            if len(extracted) > 1:
                return split_nodes_link(new_nodes)
    return new_nodes            

def text_to_textnodes(text: str) -> list[TextNode]:
    if text == "":
        raise Exception("Empty String")
    bold_in_text = False
    italic_in_text = False
    code_in_text = False
    image_in_text = False
    link_in_text = False
    if "**" in text:
        bold_in_text = True
    if "_" in text:
        italic_in_text = True
    if "`" in text:
        code_in_text = True
    image_found = extract_markdown_images(text)
    if image_found != []:
        image_in_text = True
    link_found = extract_markdown_links(text)
    if link_found != []:
        link_in_text = True
    result = ([TextNode(text, TextType.TEXT)])
    if bold_in_text:
        result = split_nodes_delimiter(result, "**", TextType.BOLD)
    if italic_in_text:
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
    if code_in_text:
        result = split_nodes_delimiter(result, "`", TextType.CODE)
    if image_in_text:
        result = split_nodes_image(result)
    if link_in_text:
        result = split_nodes_link(result)
    return result

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    starting_blocks = markdown.split("\n\n")
    for string in starting_blocks:
        print(string)
        stripped_whitespace = string.strip()
        stripped_newlines = stripped_whitespace.strip("\n")
        blocks.append(stripped_newlines)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown: str) -> BlockType:
    if markdown == "":
        raise Exception("Input String Is Empty")
    markdown_as_list = markdown.split("\n")
    quote_block = False
    unordered_list_block = False
    ordered_list_block = False
    quote_block_checks = []
    unordered_list_block_checks = []
    ordered_list_block_checks = []
    if markdown_as_list != []:
        for string in markdown_as_list:
            if string.startswith(">"):
                quote_block_checks.append(True)
            if not string.startswith(">"):
                quote_block_checks.append(False)
            if string.startswith("- "):
                unordered_list_block_checks.append(True)
            if not string.startswith("- "):
                unordered_list_block_checks.append(False)
            if re.match(r"^[0-9]\. ", string):
                ordered_list_block_checks.append(string[0])
            if re.match(r"[0-9]{2}\. ", string):
                ordered_list_block_checks.append(string[0:2])
    if quote_block_checks != []:
        if False not in quote_block_checks:
            quote_block = True
    if unordered_list_block_checks != []:
        if False not in unordered_list_block_checks:
            unordered_list_block = True
    if ordered_list_block_checks != []:
        order_check = 1
        for num in ordered_list_block_checks:
            if int(num) == order_check:
                order_check += 1
        if (order_check - 1) == len(ordered_list_block_checks):
            ordered_list_block = True
    if markdown.startswith("# "):
        return BlockType.HEADING
    elif markdown.startswith("## "):
        return BlockType.HEADING
    elif markdown.startswith("### "):
        return BlockType.HEADING
    elif markdown.startswith("#### "):
        return BlockType.HEADING
    elif markdown.startswith("##### "):
        return BlockType.HEADING
    elif markdown.startswith("###### "):
        return BlockType.HEADING
    elif markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    elif quote_block:
        return BlockType.QUOTE
    elif unordered_list_block:
        return BlockType.UNORDERED_LIST
    elif ordered_list_block:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

