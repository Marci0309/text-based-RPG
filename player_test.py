from unittest.mock import patch, MagicMock
from rpg.player import player
from rpg.items import Item
from rpg.enemy import Enemy
from rpg.room import room as Room
from rpg.door import door as Door
from rpg.base_model import Interactable
import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.starting_room = MagicMock(spec=Room)
        self.starting_room.name = 'Starting Room'
        self.starting_room.doors = {}
        self.starting_room.npcs = []
        self.starting_room.traders = []
        self.starting_room.inspect = MagicMock()

        self.player = player(starting_room=self.starting_room,
                             name='TestPlayer')

    @patch('builtins.print')
    def test_initialization(self, mock_print):
        self.assertEqual(self.player.name, 'TestPlayer')
        self.assertEqual(self.player.health, 100)
        self.assertEqual(self.player.damage, 10)
        self.assertEqual(self.player.current_room, self.starting_room)
        self.assertEqual(self.player.visited_rooms, ['Starting Room'])
        self.assertEqual(self.player.coins, 5)
        self.assertEqual(self.player.inventory, [])

    @patch('builtins.print')
    def test_inspect_current_room(self, mock_print):
        self.player.inspect()
        self.starting_room.inspect.assert_called_once()

    @patch('builtins.print')
    def test_interact_no_doors(self, mock_print):
        self.player.current_room.doors = {}
        with patch('builtins.input', return_value='-1'):
            self.player.interact()
        mock_print.assert_any_call("There are no doors in this room.")

    @patch('builtins.print')
    def test_interact_choose_door(self, mock_print):
        destination_room = MagicMock(spec=Room)
        destination_room.name = 'Destination Room'
        destination_room.doors = {}
        destination_room.npcs = []
        destination_room.traders = []
        destination_room.inspect = MagicMock()
        destination_room.add_doors = MagicMock()

        door = MagicMock(spec=Door)
        door.name = 'Door to Destination'
        door.description = 'A door leading to the destination room.'
        door.destination = destination_room

        self.player.current_room.doors = {'door1': door}

        with patch('builtins.input', return_value='0'):
            self.player.interact()

        self.assertEqual(self.player.current_room, destination_room)
        self.assertEqual(self.player.visited_rooms, ['Starting Room',
                                                     'Destination Room'])
        self.assertEqual(self.player.coins, 6)

        destination_room.inspect.assert_called_once()

    @patch('builtins.print')
    def test_interact_invalid_choice(self, mock_print):
        door = MagicMock(spec=Door)
        door.name = 'Door to Nowhere'
        door.description = 'A mysterious door that leads nowhere.'
        door.destination = None

        self.player.current_room.doors = {'door1': door}

        with patch('builtins.input', return_value='invalid'):
            self.player.interact()

        mock_print.assert_any_call("Invalid choice. \
Please select a valid door number.")

    @patch('builtins.print')
    def test_look_for_company_no_npcs(self, mock_print):
        self.player.current_room.npcs = []
        self.player.look_for_company()
        mock_print.assert_any_call("Unfortunately, there are no NPCs here.")

    @patch('builtins.print')
    def test_look_for_company_with_npcs(self, mock_print):
        npc = MagicMock(spec=Interactable)
        npc.name = 'Friendly NPC'
        npc.description = 'A friendly character.'
        npc.interact = MagicMock()

        self.player.current_room.npcs = [npc]

        with patch('builtins.input', return_value='0'):
            self.player.look_for_company()

        npc.interact.assert_called_once_with(self.player)

    @patch('builtins.print')
    def test_look_for_company_invalid_choice(self, mock_print):
        npc = MagicMock(spec=Interactable)
        npc.name = 'Friendly NPC'
        npc.description = 'A friendly character.'
        npc.interact = MagicMock()

        self.player.current_room.npcs = [npc]

        with patch('builtins.input', return_value='invalid'):
            self.player.look_for_company()

        mock_print.assert_any_call("Invalid choice. \
Please select a valid character number.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_no_monsters(self, mock_load_monsters, mock_print):
        mock_load_monsters.return_value = []

        with patch('random.randint', return_value=0):
            self.player.look_for_fight()

        mock_print.assert_any_call("     There are no monsters \
to fight right now.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_with_monster(self, mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Goblin'
        monster.description = 'A nasty goblin.'
        monster.health = 10
        monster.damage = 5
        monster.difficulty = 'easy'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', return_value=1):
            with patch('builtins.input',
                       side_effect=['0', '0', '0', '0', '0', '0']):
                self.player.look_for_fight()

        self.assertIn('Goblin', self.player.defeated_enemy)
        self.assertEqual(self.player.coins, 7)

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_run_away(self, mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Orc'
        monster.description = 'A fierce orc.'
        monster.health = 50
        monster.damage = 10
        monster.difficulty = 'medium'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', return_value=1):
            with patch('builtins.input', side_effect=['0', '4']):
                self.player.look_for_fight()

        self.assertEqual(self.player.health, 50)
        self.assertNotIn('Orc', self.player.defeated_enemy)
        mock_print.assert_any_call(f"     \nYou ran away \
but lost {50.0} health. Your current health is 50.0.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_heal_before_action_count(self,
                                                     mock_load_monsters,
                                                     mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Skeleton'
        monster.description = 'A creepy skeleton.'
        monster.health = 20
        monster.damage = 5
        monster.difficulty = 'easy'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', side_effect=[1, 15]):
            with patch('builtins.input',
                       side_effect=['0', '2', '0', '0', '0']):
                self.player.look_for_fight()

        mock_print.assert_any_call("     \nYou need to take \
3 actions before healing again.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_heal_after_action_count(self, mock_load_monsters,
                                                    mock_print):
        """
        Test healing during combat after action count reaches 3.
        """
        # Create a mock monster
        monster = MagicMock(spec=Enemy)
        monster.name = 'Zombie'
        monster.description = 'A slow-moving zombie.'
        monster.health = 20
        monster.damage = 5
        monster.difficulty = 'easy'

        mock_load_monsters.return_value = [monster]

        # Set action_count to 3 to allow healing
        self.player.action_count = 3
        # Set player health to less than 100
        self.player.health = 70

        # Force num_monsters to be 1 and heal amount
        with patch('random.randint', side_effect=[1, 25]):
            with patch('builtins.input',
                       side_effect=['0', '2', '0', '0', '0']):
                self.player.look_for_fight()

        # Assert that the heal was performed and health increased
        # Health was 70, healed by 25, then took 5 damage twice
        self.assertEqual(self.player.health, 85)
        mock_print.assert_any_call("     \nYou healed yourself for 25 health! \
Your current health is 95.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_use_item(self, mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Bandit'
        monster.description = 'A sneaky bandit.'
        monster.health = 30
        monster.damage = 7
        monster.difficulty = 'medium'

        mock_load_monsters.return_value = [monster]

        damage_item = MagicMock(spec=Item)
        damage_item.name = 'Sharp Dagger'
        damage_item.effect_type = 'damage'
        damage_item.value = 5
        damage_item.description = 'Increases damage.'
        self.player.inventory = [damage_item]

        with patch('random.randint', return_value=1):
            with patch('builtins.input',
                       side_effect=['0', '3', '0', '0', '0', '0']):
                self.player.look_for_fight()

        self.assertEqual(self.player.damage, 15)
        self.assertEqual(len(self.player.inventory), 0)

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_invalid_action(self,
                                           mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Troll'
        monster.description = 'A big troll.'
        monster.health = 40
        monster.damage = 8
        monster.difficulty = 'hard'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', return_value=1):
            with patch('builtins.input',
                       side_effect=['0', 'invalid', '0', '0', '0', '0']):
                self.player.look_for_fight()

        mock_print.assert_any_call("Invalid choice. \
Please select a valid action.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_player_defeated(self,
                                            mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Dragon'
        monster.description = 'A fearsome dragon.'
        monster.health = 200
        monster.damage = 100
        monster.difficulty = 'hard'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', return_value=1):
            with patch('builtins.input', side_effect=['0', '0']):
                with self.assertRaises(SystemExit):
                    self.player.look_for_fight()

        self.assertLessEqual(self.player.health, 0)
        mock_print.assert_any_call("     \nYou have been defeated!")
        mock_print.assert_any_call("Game Over!")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_monster_defeated(self,
                                             mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Rat'
        monster.description = 'A small rat.'
        monster.health = 5
        monster.damage = 1
        monster.difficulty = 'easy'

        mock_load_monsters.return_value = [monster]

        with patch('random.randint', return_value=1):
            with patch('builtins.input', side_effect=['0', '0']):
                self.player.look_for_fight()

        self.assertIn('Rat', self.player.defeated_enemy)
        mock_print.assert_any_call(f"     \nYou defeated {monster.name}!")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_no_more_monsters(self,
                                             mock_load_monsters, mock_print):
        monster = MagicMock(spec=Enemy)
        monster.name = 'Spider'
        monster.description = 'A giant spider.'
        monster.health = 15
        monster.damage = 3
        monster.difficulty = 'easy'

        mock_load_monsters.return_value = [monster]

        self.player.defeated_enemy.append('Spider')

        with patch('random.randint', return_value=1):
            self.player.look_for_fight()

        mock_print.assert_any_call("     There are no more \
monsters to fight in this room.")

    @patch('builtins.print')
    @patch('rpg.enemy.Enemy.load_monsters')
    def test_look_for_fight_already_fought_in_room(self,
                                                   mock_load_monsters,
                                                   mock_print):
        room_name = self.player.current_room.name
        self.player.fought_in_room[room_name] = True

        self.player.look_for_fight()

        mock_print.assert_any_call("     There are no \
more enemies in this room.")

    @patch('builtins.print')
    def test_look_for_company_with_enemy_npc(self, mock_print):
        enemy_npc = MagicMock(spec=Enemy)
        enemy_npc.name = 'Bandit Leader'
        enemy_npc.description = 'A dangerous bandit.'
        enemy_npc.health = 10
        enemy_npc.damage = 1
        enemy_npc.difficulty = 'medium'

        self.player.current_room.npcs = [enemy_npc]

        with patch('builtins.input',
                   side_effect=['0', '0', '0', '0', '0', '0']):
            self.player.look_for_company()

        self.assertIn('Bandit Leader', self.player.defeated_enemy)

    @patch('builtins.print')
    def test_show_inventory_and_use_item_negative_index(self, mock_print):
        """
        Test attempting to use an item with a negative index (other than -1).
        """
        # Add an item to the inventory
        item = MagicMock(spec=Item)
        item.name = 'Shield'
        item.effect_type = 'defense'
        item.value = 5
        item.description = 'Increases defense.'

        self.player.inventory = [item]

        with patch('builtins.input', side_effect=['0', '-2']):
            result = self.player.show_inventory_and_use_item()

        # Assert that the item was not used
        self.assertFalse(result)
        self.assertEqual(len(self.player.inventory), 1)
        mock_print.assert_any_call("Invalid item selection. \
Please choose a valid item index or -1 to go back.")

    @patch('builtins.print')
    def test_show_inventory_and_use_item_return_to_menu(self, mock_print):
        item = MagicMock(spec=Item)
        item.name = 'Helmet'
        item.effect_type = 'defense'
        item.value = 3
        item.description = 'Protects your head.'

        self.player.inventory = [item]

        with patch('builtins.input', side_effect=['0', '-1']):
            result = self.player.show_inventory_and_use_item()

        self.assertFalse(result)
        self.assertEqual(len(self.player.inventory), 1)
        mock_print.assert_any_call("Returning to menu.")

    @patch('builtins.print')
    def test_interact_with_trader_invalid_choice(self, mock_print):
        trader = MagicMock()
        trader.name = 'Trader Bob'
        trader.description = 'Sells rare items.'
        trader.trade = MagicMock()

        self.player.current_room.traders = [trader]

        with patch('builtins.input', side_effect=['invalid', '1']):
            self.player.interact_with_trader()

        trader.trade.assert_not_called()
        mock_print.assert_any_call("Invalid choice. \
Please answer with '0' (Yes) or '1' (No).")

    @patch('builtins.print')
    def test_look_for_items_no_items_found(self, mock_print):
        with patch('rpg.items.Item.load_items', return_value=[]):
            with patch('random.randint', return_value=1):
                self.player.look_for_items()

        self.assertEqual(len(self.player.inventory), 0)
        mock_print.assert_any_call("No items found.")
        self.assertTrue(self.player.looked_for_items)

    @patch('builtins.print')
    def test_show_inventory_and_use_item_no_use(self, mock_print):
        item = MagicMock(spec=Item)
        item.name = 'Elixir'
        item.effect_type = 'health'
        item.value = 50
        item.description = 'Restores a large amount of health.'

        self.player.inventory = [item]

        with patch('builtins.input', side_effect=['1']):
            result = self.player.show_inventory_and_use_item()

        self.assertFalse(result)
        self.assertEqual(len(self.player.inventory), 1)
        mock_print.assert_any_call("You chose not to use any items.")

    @patch('builtins.print')
    def test_interact_with_trader_multiple_times(self, mock_print):
        trader = MagicMock()
        trader.name = 'Merchant Mary'
        trader.description = 'Sells various goods.'
        trader.trade = MagicMock()

        self.player.current_room.traders = [trader]

        with patch('builtins.input', side_effect=['0', '0']):
            self.player.interact_with_trader()
            self.player.interact_with_trader()

        self.assertEqual(trader.trade.call_count, 2)


if __name__ == '__main__':
    unittest.main()
