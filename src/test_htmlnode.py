import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_args(self):
        node = HTMLNode()

        result = node.props_to_html()
        expected = ""

        self.assertEqual(result, expected)

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})

        result = node.props_to_html()
        expected = ""

        self.assertEqual(result, expected)

    def test_props_to_html_single_props(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com",})

        result = node.props_to_html()
        expected = " href=\"https://www.google.com\""

        self.assertEqual(result, expected)

    def test_props_to_html_multi_props(self):
        node = HTMLNode(tag="a", props={"href": "https://www.google.com","target": "_blank",})

        result = node.props_to_html()
        expected = " href=\"https://www.google.com\" target=\"_blank\""

        self.assertEqual(result, expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_tag_a_value_single_prop(self):
        node = LeafNode(tag="a", value="Hello World!", props={"href": "https://www.google.com",})

        result = node.to_html()
        expected = "<a href=\"https://www.google.com\">Hello World!</a>"

        self.assertEqual(result, expected)

    def test_leaf_to_html_tag_a_value_multi_prop(self):
        node = LeafNode(tag="a", value="Hello World!", props={"href": "https://www.google.com","target": "_blank",})

        result = node.to_html()
        expected = "<a href=\"https://www.google.com\" target=\"_blank\">Hello World!</a>"

        self.assertEqual(result, expected)

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, None)

        with self.assertRaises(ValueError):
            node.to_html()