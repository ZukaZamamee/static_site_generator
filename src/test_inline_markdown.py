import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertListEqual(result, expected)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
            ]
        self.assertListEqual(result, expected)

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another one**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another one", TextType.BOLD),
            ]
        self.assertListEqual(result, expected)

    def test_delim_italic(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertListEqual(result, expected)

    def test_delim_bold_and_italic(self):
        node = TextNode("This is text with a **bolded word** and _an italic_", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("an italic", TextType.ITALIC),
            ]
        self.assertListEqual(result, expected)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertListEqual(result, expected)

    def test_delimiter_invalid(self):
        node = TextNode("This is text with a **invalid delimiter*", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


    def test_extract_markdown_images(self):
        result = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_multiple(self):
        result = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![dance](https://imgur.com/1Ccjp)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png"),("dance", "https://imgur.com/1Ccjp")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_link(self):
        result = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_links_multiple(self):
        result = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        expected = [("to boot dev", "https://www.boot.dev"),("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, result)

    def test_extract_markdown_links_nothing(self):
        result = extract_markdown_links(
            "This is text without a link"
        )
        expected = []
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_nothing(self):
        result = extract_markdown_images(
            "This is text without an image"
        )
        expected = []
        self.assertListEqual(expected, result)