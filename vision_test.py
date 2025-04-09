from rpg.vision_handler import (
    visions,
    get_next_vision,
    show_next_vision,
    reveal_truth
)
import unittest
from unittest.mock import patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestVisions(unittest.TestCase):

    def test_get_next_vision_within_range(self):
        """
        Test get_next_vision when the index is within the range of visions.
        """
        index = 0
        vision, updated_index = get_next_vision(index)
        self.assertEqual(vision, visions[0])
        self.assertEqual(updated_index, 1)

    def test_get_next_vision_at_end(self):
        """
        Test get_next_vision when all visions have been shown.
        """
        index = len(visions)
        vision, updated_index = get_next_vision(index)
        self.assertEqual(vision,
                         "You have recalled all you can from your past.")
        self.assertEqual(updated_index, index)

    def test_get_next_vision_past_end(self):
        """
        Test get_next_vision when index is beyond the range of visions.
        """
        index = len(visions) + 5
        vision, updated_index = get_next_vision(index)
        self.assertEqual(vision,
                         "You have recalled all you can from your past.")
        self.assertEqual(updated_index, index)

    @patch('builtins.print')
    def test_show_next_vision_within_range(self, mock_print):
        """
        Test show_next_vision when the index is within the range of visions.
        """
        index = 0
        updated_index = show_next_vision(index)
        expected_output = f"\n** Vision from the past: **\n{visions[0]}\n"
        mock_print.assert_called_with(expected_output)  # Removed .strip()
        self.assertEqual(updated_index, 1)

    @patch('builtins.print')
    def test_show_next_vision_at_end(self, mock_print):
        """
        Test show_next_vision when all visions have been shown.
        """
        index = len(visions)
        updated_index = show_next_vision(index)
        expected_output = (
            "\n** Vision from the past: **\nYou \
have recalled all you can from your past.\n"
        )
        mock_print.assert_called_with(expected_output)  # Removed .strip()
        self.assertEqual(updated_index, index)

    @patch('builtins.print')
    def test_reveal_truth(self, mock_print):
        """
        Test reveal_truth function to ensure
        it prints the correct final message.
        """
        reveal_truth()
        expected_calls = [
            unittest.mock.call("\n=== The Truth Revealed ===\n"),
            unittest.mock.call(
                "As the dust settles and the final battle ends,"
                "the truth is revealed...\n\n"
                "Everything you've experienced here \
has been leading to this moment."
                "The visions, the memories,"
                "the challenges—they were all a reflection of"
                "your past. You now understand that \
the Labyrinth is a construct of "
                "your own mind, a way to come to \
terms with the truths you've buried "
                "deep within yourself. With the final \
boss defeated, you are free from"
                "the labyrinth, and the memories of \
your past can finally rest."
            )
        ]
        mock_print.assert_has_calls(expected_calls)

    @patch('builtins.print')
    def test_show_next_vision_past_end(self, mock_print):
        """
        Test show_next_vision when index is beyond the range of visions.
        """
        index = len(visions) + 5
        updated_index = show_next_vision(index)
        expected_output = (
            "\n** Vision from the past: **\nYou have \
recalled all you can from your past.\n"
        )
        mock_print.assert_called_with(expected_output)  # Removed .strip()
        self.assertEqual(updated_index, index)

    def test_visions_content(self):
        """
        Test that the visions list contains the correct number of visions.
        """
        # Adjust this number if visions are added or removed
        expected_number_of_visions = 20
        self.assertEqual(len(visions), expected_number_of_visions)


if __name__ == '__main__':
    unittest.main()
