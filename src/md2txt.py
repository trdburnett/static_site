from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            delimiter_count = 0
            for char in node.text:
                if char == delimiter:
                    delimiter_count += 1
            print(delimiter_count)
        if delimiter_count % 2 != 0:
            raise Exception("Invalid Markdown Syntax")
        else:
            text = node.text.split(delimiter,maxsplit=i(delimiter_count//2))
            print(text)

split_nodes_delimiter([TextNode("This is text with a `code block` word", TextType.TEXT)], "`", TextType.CODE)