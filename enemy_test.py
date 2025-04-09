from rpg.enemy import Enemy
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestEnemy(unittest.TestCase):

    def setUp(self):
        """
        Set up an Enemy instance for testing.
        """
        self.enemy = Enemy(
            name="Goblin",
            description="A small but ferocious creature.",  # Period included
            health=30,
            damage=5,
            difficulty="Easy"
        )

    def test_enemy_initialization(self):
        """
        Test that the Enemy class initializes correctly.
        """
        self.assertEqual(self.enemy.name, "Goblin")
        self.assertEqual(self.enemy.description,
                         "A small but ferocious creature.")
        self.assertEqual(self.enemy.health, 30)
        self.assertEqual(self.enemy.damage, 5)
        self.assertEqual(self.enemy.difficulty, "Easy")
        self.assertEqual(self.enemy.defeated_monsters, [])

    @patch('builtins.print')
    def test_enemy_inspect(self, mock_print):
        """
        Test the inspect method of the Enemy.
        """
        self.enemy.inspect()
        mock_print.assert_called_with(
            "Goblin:A small but ferocious creature., Health: 30, Damage: 5"
        )

    @patch('builtins.print')
    def test_enemy_interact_first_encounter(self, mock_print):
        """
        Test the interact method
        when encountering the enemy for the first time.
        """
        player = MagicMock()
        player.start_combat = MagicMock()

        self.enemy.interact(player)

        mock_print.assert_called_with("A wild Goblin appears!")
        player.start_combat.assert_called_with(self.enemy)
        self.assertIn("Goblin", self.enemy.defeated_monsters)

    @patch('builtins.print')
    def test_enemy_interact_after_defeat(self, mock_print):
        """
        Test the interact method after the enemy has been defeated.
        """
        player = MagicMock()
        self.enemy.defeated_monsters.append("Goblin")

        self.enemy.interact(player)

        # Should not print anything or start combat again
        mock_print.assert_not_called()
        player.start_combat.assert_not_called()

    @patch('builtins.print')
    def test_enemy_attack_player_alive(self, mock_print):
        """
        Test the attack method when the player is still alive after attack.
        """
        player = MagicMock()
        player.health = 20

        result = self.enemy.attack(player)

        self.assertFalse(result)
        mock_print.assert_not_called()

    @patch('builtins.print')
    def test_enemy_attack_player_defeated(self, mock_print):
        """
        Test the attack method when the player has been defeated.
        """
        player = MagicMock()
        player.health = 0

        result = self.enemy.attack(player)

        self.assertTrue(result)
        mock_print.assert_called_with("You have been defeated by the enemy!")

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "monsters": [
            {
                "name": "Orc",
                "description": "A large and brutish creature.",
                "health": 50,
                "damage": 10,
                "difficulty": "Medium"
            },
            {
                "name": "Dragon",
                "description": "A fearsome dragon with fiery breath.",
                "health": 200,
                "damage": 50,
                "difficulty": "Hard"
            }
        ]
    }))
    @patch('os.path.dirname', return_value='.')
    def test_load_monsters_success(self, mock_dirname, mock_file):
        """
        Test that load_monsters correctly
        loads a list of Enemy objects from a JSON file.
        """
        monsters = Enemy.load_monsters()
        self.assertEqual(len(monsters), 2)
        self.assertEqual(monsters[0].name, "Orc")
        self.assertEqual(monsters[0].health, 50)
        self.assertEqual(monsters[1].name, "Dragon")
        self.assertEqual(monsters[1].damage, 50)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('os.path.dirname', return_value='.')
    @patch('builtins.print')
    def test_load_monsters_file_not_found(
        self, mock_print, mock_dirname, mock_open
    ):
        """
        Test that load_monsters handles a FileNotFoundError
        gracefully and returns an empty list.
        """
        monsters = Enemy.load_monsters()
        self.assertEqual(monsters, [])
        mock_print.assert_called_with("Error loading monsters: ")

    @patch('builtins.open', new_callable=mock_open, read_data='Invalid JSON')
    @patch('os.path.dirname', return_value='.')
    @patch('builtins.print')
    def test_load_monsters_json_decode_error(
        self, mock_print, mock_dirname, mock_file
    ):
        """
        Test that load_monsters handles a JSONDecodeError
        gracefully and returns an empty list.
        """
        monsters = Enemy.load_monsters()
        self.assertEqual(monsters, [])
        mock_print.assert_called_with(
            "Error loading monsters: Expecting value: line 1 column 1 (char 0)"
        )


if __name__ == '__main__':
    unittest.main()
