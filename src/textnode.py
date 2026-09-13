from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        #super().self.__init__()
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode"):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

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
