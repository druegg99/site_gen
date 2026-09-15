import re
from textnode import *
from htmlnode import *


#Takes text nodes, splits them as required, and assigns the given TextType
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

#Returns list of tuples with image links
def extract_markdown_images(text: str) -> list[(str, str)]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#Returns list of tuples with links
def extract_markdown_links(text: str) -> list[(str, str)]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

#helper function to split the text after links are identified
def img_tuple_to_str(images: (str, str)) -> str:
    return f"![{images[0]}]({images[1]})"

#helper function to split the text after links are identified
def link_tuple_to_str(images: (str, str)) -> str:
    return f"[{images[0]}]({images[1]})"

#Uses extract and the helper function to format images into proper nodes
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

#Uses extract and the helper function to format links into proper nodes
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

#Takes raw text and returns inline elements
def text_to_textnodes(text: str) -> list[TextNode]:
    initial_text = TextNode(text, TextType.TEXT)
    output = split_nodes_link([initial_text])
    output = split_nodes_image(output)
    output = split_nodes_delimiter(output, "_", TextType.ITALIC)
    output = split_nodes_delimiter(output, "**", TextType.BOLD)
    output = split_nodes_delimiter(output, "`", TextType.CODE)
    return output

#Takes raw document and splits into blocks
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        stripped = block.strip()
        if stripped != "":
            blocks.append(stripped)
    return blocks

#Returns block type
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
            if line[0] != ">":
                is_quote = False
        if is_quote:
            return BlockType.QUOTE

    if md_block[:2] == "- ":
        #print("list DECTECTED")
        lines = md_block.split("\n")
        is_list = True
        for line in lines:
            if line[:2] == "- ":
                is_list = is_list and True
            else:
                is_list = False
        if is_list:
            return BlockType.UNORDERED_LIST

    if md_block[1:3] == ". ":
        #print("ORDER")
        lines = md_block.split("\n")
        #print(lines)
        is_list = True
        for i in range(0, len(lines)):
            #print(f'Index: {i}, line: {lines[i]}, first slice: "{lines[i][0]}", second slice: "{lines[i][1:3]}"')
            if lines[i][0] == str(i + 1) and lines[i][1:3] == ". ":
                is_list = is_list and True
                #print(f"line {i} True: {is_list}")
            else:
                #print("list not detected")
                is_list = False
        if is_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

#Takes split block element and returns a single HTML leaf node
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise Exception("incorrect Text Type")
    if text_node.text_type is TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type is TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type is TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type is TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type is TextType.LINK:
        return LeafNode("a", text_node.text, props = {"href": text_node.url})
    if text_node.text_type is TextType.IMAGE:
        return LeafNode("img", "", props = {"src": text_node.url, "alt": text_node.text})


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    types = []
    HTML_blocks = []
    for block in blocks:
        type = block_to_block_type(block)
        inline_text = block_to_inline_text(block, type)
        raw_text = inline_text[0]
        if type is BlockType.CODE:
            HTML_blocks.append(ParentNode("pre", [LeafNode("code", raw_text)]))
        else:
            textnodes = text_to_textnodes(raw_text)
            leaves = []
            for node in textnodes:
                leaves.append(text_node_to_html_node(node))
            if type is BlockType.QUOTE:
                HTML_blocks.append(ParentNode("blockquote", leaves))
            if type is BlockType.UNORDERED_LIST:
                HTML_blocks.append(ParentNode("ul", list_raw_to_leaves(raw_text)))
            if type is BlockType.ORDERED_LIST:
                HTML_blocks.append(ParentNode("ol", list_raw_to_leaves(raw_text)))
            if type is BlockType.HEADING:
                HTML_blocks.append(ParentNode("h" + inline_text[1], leaves))
            if type is BlockType.PARAGRAPH:
                paragraph_lines = raw_text.split("\n")
                paragraph_spaces = ""
                for line in paragraph_lines:
                    paragraph_spaces += line + " "
                paragraph_nodes = text_to_textnodes(paragraph_spaces[:-1])
                paragraph_leaves = []
                for leaf in paragraph_nodes:
                    paragraph_leaves.append(text_node_to_html_node(leaf))

                HTML_blocks.append(ParentNode("p", paragraph_leaves))
                #HTML_blocks.append(ParentNode("p", leaves))
    return ParentNode("div", HTML_blocks)

#Returns the raw inline text in a tuple, second element is the heading number if heading
def block_to_inline_text(block: str, type: BlockType) -> (str, str):
    if type is BlockType.CODE:
        return (block[4:-3], "")
    if type is BlockType.PARAGRAPH:
        return (block, "")
    if type is BlockType.QUOTE:
        lines = block.split("\n")
        out = ""
        for line in lines:
            out += line[1:].strip() + "\n"
        return (out[:-1], "")
    if type is BlockType.HEADING:
        i = 0
        while block[i] == "#":
            i += 1
        return (block[i + 1:], str(i))
    if type is BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        out = ""
        for line in lines:
            out += line[2:] + "\n"
        return (out[:-1], "")
    if type is BlockType.ORDERED_LIST:
        lines = block.split("\n")
        out = ""
        for line in lines:
            out += line[3:] + "\n"
        return (out[:-1], "")

def list_raw_to_leaves(raw_text: str) -> list[ParentNode]:
    lines = raw_text.split("\n")
    elements = []
    for line in lines:
        line_nodes = text_to_textnodes(line)
        list_line = []
        for node in line_nodes:
            list_line.append(text_node_to_html_node(node))
        elements.append(ParentNode("li", list_line))
    return elements
