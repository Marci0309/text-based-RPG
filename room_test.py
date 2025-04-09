from rpg.room import room
import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestRoom(unittest.TestCase):

    def setUp(self):
        """
        Set up a Room instance for testing.
        """
        # Mock 'initialize_npcs' to prevent
        # unwanted NPC and trader initialization
        with patch.object(room, 'initialize_npcs'):
            self.default_room = room(
                name="Test Room",
                description="A room for testing."
            )
    # Mock to prevent NPC/trader initialization

    @patch.object(room, 'initialize_npcs')
    def test_room_initialization(self, mock_initialize_npcs):
        """
        Test that the Room class initializes correctly.
        """
        room_instance = room(name="Test Room")
        self.assertEqual(room_instance.name, "Test Room")
        # Since description is None, it will select a random one
        self.assertTrue(isinstance(room_instance.description, str))
        self.assertEqual(len(room_instance.doors), 0)
        self.assertEqual(len(room_instance.npcs), 0)
        self.assertEqual(len(room_instance.traders), 0)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "room_descriptions": ["A mysterious room."],
        "npcs": [],
        "traders": []
    }))
    @patch('random.choice', return_value="A mysterious room.")
    def test_room_random_description(self, mock_choice, mock_open):
        """
        Test that a random room description is chosen when none is provided.
        """
        # Prevent NPC initialization
        with patch.object(room, 'initialize_npcs'):
            room_instance = room(name="Random Room")
            self.assertEqual(room_instance.description, "A mysterious room.")

    @patch('random.randint', return_value=1)  # Mock 1 NPC initialization
    @patch('random.sample', return_value=[
        {"name": "Friendly NPC",
         "description": "A helpful character.",
         "dialogues": {}}
    ])
    @patch('random.choice', return_value={
        "name": "Trader Bob",
        "description": "A merchant with many goods.",
        "dialogues": {},
        "items": [{"name": "Health Potion",
                   "rarity": "common",
                   "effect_type": "health",
                   "value": 50, "description": "Restores 50 health.",
                   "price": 10}]
    })
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "npcs": [
            {"name": "Friendly NPC",
             "description": "A helpful character.",
             "dialogues": {}}
        ],
        "traders": [
            {"name": "Trader Bob",
             "description": "A merchant with many goods.",
             "dialogues": {},
             "items": [{"name": "Health Potion", "rarity": "common",
                                "effect_type": "health", "value": 50,
                                "description": "Restores 50 health.",
                                "price": 10}]}
        ]
    }))
    def test_initialize_npcs(self,
                             mock_open,
                             mock_choice,
                             mock_sample,
                             mock_randint):
        """
        Test that NPCs and traders are initialized correctly.
        """
        # The order of mocks is reversed when passed as arguments
        test_room = room(name="Test Room with NPCs")

        # Assert that 1 NPC and 1 trader were initialized correctly
        self.assertEqual(len(test_room.npcs), 1)
        self.assertEqual(test_room.npcs[0].name, "Friendly NPC")

        self.assertEqual(len(test_room.traders), 1)
        self.assertEqual(test_room.traders[0].name, "Trader Bob")
        self.assertEqual(test_room.traders[0].items[0].name, "Health Potion")

    @patch('random.randint', return_value=3)
    @patch('random.shuffle', side_effect=lambda x: x)
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "door_descriptions": ["A sturdy oak door.",
                              "A creaky old door.",
                              "A metal door."],
        "npcs": [],
        "traders": []
    }))
    def test_add_doors(self, mock_open, mock_shuffle, mock_randint):
        """
        Test that doors are added correctly to the room.
        """
        with patch.object(room, 'initialize_npcs'):
            existing_rooms = [room(name="Existing Room 1"),
                              room(name="Existing Room 2")]
            self.default_room.add_doors(existing_rooms)

            # Assert that 3 doors were added
            self.assertEqual(len(self.default_room.doors), 3)
            self.assertIn("Door 1", self.default_room.doors)
            self.assertIn("Door 2", self.default_room.doors)
            self.assertIn("Door 3", self.default_room.doors)

    @patch('builtins.print')
    def test_room_inspect(self, mock_print):
        """
        Test the inspect method of the room.
        """
        self.default_room.inspect()
        mock_print.assert_called_with(
            "\nYou decide to look around and see: A room for testing. "
            "There are 0 doors in this room."
        )

    @patch('builtins.print')
    def test_room_interact(self, mock_print):
        """
        Test the interact method of the room.
        """
        self.default_room.interact()
        mock_print.assert_called_with("You can explore the \
room or look for NPCs.")

    @patch('random.randint', side_effect=[2])
    @patch('random.choice', return_value="A mysterious room.")
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "room_descriptions": ["A mysterious room."],
        "door_descriptions": ["A simple wooden door.", "A heavy iron door."],
        "npcs": [],
        "traders": []
    }))
    def test_room_random_description_and_doors(self,
                                               mock_open,
                                               mock_choice,
                                               mock_randint):
        """
        Test that random descriptions and random number of
        doors are used when no description is provided and doors are added.
        """
        with patch.object(room, 'initialize_npcs'):
            new_room = room(name="Test Room")
            existing_rooms = [room(name="Existing Room")]
            new_room.add_doors(existing_rooms)

            self.assertEqual(new_room.description, "A mysterious room.")
            # Two doors should be added
            self.assertEqual(len(new_room.doors), 2)


if __name__ == '__main__':
    unittest.main()
