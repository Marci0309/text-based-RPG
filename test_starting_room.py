from rpg.starting_room import StartingRoom
import unittest
from unittest.mock import patch, mock_open
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestStartingRoom(unittest.TestCase):

    def setUp(self):
        """
        Set up a StartingRoom instance for testing.
        """
        self.starting_room = StartingRoom()
        self.starting_room.player_name = 'TestPlayer'

    @patch('builtins.print')
    def test_initialization(self, mock_print):
        """
        Test that the StartingRoom class
        initializes with the correct default values.
        """
        sr = StartingRoom()
        self.assertTrue(sr.npc_present)
        self.assertTrue(sr.door_locked)
        self.assertFalse(sr.has_interacted_with_npc)
        self.assertIsNone(sr.player_name)
        self.assertFalse(sr.defeated)
        self.assertEqual(sr.health, 100)
        self.assertEqual(sr.heal_used, 0)
        self.assertEqual(sr.action_count, 3)
        self.assertFalse(sr.told)
        self.assertFalse(sr.wrong)

    @patch('builtins.input', side_effect=['', 'ExistingPlayer', 'NewPlayer'])
    @patch('builtins.print')
    @patch('rpg.starting_room.StartingRoom.load_saved_players',
           return_value=['ExistingPlayer'])
    def test_ask_player_name(self,
                             mock_load_saved_players, mock_print, mock_input):
        """
        Test the ask_player_name method with different scenarios:
        - Empty input
        - Name already taken
        - Valid new name
        """
        self.starting_room.ask_player_name()
        self.assertEqual(self.starting_room.player_name, 'NewPlayer')
        self.assertEqual(mock_input.call_count, 3)
        mock_print.assert_any_call("Please enter a valid name.")
        mock_print.assert_any_call("The name 'ExistingPlayer' is \
already taken. Please choose a different name.")
        mock_print.assert_any_call("\nAh, NewPlayer! \
A fine name you have indeed!")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open',
           new_callable=mock_open,
           read_data=json.dumps({"Player1": {}, "Player2": {}}))
    def test_load_saved_players(self, mock_file, mock_exists):
        """
        Test that load_saved_players correctly loads saved player names.
        """
        saved_players = self.starting_room.load_saved_players()
        self.assertEqual(set(saved_players), {'Player1', 'Player2'})

    @patch('os.path.exists', return_value=False)
    def test_load_saved_players_no_file(self, mock_exists):
        """
        Test that load_saved_players returns
        an empty dict when the save file does not exist.
        """
        saved_players = self.starting_room.load_saved_players()
        self.assertEqual(saved_players, {})

    @patch('builtins.print')
    def test_show_room_description(self, mock_print):
        """
        Test that the show_room_description
        method prints the correct description.
        """
        self.starting_room.show_room_description()
        mock_print.assert_called_with("\tTestPlayer, you find \
yourself in a small room with one"
                                      "door. You are probably \
wondering how you got here, but that's "
                                      "for you to find out, adventurer.")

    @patch('builtins.input', side_effect=['0'])
    @patch('builtins.print')
    def test_interact_with_npc_first_time(self, mock_print, mock_input):
        """
        Test interacting with the NPC for the first time.
        """
        self.starting_room.defeated = False
        with patch.object(self.starting_room,
                          'offer_additional_options') as mock_offer_options, \
             patch.object(self.starting_room,
                          'start_combat_tutorial') as mock_combat_tutorial:
            self.starting_room.interact_with_npc()
            mock_print.assert_any_call("\nGame guide: Greetings, TestPlayer! \
I see you're ready for the adventure ahead.'")
            mock_offer_options.assert_called()
            mock_combat_tutorial.assert_called()
            self.assertTrue(self.starting_room.has_interacted_with_npc)
            # Door should be unlocked after interaction
            self.assertFalse(self.starting_room.door_locked)

    @patch('builtins.input', side_effect=['1', '0', '0'])
    @patch('builtins.print')
    def test_interact_with_npc_additional_options(self,
                                                  mock_print, mock_input):
        """
        Test interacting with the NPC and choosing to ask something else.
        """
        self.starting_room.defeated = False
        with patch.object(self.starting_room,
                          'offer_additional_options') as mock_offer_options, \
             patch.object(self.starting_room,
                          'start_combat_tutorial') as mock_combat_tutorial:
            self.starting_room.interact_with_npc()
            self.assertEqual(mock_offer_options.call_count, 2)
            mock_combat_tutorial.assert_called()
            self.assertTrue(self.starting_room.has_interacted_with_npc)
            self.assertFalse(self.starting_room.door_locked)

    @patch('builtins.print')
    def test_interact_with_npc_after_defeat(self, mock_print):
        """
        Test interacting with the NPC after defeating the dummy.
        """
        self.starting_room.defeated = True
        self.starting_room.told = False
        self.starting_room.interact_with_npc()
        mock_print.assert_any_call("\nGame guide: 'Well done, adventurer! \
You've proven your mettle. The door is now unlocked.'")
        self.assertFalse(self.starting_room.door_locked)
        self.assertTrue(self.starting_room.told)

    @patch('builtins.print')
    def test_try_open_door_locked(self, mock_print):
        """
        Test trying to open the door when it's locked.
        """
        self.starting_room.door_locked = True
        result = self.starting_room.try_open_door()
        self.assertFalse(result)
        mock_print.assert_called_with("\nThe door is locked, TestPlayer. \
Perhaps you should talk to the Game guide first.")

    @patch('builtins.print')
    def test_try_open_door_unlocked(self, mock_print):
        """
        Test trying to open the door when it's unlocked.
        """
        self.starting_room.door_locked = False
        result = self.starting_room.try_open_door()
        self.assertTrue(result)
        mock_print.assert_called_with("\nThe door creaks open, TestPlayer. \
You step through into the next phase of your adventure.")

    @patch('builtins.input', side_effect=['4'])
    @patch('builtins.print')
    def test_run_exit_game(self, mock_print, mock_input):
        """
        Test that the game exits when the player chooses to exit.
        """
        with patch.object(self.starting_room,
                          'ask_player_name') as mock_ask_name, \
             patch.object(self.starting_room,
                          'show_room_description') as mock_show_description, \
             self.assertRaises(SystemExit):
            self.starting_room.run()
            mock_ask_name.assert_called()
            mock_show_description.assert_called()
        mock_print.assert_any_call("Exiting game...")

    @patch('builtins.input', side_effect=['1', '2', '4'])
    @patch('builtins.print')
    def test_run_interact_then_exit(self, mock_print, mock_input):
        """
        Test running the game where the player
        interacts with the NPC and then exits.
        """
        with patch.object(self.starting_room,
                          'ask_player_name') as mock_ask_name, \
             patch.object(self.starting_room,
                          'show_room_description') as mock_show_description, \
             patch.object(self.starting_room,
                          'interact_with_npc') as mock_interact_with_npc, \
             self.assertRaises(SystemExit):
            self.starting_room.run()
            mock_ask_name.assert_called()
            mock_show_description.assert_called()
            mock_interact_with_npc.assert_called()
        mock_print.assert_any_call("Exiting game...")

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_offer_additional_options_valid_choice(self,
                                                   mock_print, mock_input):
        """
        Test offering additional options with a valid choice.
        """
        self.starting_room.offer_additional_options()
        expected_output = "\nGame guide: This is the starting room. \
My purpose is\n    to teach you what you can do throughout the game."
        printed_outputs = [call_args[0][0]
                           for call_args in mock_print.call_args_list]
        self.assertIn(expected_output, printed_outputs)

    @patch('builtins.input', side_effect=['0', '1'])
    @patch('builtins.print')
    def test_offer_additional_options_invalid_choice(self,
                                                     mock_print, mock_input):
        """
        Test offering additional options with an invalid choice.
        """
        self.starting_room.offer_additional_options()
        mock_print.assert_any_call("\nGame guide: \
'That's not a valid choice, adventurer. Choose wisely next time!'")

    @patch('builtins.input', side_effect=['0', '0', '0'])
    @patch('builtins.print')
    def test_start_combat_tutorial_attack_to_win(self, mock_print, mock_input):
        """
        Test that the player can defeat the dummy by
        attacking until the enemy is defeated.
        """
        self.starting_room.health = 100
        self.starting_room.start_combat_tutorial()
        expected_health = 90
        self.assertEqual(self.starting_room.health, expected_health)
        self.assertTrue(self.starting_room.defeated)

    @patch('builtins.input', side_effect=['2', '0', '0', '0'])
    @patch('builtins.print')
    def test_start_combat_tutorial_heal(self, mock_print, mock_input):
        """
        Test that the player can heal during combat.
        """
        self.starting_room.health = 80
        self.starting_room.action_count = 3  # Ensure heal is allowed
        with patch('random.randint', return_value=15):  # Control heal amount
            self.starting_room.start_combat_tutorial()
            expected_health = 80
            self.assertEqual(self.starting_room.health, expected_health)
            self.assertTrue(self.starting_room.defeated)

    @patch('builtins.input', side_effect=['1', '0', '0', '0'])
    @patch('builtins.print')
    def test_start_combat_tutorial_defend(self, mock_print, mock_input):
        """
        Test that defending reduces damage from the next attack.
        """
        self.starting_room.health = 100
        self.starting_room.start_combat_tutorial()
        expected_health = 88
        self.assertEqual(self.starting_room.health, expected_health)
        self.assertTrue(self.starting_room.defeated)

    @patch('builtins.input', side_effect=['2', '0', '0', '0'])
    @patch('builtins.print')
    def test_start_combat_tutorial_heal_not_allowed(self,
                                                    mock_print, mock_input):
        """
        Test that the player cannot heal when action_count is less than 3.
        """
        self.starting_room.health = 80
        self.starting_room.action_count = 1  # Not enough actions to heal
        with patch('random.randint', return_value=15):  # Control heal amount
            self.starting_room.start_combat_tutorial()
            expected_health = 65
            self.assertEqual(self.starting_room.health, expected_health)
            self.assertTrue(self.starting_room.defeated)
            mock_print.assert_any_call("\nYou cannot \
heal again in this combat!")

    @patch('builtins.input', side_effect=['3'])
    @patch('builtins.print')
    def test_start_combat_tutorial_run_away(self, mock_print, mock_input):
        """
        Test that running away exits the combat.
        """
        self.starting_room.health = 100
        self.starting_room.start_combat_tutorial()
        self.assertEqual(self.starting_room.health, 50)
        self.assertFalse(self.starting_room.defeated)
        mock_print.assert_any_call("\nCome oooonn! \
You can do better than that!")


if __name__ == '__main__':
    unittest.main()
