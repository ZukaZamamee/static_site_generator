import unittest

from htmlnode import HTMLNode


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