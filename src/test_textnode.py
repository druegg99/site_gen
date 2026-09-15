import unittest
from text_func import *
from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("this is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_diffurl(self):
        node = TextNode("This is a link node", TextType.LINK, "url")
        node2 = TextNode("This is a link node", TextType.LINK, "url2")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "httpssomethings")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.to_html(), '<img src="httpssomethings" alt="This is an image" />')

    def test_html_url(self):
        node = TextNode("This is a url", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a url</a>')

    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_delimiter_nosplit(self):
        node = TextNode("This is text without any inline MD", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_notlink(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another [second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_notimage(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(input)
        self.assertEqual(
            output,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_erratic_linebreaks(self):
            md = """
This is a paragraph


This is another after two new lines here
This is the same paragraph on a new line



- This is a list after three line breaks
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is a paragraph",
                    "This is another after two new lines here\nThis is the same paragraph on a new line",
                    "- This is a list after three line breaks\n- with items",
                ],
            )

    def test_block_to_block(self):
        block = """This is a regular paragraph.
With two lines."""
        block1 = """- This is an unordered list
- With three elements
- This is the last"""
        block2 = """1. This is an ordered list
2. It should identify correctly
3. With three elements"""
        block3 = """1. This isn't an ordered list
3. The elements
2. Are out of ordered"""
        block4 = """- This starts like an unordered list
but isnt"""
        block5 = """```
This is a code block, let's see if it works.
```"""
        block5 = """```
Edge case for code, I think this should count as code```"""
        block6 = """```
this starts as code but isn't``"""
        block7 = "###### this is a heading"
        block8 = "# this is also a heading"
        block9 = "####### this isn't a heading"
        block10 = """>This is a quote
> With two lines"""
        block11 = """>this isn't a quote
because there's no sign here
>but here yes"""
        block12 = ">only one quote"
        block13 = """-test for
- unordered lists
- it shouldn't pass"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block2), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block4), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block5), BlockType.CODE)
        self.assertEqual(block_to_block_type(block6), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block7), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block8), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block9), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block10), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block11), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block12), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block13), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        print("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    def test_quote_block(self):
        md = '''
> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien'''
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."\n\n-- J.R.R. Tolkien</blockquote></div>'
        )

if __name__ == "__main__":
    unittest.main()
