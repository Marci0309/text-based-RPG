# test_final_boss.py
from rpg.final_boss import FinalBoss
from rpg.player import player
import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestFinalBoss(unittest.TestCase):
    def setUp(self):
        """
        Set up the test case by creating a real
        player and a FinalBoss instance.
        """
        # Create a real player instance with necessary attributes
        self.mock_player = player(starting_room=None, name='TestPlayer')
        self.mock_player.health = 100
        self.mock_player.damage = 50
        self.mock_player.inventory = []
        self.mock_player.action_count = 0
        self.mock_player.show_inventory_and_use_item = MagicMock(
            return_value=False)

        # Initialize the FinalBoss instance with the mock player
        self.final_boss = FinalBoss(self.mock_player)

        # Set boss's health and damage directly
        self.final_boss.final_boss.health = 60  # Adjusted for testing
        self.final_boss.final_boss.damage = 10

    @patch('builtins.print')
    def test_final_room_description(self, mock_print):
        """
        Test the final_room_description method to
        ensure it prints the correct information.
        """
        self.final_boss.final_room_description()
        # Check that print was called with the expected messages
        expected_calls = [
            unittest.mock.call(
                f"{self.mock_player.name}, you stand in a dark, \
ominous chamber."
                "This is the final test of your strength and courage."
                "The air is thick with tension."
            ),
            unittest.mock.call(
                f"\nYour current health: {self.mock_player.health},"
                f" strength: {self.mock_player.damage},"
                f" and you have {len(self.mock_player.inventory)} item(s)"
                " in your inventory."
            ),
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

    @patch('random.randint')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_combat_attack(self, mock_input, mock_print, mock_randint):
        """
        Test the final_combat method when the player chooses to attack.
        """
        # Provide enough inputs for the combat loop
        mock_input.side_effect = ['0', '0']  # Player will attack twice

        # Define a side effect function for random.randint
        def randint_side_effect(start, end):
            if start == 20 and end == 40:
                return 10  # Boss attack damage
            elif start == 250 and end == 300:
                return 60  # Boss health during initialization
            elif start == 10 and end == 20:
                return 10  # Boss damage during initialization
            else:
                return start  # Default value

        mock_randint.side_effect = randint_side_effect

        self.final_boss.final_combat()

        # Verify that the player's action_count increased appropriately
        self.assertEqual(self.mock_player.action_count, 2)

        # Verify that the boss's health decreased correctly
        expected_boss_health = 60 - (50 * 2)  # Boss starts at 60 health
        self.assertEqual(self.final_boss.final_boss.health,
                         expected_boss_health)

        # Adjusted expected player health
        expected_player_health = 100 - (10 * 1)  # Player takes damage once
        self.assertEqual(self.mock_player.health, expected_player_health)

    @patch('random.randint')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_combat_defend(self, mock_input, mock_print, mock_randint):
        """
        Test the final_combat method when the player chooses to defend.
        """
        # Provide inputs: defend, attack, attack
        mock_input.side_effect = ['1', '0', '0']

        # Adjust boss's health so combat ends after three actions
        self.final_boss.final_boss.health = 100

        def randint_side_effect(start, end):
            if start == 20 and end == 40:
                return 10  # Boss attack damage
            elif start == 250 and end == 300:
                return 100  # Boss health during initialization
            elif start == 10 and end == 20:
                return 10  # Boss damage during initialization
            else:
                return start  # Default value

        mock_randint.side_effect = randint_side_effect

        self.final_boss.final_combat()

        # Verify that the player's action_count increased
        self.assertEqual(self.mock_player.action_count, 3)

        # Corrected expected player health calculation
        damage_received_defend = (10 // 2)  # 5 damage when defending
        damage_received_attack = 10  # 10 damage when attacking
        total_damage_received = damage_received_defend + \
            damage_received_attack  # Total damage: 5 + 10 = 15
        # Expected health: 85
        expected_player_health = 100 - total_damage_received

        self.assertEqual(self.mock_player.health, expected_player_health)

    @patch('random.randint')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_combat_heal_allowed(self, mock_input, mock_print,
                                       mock_randint):
        """
        Test that healing works when action_count is 3 or more.
        """
        # Player's action_count is 3
        self.mock_player.action_count = 3

        # Provide inputs: heal, attack to end combat
        mock_input.side_effect = ['2', '0']

        # Adjust boss's health
        self.final_boss.final_boss.health = 50

        def randint_side_effect(start, end):
            if start == 10 and end == 30:
                return 20  # Heal amount
            elif start == 20 and end == 40:
                return 10  # Boss attack damage
            elif start == 250 and end == 300:
                return 50  # Boss health during initialization
            elif start == 10 and end == 20:
                return 10  # Boss damage during initialization
            else:
                return start  # Default value

        mock_randint.side_effect = randint_side_effect

        self.final_boss.final_combat()

        # Verify that the player's health increased by
        # heal amount and then decreased by boss attack
        # Heals 20, then takes 10 damage
        expected_player_health = min(100, 100 + 20) - 10
        self.assertEqual(self.mock_player.health, expected_player_health)

        # Verify that action_count was reset and then incremented
        self.assertEqual(self.mock_player.action_count, 1)

    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_combat_run_away(self, mock_input, mock_print):
        """
        Test that running away is not allowed in the final combat.
        """
        # Try to run away, then attack to end combat
        mock_input.side_effect = ['4', '0', '0']

        # Adjust boss's health
        self.final_boss.final_boss.health = 50

        self.final_boss.final_combat()

        # Verify that the player was informed they cannot run away
        mock_print.assert_any_call("\nThere is no escape \
from the final battle!")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_combat_invalid_choice(self, mock_input, mock_print):
        """
        Test that an invalid choice prompts an error message.
        """
        # Invalid input, then attack to end combat
        mock_input.side_effect = ['invalid', '0', '0']

        # Adjust boss's health
        self.final_boss.final_boss.health = 50

        self.final_boss.final_combat()

        # Verify that the invalid choice message was printed
        mock_print.assert_any_call("Invalid choice. \
Please select a valid action.")

    @patch('builtins.print')
    @patch('builtins.input')
    def test_final_boss_defeated(self, mock_input, mock_print):
        """
        Test the scenario where the player defeats the final boss.
        """
        # Set boss health low enough to be defeated in one hit
        self.final_boss.final_boss.health = 40
        # Player's damage is 50

        mock_input.side_effect = ['0']  # Attack

        self.final_boss.final_combat()

        # Verify that the boss's health is zero or less
        self.assertLessEqual(self.final_boss.final_boss.health, 0)

        # Verify that the victory message was printed
        mock_print.assert_any_call(f"  You defeated the \
{self.final_boss.final_boss.name}!")

    @patch('random.randint')
    @patch('builtins.print')
    @patch('builtins.input')
    def test_player_defeated(self, mock_input, mock_print, mock_randint):
        """
        Test the scenario where the player is defeated by the final boss.
        """
        # Set boss attack damage high enough to defeat the player
        def randint_side_effect(start, end):
            if start == 20 and end == 40:
                return 100  # Boss attack damage
            elif start == 250 and end == 300:
                return 50  # Boss health during initialization
            elif start == 10 and end == 20:
                return 10  # Boss damage during initialization
            else:
                return start  # Default value

        mock_randint.side_effect = randint_side_effect

        # Player health low enough to be defeated
        self.mock_player.health = 50

        # Adjust boss's health so combat ends
        self.final_boss.final_boss.health = 100

        mock_input.side_effect = ['0']  # Attack

        self.final_boss.final_combat()

        # Verify that the player's health is zero or less
        self.assertLessEqual(self.mock_player.health, 0)

        # Verify that the defeat message was printed
        mock_print.assert_any_call("You have fallen in battle...")


if __name__ == '__main__':
    unittest.main()
