# test_door.py
from rpg.door import door
from rpg.room import room as Room
from rpg.player import player
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestDoor(unittest.TestCase):
    def setUp(self):
        """
        Set up test cases for Door class.
        """
        # Mock destination room
        self.destination_room = MagicMock(spec=Room)
        self.destination_room.name = 'Destination Room'

        # Create a mock player
        self.mock_player = MagicMock(spec=player)
        self.mock_player.current_room = None

        # Door leading to destination room
        self.door_to_destination = door(
            name='Wooden Door',
            description='An old wooden door.',
            destination=self.destination_room,
            locked=False
        )

        # Door with no destination
        self.door_no_destination = door(
            name='Mystery Door',
            description='A door that seems to go nowhere.',
            destination=None,
            locked=False
        )

        # Locked door
        self.locked_door = door(
            name='Iron Door',
            description='A sturdy iron door with a heavy lock.',
            destination=self.destination_room,
            locked=True
        )

    @patch('builtins.print')
    def test_door_initialization(self, mock_print):
        """
        Test that the door is initialized correctly.
        """
        self.assertEqual(self.door_to_destination.name, 'Wooden Door')
        self.assertEqual(
            self.door_to_destination.description,
            'An old wooden door.'
            )
        self.assertEqual(
            self.door_to_destination.destination,
            self.destination_room
            )
        self.assertFalse(self.door_to_destination.locked)

    @patch('builtins.print')
    def test_interact_with_unlocked_door_with_destination(self, mock_print):
        """
        Test interacting with an unlocked door that has a destination.
        """
        self.door_to_destination.interact(self.mock_player)
        # Assert that the player moved to the destination room
        self.assertEqual(self.mock_player.current_room, self.destination_room)
        # Assert that the correct message was printed
        mock_print.assert_called_with("You go through the Wooden Door.")

    @patch('builtins.print')
    def test_interact_with_unlocked_door_no_destination(self, mock_print):
        """
        Test interacting with an unlocked door that has no destination.
        """
        self.door_no_destination.interact(self.mock_player)
        # Assert that the player's current room did not change
        self.assertIsNone(self.mock_player.current_room)
        # Assert that the correct message was printed
        mock_print.assert_called_with("This door does not lead anywhere.")

    @patch('builtins.print')
    def test_interact_with_locked_door(self, mock_print):
        """
        Test interacting with a locked door.
        """
        self.locked_door.interact(self.mock_player)
        # Assert that the player did not move to the destination room
        self.assertNotEqual(
            self.mock_player.current_room,
            self.destination_room
            )
        # Assert that the correct message was printed
        mock_print.assert_called_with(
            "The Iron Door is locked. You cannot go through it."
            )

    @patch('builtins.print')
    def test_inspect_unlocked_door(self, mock_print):
        """
        Test inspecting an unlocked door.
        """
        self.door_to_destination.inspect()
        # Assert that the correct information was printed
        mock_print.assert_called_with(
            "Door: Wooden Door, Description: \
An old wooden door., Locked: False"
            )

    @patch('builtins.print')
    def test_inspect_locked_door(self, mock_print):
        """
        Test inspecting a locked door.
        """
        self.locked_door.inspect()
        # Assert that the correct information was printed
        mock_print.assert_called_with("Door: Iron Door, Description: \
A sturdy iron door with a heavy lock., Locked: True")


if __name__ == '__main__':
    unittest.main()
