import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestBlockMarkdown(unittest.TestCase):

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
    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_heading_1(self):
        md = "# Heading 1"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_2(self):
        md = "## Heading 2"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_3(self):
        md = "### Heading 3"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_4(self):
        md = "#### Heading 4"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_5(self):
        md = "##### Heading 5"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_heading_6(self):
        md = "###### Heading 6"
        result = block_to_block_type(md)
        expected = BlockType.HEADING

        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph(self):
        md = "####### Heading 7"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph_text(self):
        md = "Heading 0"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        md = "```\ncode\n```"
        result = block_to_block_type(md)
        expected = BlockType.CODE

        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        md = "> quote\n> more quote"
        result = block_to_block_type(md)
        expected = BlockType.QUOTE

        self.assertEqual(result, expected)

    def test_block_to_block_type_list(self):
        md = "- list\n- items"
        result = block_to_block_type(md)
        expected = BlockType.UNORDERED_LIST

        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        md = "1. list\n2. items"
        result = block_to_block_type(md)
        expected = BlockType.ORDERED_LIST

        self.assertEqual(result, expected)

    def test_block_to_block_type_mix(self):
        md = "> quote\n- list"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_block_to_block_type_mixed_lists(self):
        md = "- quote\n1. list"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_ordered_lists(self):
        md = "1. list\n3. item\n2. thing"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list_mixed(self):
        md = "1. list\n> quote"
        result = block_to_block_type(md)
        expected = BlockType.PARAGRAPH

        self.assertEqual(result, expected)

    def test_paragraph(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
    - This is a list
    - with items
    - and _more_ items

    1. This is an `ordered` list
    2. with items
    3. and more items

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
    # this is an h1

    this is paragraph text

    ## this is an h2
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )


    def test_blockquote(self):
        md = """
    > This is a
    > blockquote block

    this is paragraph text

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
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

    def test_extract_title_heading(self):
        md = "# Heading 1"
        result = extract_title(md)
        expected = "Heading 1"

        self.assertEqual(result, expected)

    def test_extract_title_no_heading(self):
        md = "Heading 1"

        with self.assertRaises(ValueError):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()