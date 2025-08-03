import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children,None)
        self.assertEqual(node.props,None)

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(node.__repr__(),"HTMLNode(p, What a strange world, None, {'class': 'primary'})")

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


class TestParentNode(unittest.TestCase):
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

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_child(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()