import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image,  text_to_textnodes
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ]
        self.assertListEqual(expected, result)

    def test_split_links(self):
        node = TextNode(
            "This is text with an [google](www.google.com) and another [frontpage of the internet](www.reddit.com/r/all)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        expected = [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("google", TextType.LINK, "www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("frontpage of the internet", TextType.LINK, "www.reddit.com/r/all"),
            ]
        self.assertListEqual(expected, result)

    def test_split_links_and_images(self):
        node = TextNode(
            "This is text with a link [google](www.google.com) and an image ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        result = split_nodes_image(result)
        expected = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("google", TextType.LINK, "www.google.com"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ]
        self.assertListEqual(expected, result)

    def test_split_multi_links_and_images(self):
        node = TextNode(
            "This is text with a link [google](www.google.com) and an image ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another link [frontpage of the internet](www.reddit.com/r/all) and another image ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        result = split_nodes_image(result)
        expected = [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("google", TextType.LINK, "www.google.com"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("frontpage of the internet", TextType.LINK, "www.reddit.com/r/all"),
                TextNode(" and another image ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ]
        self.assertListEqual(expected, result)

    def test_split_no_links_and_images(self):
        node = TextNode(
            "This is text with no links or images.",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        result = split_nodes_image(result)
        expected = [
                TextNode("This is text with no links or images.", TextType.TEXT),
            ]
        self.assertListEqual(expected, result)

    def test_text_to_textnode_no_links_and_images(self):
        text = "This is text with no links or images."
        result = text_to_textnodes(text)
        expected = [
                TextNode("This is text with no links or images.", TextType.TEXT),
            ]
        self.assertListEqual(expected, result)

    def test_text_to_textnode_everything(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
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

        self.assertListEqual(expected, result)

    def test_text_to_textnode_bolded(self):
        text = "This is text with a **bolded** word."
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
            ]
        self.assertListEqual(expected, result)

    def test_text_to_textnode_bold_and_image(self):
        text = "This is **text** and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertListEqual(expected, result)