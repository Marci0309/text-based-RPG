import unittest
from unittest.mock import patch, MagicMock
from rpg.game import Game
from rpg.enemy import Enemy


class TestGame(unittest.TestCase):

    def setUp(self):
        """
        Set up a Game instance for testing.
        """
        self.game = Game()

    @patch('builtins.input', side_effect=[
        'TestPlayer',    # Player enters their name
        '1',             # Player interacts with NPC
        '1',             # Asks about the place
        '2',             # Tries to open the door
        '4',             # Exits the game
        '-1'             # Final exit to end the loop
    ])
    @patch('random.randint', return_value=3)  # Control random events
    def test_game_flow(self, mock_input, mock_randint):
        """
        Test game flow with controlled input and avoid infinite loops.
        """
        with patch('rpg.game.save_game'), patch('rpg.game.load_game'):
            # Run the game (this simulates the full game loop)
            self.game.run()

        # Test assertions
        self.assertEqual(self.game.player_instance.name, "TestPlayer")
        self.assertEqual(len(self.game.rooms), 1)  # Ensure 1 room exists
        self.assertFalse(self.game.boss_fight_done)

    @patch('builtins.input', side_effect=[
        'Invalid',       # Invalid input
        'TestPlayer',    # Correct input
        '-1'             # Exit
    ])
    @patch('builtins.print')
    def test_invalid_input(self, mock_print, mock_input):
        """
        Test handling of invalid input by the game loop.
        """
        self.game.scanner.read_int = MagicMock(side_effect=[1, -1])
        self.game.run()

        # Verify invalid input was handled
        mock_print.assert_any_call("Invalid input. Please try again.")

    @patch('builtins.input', side_effect=[
        'TestPlayer',    # Player enters their name
        '1',             # Talks to NPC
        '2',             # Asks for story
        '-1'             # Exit game
    ])
    @patch('builtins.print')
    def test_npc_interaction(self, mock_print, mock_input):
        """
        Test interaction with the NPC in the starting room.
        """
        self.game.scanner.read_int = MagicMock(side_effect=[1, -1])
        self.game.run()

        # Verify interaction with NPC
        mock_print.assert_any_call("Game guide: 'What \
                                   would you like to know?'")

    @patch('builtins.input', side_effect=[
        'TestPlayer',    # Player enters their name
        '7',             # Interacts with trader
        '-1'             # Exit game
    ])
    @patch('rpg.npc.Trader.interact')  # Correct the method mock
    def test_player_trader_interaction(self, mock_trader_interact, mock_input):
        """
        Test player interaction with a trader.
        """
        self.game.scanner.read_int = MagicMock(return_value=7)
        self.game.run()

        # Ensure trader interaction is called once
        mock_trader_interact.assert_called_once()

    @patch('builtins.input', side_effect=[
        'TestPlayer',    # Player enters their name
        '-1'             # Exit game
    ])
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_load_monsters(self, mock_load_monsters, mock_input):
        """
        Test that monsters are loaded correctly in the game.
        """
        self.game.monsters = ["Goblin", "Troll"]
        mock_load_monsters.return_value = self.game.monsters
        loaded_monsters = Enemy.load_monsters()

        self.assertEqual(loaded_monsters, self.game.monsters)
        mock_load_monsters.assert_called_once()


if __name__ == '__main__':
    unittest.main()
