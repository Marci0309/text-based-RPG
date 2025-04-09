from rpg.cornelia import Cornelia
from rpg.items import Item
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestCornelia(unittest.TestCase):

    def setUp(self):
        """
        Set up a Cornelia instance and a mock player for testing.
        """
        self.cornelia = Cornelia()
        self.player = MagicMock()
        self.player.health = 100
        self.player.inventory = []

    @patch('builtins.input', side_effect=['0', '2'])
    @patch('builtins.print')
    def test_interact_play_game_punishment(self, mock_print, mock_input):
        """
        Test that choosing card '2' halves
        the player's health and no item is awarded.
        """
        self.cornelia.interact(self.player)

        # Assert that the player's health is halved
        self.assertEqual(self.player.health, 50)

        # Assert that no item was added to the inventory
        self.assertEqual(len(self.player.inventory), 0)

        # Assert that 'played' remains False
        # since punishment does not set it to True
        self.assertFalse(self.cornelia.played)

    @patch('rpg.cornelia.random.choice')
    # Choose to play, then choose card '0' (reward)
    @patch('builtins.input', side_effect=['0', '0'])
    @patch('builtins.print')
    def test_interact_play_game_reward(
        self,
        mock_print,
        mock_input,
        mock_random_choice
    ):
        """
        Test that choosing a valid card awards an epic item to the player.
        """
        # Mock random.choice to return a specific item for predictability
        mock_random_choice.return_value = {
            "name": "Epic Sword",
            "description": "A sword of epic proportions.",
            "effect_type": "damage",
            "value": 20,
            "price": 0
        }

        self.cornelia.interact(self.player)

        # Assert that an item was added to the player's inventory
        self.assertEqual(len(self.player.inventory), 1)
        epic_item = self.player.inventory[0]
        self.assertEqual(epic_item.name, "Epic Sword")
        self.assertEqual(epic_item.rarity, "epic")
        self.assertEqual(epic_item.effect_type, "damage")
        self.assertEqual(epic_item.value, 20)
        self.assertEqual(epic_item.description, "A sword of epic proportions.")
        self.assertEqual(epic_item.price, 0)

        # Assert that 'played' is set to True
        self.assertTrue(self.cornelia.played)

        # Assert that the player's health remains unchanged
        self.assertEqual(self.player.health, 100)

    @patch('builtins.input', side_effect=['1'])  # Choose not to play
    @patch('builtins.print')
    def test_interact_decline_game(self, mock_print, mock_input):
        """
        Test that declining to play results
        in no changes to the player's state.
        """
        self.cornelia.interact(self.player)

        # Assert that the player's health remains unchanged
        self.assertEqual(self.player.health, 100)

        # Assert that the player's inventory remains empty
        self.assertEqual(len(self.player.inventory), 0)

        # Assert that 'played' remains False
        self.assertFalse(self.cornelia.played)

    # Invalid choice, then choose not to play

    @patch('builtins.input', side_effect=['invalid', '1'])
    @patch('builtins.print')
    def test_interact_invalid_choice(self, mock_print, mock_input):
        """
        Test that entering an invalid choice prompts the player again.
        """
        self.cornelia.interact(self.player)

        # Assert that the player's health remains unchanged
        self.assertEqual(self.player.health, 100)

        # Assert that the player's inventory remains empty
        self.assertEqual(len(self.player.inventory), 0)

        # Assert that 'played' remains False
        self.assertFalse(self.cornelia.played)

        # Assert that the invalid choice message was printed
        mock_print.assert_any_call(
            "Invalid choice. Please enter (0) to play or (1) to quit the game."
        )

    # Play game, invalid card, then valid card

    @patch('builtins.input', side_effect=['0', 'invalid', '3'])
    @patch('builtins.print')
    def test_play_game_invalid_card_choice(self, mock_print, mock_input):
        """
        Test that entering an invalid card choice
        results in losing the chance to play.
        """
        self.cornelia.interact(self.player)

        # Assert that no item was added to the player's inventory
        self.assertEqual(len(self.player.inventory), 0)

        # Assert that the player's health remains unchanged
        self.assertEqual(self.player.health, 100)

        # Assert that 'played' remains False
        self.assertFalse(self.cornelia.played)

        # Assert that the invalid card choice message was printed
        mock_print.assert_any_call(
            "Invalid card choice. You lost your chance!"
            )

    @patch('rpg.cornelia.random.choice')
    def test_get_random_epic_item(self, mock_random_choice):
        """
        Test that get_random_epic_item returns items with correct attributes.
        """
        epic_items_data = [
            {
                "name": "Epic Sword",
                "description": "A sword of epic proportions.",
                "effect_type": "damage",
                "value": 20,
                "price": 0
            },
            {
                "name": "Epic Axe",
                "description": "An axe with unstoppable power.",
                "effect_type": "damage",
                "value": 15,
                "price": 0
            },
            {
                "name": "Epic Bow",
                "description": "A bow that shoots arrows with great precision",
                "effect_type": "damage",
                "value": 18,
                "price": 0
            }
        ]

        # Mock random.choice to return each epic item in sequence
        mock_random_choice.side_effect = epic_items_data

        items_returned = set()
        for expected_item_data in epic_items_data:
            item = self.cornelia.get_random_epic_item()
            self.assertIsInstance(item, Item)
            self.assertEqual(item.rarity, "epic")
            self.assertEqual(item.name, expected_item_data['name'])
            self.assertEqual(
                item.description,
                expected_item_data['description']
                )
            self.assertEqual(
                item.effect_type,
                expected_item_data['effect_type']
                )
            self.assertEqual(item.value, expected_item_data['value'])
            self.assertEqual(item.price, expected_item_data['price'])
            items_returned.add(item.name)

        # Assert that all possible items were returned
        self.assertEqual(
            items_returned,
            {"Epic Sword", "Epic Axe", "Epic Bow"}
            )


if __name__ == '__main__':
    unittest.main()
