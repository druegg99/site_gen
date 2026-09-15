import re
from textnode import *


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    resulting_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            resulting_nodes.append(node)
        else:
            split_str = node.text.split(delimiter)
            if len(split_str) % 2 == 0:
                raise Exception("Invalid Markdown syntax")
            for i in range(0, len(split_str)):
                if i % 2 == 0:
                    new_node = TextNode(split_str[i], TextType.TEXT)
                else:
                    new_node = TextNode(split_str[i], text_type)
                if new_node.text != "":
                    resulting_nodes.append(new_node)
    return resulting_nodes

def extract_markdown_images(text: str) -> list[(str, str)]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str) -> list[(str, str)]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def img_tuple_to_str(images: (str, str)) -> str:
    return f"![{images[0]}]({images[1]})"

def link_tuple_to_str(images: (str, str)) -> str:
    return f"[{images[0]}]({images[1]})"

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    resulting_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            resulting_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                resulting_nodes.append(node)
            else:
                working_text = [node.text]
                for image in images:
                    working_text = working_text[-1].split(img_tuple_to_str(image), 1)
                    resulting_nodes.append(TextNode(working_text[0], TextType.TEXT))
                    resulting_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                if working_text[-1] != "":
                    resulting_nodes.append(TextNode(working_text[-1], TextType.TEXT))
    return resulting_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    resulting_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            resulting_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                resulting_nodes.append(node)
            else:
                working_text = [node.text]
                for link in links:
                    working_text = working_text[-1].split(link_tuple_to_str(link), 1)
                    resulting_nodes.append(TextNode(working_text[0], TextType.TEXT))
                    resulting_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                if working_text[-1] != "":
                    resulting_nodes.append(TextNode(working_text[-1], TextType.TEXT))
    return resulting_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    initial_text = TextNode(text, TextType.TEXT)
    output = split_nodes_link([initial_text])
    output = split_nodes_image(output)
    output = split_nodes_delimiter(output, "_", TextType.ITALIC)
    output = split_nodes_delimiter(output, "**", TextType.BOLD)
    output = split_nodes_delimiter(output, "`", TextType.CODE)
    return output

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks

def block_to_block_type(md_block: str) -> BlockType:
    if md_block[0] == "#":
        i = 0
        while md_block[i] == "#":
            i += 1
        if md_block[i] == " ":
            if i < 7:
                return BlockType.HEADING
        return BlockType.PARAGRAPH

    if md_block[0:4] == "```\n" and md_block[-3:] == "```":
        return BlockType.CODE

    if md_block[0] == ">":
        lines = md_block.split("\n")
        is_quote = True
        for line in lines:
            if line[0] != ">"
                is_quote = False
        if is_quote:
            return BlockType.QUOTE

    if md_block[0:2] == "- ":
        lines = md_block.split("\n")
        is_code = True
        for line in lines:
            if line[0:2] != "- "
                is_code = False
        if is_code:
            return BlockType.UNORDERED_LIST

    if md_block[1:3] == ". ":
        lines = md_block.split("\n")
        is_list = False
        for i in range(0, len(lines)):
            if lines[i-1][0] = i + 1 and lines[i-1][1:3] == ". ":
                is_list = True
            else:
                is_list = False
        if is_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
