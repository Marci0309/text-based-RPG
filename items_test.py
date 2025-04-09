from rpg.items import Item
import io
import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestItem(unittest.TestCase):

    def setUp(self):
        """
        Set up an Item instance for testing.
        """
        self.default_item = Item(
            name="Health Potion",
            rarity="common",
            effect_type="health",
            value=50,
            description="Restores 50 health points.",
            price=10
        )

    def test_item_initialization(self):
        """
        Test that the Item class initializes correctly.
        """
        self.assertEqual(self.default_item.name, "Health Potion")
        self.assertEqual(self.default_item.rarity, "common")
        self.assertEqual(self.default_item.effect_type, "health")
        self.assertEqual(self.default_item.value, 50)
        self.assertEqual(self.default_item.description,
                         "Restores 50 health points.")
        self.assertEqual(self.default_item.price, 10)

    def test_item_to_dict(self):
        """
        Test that the Item's to_dict method returns the correct dictionary.
        """
        expected_dict = {
            'name': "Health Potion",
            'rarity': "common",
            'effect_type': "health",
            'value': 50,
            'description': "Restores 50 health points.",
            'price': 10
        }
        self.assertEqual(self.default_item.to_dict(), expected_dict)

    def test_item_from_dict(self):
        """
        Test that the from_dict method creates an Item object correctly.
        """
        item_dict = {
            'name': "Sword of Power",
            'rarity': "rare",
            'effect_type': "damage",
            'value': 25,
            'description': "A sword that deals extra damage.",
            'price': 100
        }
        item_instance = Item.from_dict(item_dict)
        self.assertEqual(item_instance.name, "Sword of Power")
        self.assertEqual(item_instance.rarity, "rare")
        self.assertEqual(item_instance.effect_type, "damage")
        self.assertEqual(item_instance.value, 25)
        self.assertEqual(item_instance.description,
                         "A sword that deals extra damage.")
        self.assertEqual(item_instance.price, 100)

    def test_item_price(self):
        """
        Test that the price of the item is set correctly.
        """
        self.assertEqual(self.default_item.price, 10)

    @patch('builtins.open', new_callable=mock_open, read_data='{"items": []}')
    @patch('sys.stdout', new_callable=io.StringIO)  # Suppress print output
    def test_load_items_empty_file(self, mock_stdout, mock_file):
        """
        Test that load_items returns an empty list if the items file is empty.
        """
        items = Item.load_items()
        self.assertEqual(items, [])

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "items": [
            {
                "name": "Health Potion",
                "rarity": "common",
                "effect_type": "health",
                "value": 50,
                "description": "Restores 50 health points.",
                "price": 10
            },
            {
                "name": "Sword of Power",
                "rarity": "rare",
                "effect_type": "damage",
                "value": 25,
                "description": "A sword that deals extra damage.",
                "price": 100
            }
        ]
    }))
    @patch('os.path.dirname', return_value='.')
    def test_load_items_success(self, mock_dirname, mock_file):
        """
        Test that load_items correctly
        loads a list of Item objects from a JSON file.
        """
        items = Item.load_items()

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].name, "Health Potion")
        self.assertEqual(items[1].name, "Sword of Power")

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.dirname', return_value='.')
    @patch('sys.stdout', new_callable=io.StringIO)  # Suppress print output
    def test_load_items_file_not_found(self,
                                       mock_stdout, mock_dirname, mock_open):
        """
        Test that load_items handles a FileNotFoundError
        gracefully and returns an empty list.
        """
        items = Item.load_items()
        self.assertEqual(items, [])

    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON')
    @patch('os.path.dirname', return_value='.')
    @patch('sys.stdout', new_callable=io.StringIO)  # Suppress print output
    def test_load_items_json_decode_error(self,
                                          mock_stdout,
                                          mock_dirname, mock_file):
        """
        Test that load_items handles a
        JSONDecodeError and returns an empty list.
        """
        items = Item.load_items()
        self.assertEqual(items, [])


if __name__ == '__main__':
    unittest.main()
