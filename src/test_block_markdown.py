import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

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

if __name__ == "__main__":
    unittest.main()