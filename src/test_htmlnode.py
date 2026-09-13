import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq_none(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_props(self):
        node = HTMLNode(props = {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_children(self):
        child = HTMLNode()
        child2 = HTMLNode(props = {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        print(child2)
        parent = HTMLNode(children = [child, child2])
        print(parent)
        parent2 = HTMLNode(children = [child])
        self.assertNotEqual(parent, parent2)

    def test_equal_val(self):
        node = HTMLNode(tag = "test")
        node2 = HTMLNode(tag = "test")
        self.assertEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("b", "This is bold!")
        self.assertEqual(node.to_html(), "<b>This is bold!</b>")

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "This is a link!", props = {"href": "https.www.urmom.com"})
        self.assertEqual(node.to_html(), '<a href="https.www.urmom.com">This is a link!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
