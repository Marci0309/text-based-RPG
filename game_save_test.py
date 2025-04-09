# test_game_save.py
from rpg.game_save import save_game, load_game
from rpg.items import Item
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGameSave(unittest.TestCase):

    def setUp(self):
        """
        Set up a mock player instance with necessary attributes for testing.
        """
        self.player_instance = MagicMock()
        self.player_instance.name = 'TestPlayer'
        self.player_instance.health = 100
        self.player_instance.damage = 10
        self.player_instance.visited_rooms = ['Room1', 'Room2']
        self.player_instance.heal_used = 0
        self.player_instance.action_count = 5
        self.player_instance.defeated_enemy = ['Enemy1']
        self.player_instance.coins = 50

        # Mock inventory with items having to_dict method
        item1 = MagicMock(spec=Item)
        item1.to_dict.return_value = {'name': 'Sword', 'damage': 10}
        item2 = MagicMock(spec=Item)
        item2.to_dict.return_value = {'name': 'Shield', 'defense': 5}
        self.player_instance.inventory = [item1, item2]

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    @patch('builtins.print')
    def test_save_game_new_file(self, mock_print, mock_exists, mock_file):
        """
        Test saving game when the save file does not exist.
        """
        save_game(self.player_instance, filename='test_save.json')

        # Check that open was called with 'w' mode to write the new file
        mock_file.assert_called_with('test_save.json', 'w')

        # Get the written data
        handle = mock_file()
        written_data = ''.join(args[0]
                               for args, _ in handle.write.call_args_list)

        # Load the written data as JSON
        saved_data = json.loads(written_data)

        # Check that the player's data is correctly saved
        self.assertIn('TestPlayer', saved_data)
        player_data = saved_data['TestPlayer']
        self.assertEqual(player_data['name'], 'TestPlayer')
        self.assertEqual(player_data['health'], 100)
        self.assertEqual(player_data['damage'], 10)
        self.assertEqual(player_data['visited_rooms'], ['Room1', 'Room2'])
        self.assertEqual(player_data['heal_used'], 0)
        self.assertEqual(player_data['action_count'], 5)
        self.assertEqual(player_data['defeated_enemy'], ['Enemy1'])
        self.assertEqual(player_data['coins'], 50)
        self.assertEqual(player_data['inventory'], [
            {'name': 'Sword', 'damage': 10},
            {'name': 'Shield', 'defense': 5}
        ])

        # Check that the success message was printed
        mock_print.assert_called_with('Game for player TestPlayer \
saved successfully!')

    @patch('builtins.open',
           new_callable=mock_open,
           read_data=json.dumps({'ExistingPlayer': {'some': 'data'}}))
    @patch('os.path.exists', return_value=True)
    @patch('builtins.print')
    def test_save_game_existing_file(self, mock_print, mock_exists, mock_file):
        """
        Test saving game when the save file already exists.
        """
        save_game(self.player_instance, filename='test_save.json')

        # Check that open was called with 'r' and 'w' modes
        mock_file.assert_any_call('test_save.json', 'r')
        mock_file.assert_any_call('test_save.json', 'w')

        # Get the written data
        handle = mock_file()
        written_data = ''.join(args[0]
                               for args, _ in handle.write.call_args_list)

        # Load the written data as JSON
        saved_data = json.loads(written_data)

        # Check that the existing data is preserved and new data is added
        self.assertIn('ExistingPlayer', saved_data)
        self.assertEqual(saved_data['ExistingPlayer'], {'some': 'data'})

        self.assertIn('TestPlayer', saved_data)
        player_data = saved_data['TestPlayer']
        self.assertEqual(player_data['name'], 'TestPlayer')
        self.assertEqual(player_data['health'], 100)
        self.assertEqual(player_data['damage'], 10)
        self.assertEqual(player_data['visited_rooms'], ['Room1', 'Room2'])
        self.assertEqual(player_data['heal_used'], 0)
        self.assertEqual(player_data['action_count'], 5)
        self.assertEqual(player_data['defeated_enemy'], ['Enemy1'])
        self.assertEqual(player_data['coins'], 50)
        self.assertEqual(player_data['inventory'], [
            {'name': 'Sword', 'damage': 10},
            {'name': 'Shield', 'defense': 5}
        ])

        # Check that the success message was printed
        mock_print.assert_called_with('Game for player \
TestPlayer saved successfully!')

    @patch('rpg.game_save.Item')  # Corrected import path
    @patch('builtins.print')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        'TestPlayer': {
            'name': 'TestPlayer',
            'health': 90,
            'damage': 12,
            'visited_rooms': ['Room1', 'Room2'],
            'heal_used': 1,
            'action_count': 3,
            'defeated_enemy': ['Enemy1', 'Enemy2'],
            'inventory': [
                {'name': 'Sword', 'damage': 10},
                {'name': 'Shield', 'defense': 5}
            ],
            'coins': 60
        }
    }))
    def test_load_game_success(self, mock_file, mock_print, mock_item_class):
        """
        Test loading game when player data exists.
        """
        # Mock Item.from_dict to return MagicMock items
        sword_item = MagicMock(spec=Item)
        shield_item = MagicMock(spec=Item)
        mock_item_class.from_dict.side_effect = [sword_item, shield_item]

        # Create a player_instance to load data into
        player_instance = MagicMock()

        load_game(player_instance, 'TestPlayer', filename='test_save.json')

        # Check that Item.from_dict was called correctly
        expected_calls = [({'name': 'Sword', 'damage': 10},),
                          ({'name': 'Shield', 'defense': 5},)]
        actual_calls = [call.args
                        for call in mock_item_class.from_dict.call_args_list]
        self.assertEqual(actual_calls, expected_calls)

        # Check that the player's data was updated correctly
        self.assertEqual(player_instance.inventory, [sword_item, shield_item])
        self.assertEqual(player_instance.name, 'TestPlayer')
        self.assertEqual(player_instance.health, 90)
        self.assertEqual(player_instance.damage, 12)
        self.assertEqual(player_instance.visited_rooms, ['Room1', 'Room2'])
        self.assertEqual(player_instance.heal_used, 1)
        self.assertEqual(player_instance.action_count, 3)
        self.assertEqual(player_instance.defeated_enemy, ['Enemy1', 'Enemy2'])
        self.assertEqual(player_instance.coins, 60)

        # Check that the success message was printed
        mock_print.assert_called_with('Game for player \
TestPlayer loaded successfully!')

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('builtins.print')
    def test_load_game_file_not_found(self, mock_print, mock_open_file):
        """
        Test loading game when the save file does not exist.
        """
        player_instance = MagicMock()
        load_game(player_instance, 'TestPlayer', filename='test_save.json')

        # Check that the appropriate message was printed
        mock_print.assert_called_with('No save file found at \
test_save.json. Starting a new game.')

        # Ensure that player_instance attributes were not set
        # No methods should have been called on player_instance
        self.assertFalse(player_instance.method_calls)

    @patch('builtins.open',
           new_callable=mock_open,
           read_data=json.dumps({'OtherPlayer': {}}))
    @patch('builtins.print')
    def test_load_game_player_not_found(self, mock_print, mock_file):
        """
        Test loading game when the player data is not found in the save file.
        """
        player_instance = MagicMock()
        load_game(player_instance, 'TestPlayer', filename='test_save.json')

        # Check that the appropriate message was printed
        mock_print.assert_called_with('No saved game found \
for player TestPlayer.')

        # Ensure that player_instance attributes were not set
        # No methods should have been called on player_instance
        self.assertFalse(player_instance.method_calls)


if __name__ == '__main__':
    unittest.main()
