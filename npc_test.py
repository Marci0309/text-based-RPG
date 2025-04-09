from rpg.npc import npc, Enemy, Trader, Item
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestNPC(unittest.TestCase):

    def setUp(self):
        """
        Set up an NPC instance for testing.
        """
        self.default_npc = npc(
            name="Old Man",
            description="An old man with a wise look.",
            dialogues={
                "Hello, traveler!": {
                    "options": {
                        "How are you?": ["I am doing well, thank you."],
                        "Goodbye": ["Farewell, traveler."]
                    }
                }
            }
        )

    @patch('builtins.input', side_effect=['0'])
    def test_npc_interact(self, mock_input):
        """
        Test interaction with an NPC.
        """
        player = MagicMock()
        with patch('builtins.print') as mock_print:
            self.default_npc.interact(player)
            mock_print.assert_any_call("\nOld Man says: Hello, traveler!")

    @patch('builtins.print')
    def test_npc_inspect(self, mock_print):
        """
        Test the inspect method of the NPC.
        """
        self.default_npc.inspect()
        mock_print.assert_called_with("NPC: Old Man, Description: \
An old man with a wise look.")

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "npcs": [
            {"name": "Merchant",
             "description": "A friendly trader.", "dialogues": {}}
        ]
    }))
    @patch('os.path.dirname', return_value='.')
    def test_load_npcs_success(self, mock_dirname, mock_file):
        """
        Test loading NPCs from a JSON file.
        """
        npcs = npc.load_npcs()
        self.assertEqual(len(npcs), 1)
        self.assertEqual(npcs[0].name, "Merchant")
        self.assertEqual(npcs[0].description, "A friendly trader.")


class TestEnemy(unittest.TestCase):

    def setUp(self):
        """
        Set up an Enemy instance for testing.
        """
        self.enemy = Enemy(
            name="Goblin",
            description="A small but dangerous creature.",
            health=50,
            damage=10
        )

    def test_enemy_initialization(self):
        """
        Test that the Enemy class initializes correctly.
        """
        self.assertEqual(self.enemy.name, "Goblin")
        self.assertEqual(self.enemy.description,
                         "A small but dangerous creature.")
        self.assertEqual(self.enemy.health, 50)
        self.assertEqual(self.enemy.damage, 10)

    def test_enemy_attack(self):
        """
        Test the attack method of the Enemy.
        """
        player = MagicMock()
        player.health = 40

        result = self.enemy.attack(player)
        self.assertEqual(player.health, 30)  # Player should take 10 damage
        self.assertFalse(result)

        player.health = 5
        result = self.enemy.attack(player)
        self.assertEqual(player.health, -5)  # Player health below zero
        self.assertTrue(result)


class TestTrader(unittest.TestCase):

    def setUp(self):
        """
        Set up a Trader instance for testing.
        """
        self.trader = Trader(
            name="John the Trader",
            description="A seasoned merchant with various items.",
            dialogues={"Welcome!": {"options": {"Goodbye": ["Farewell."]}}},
            items=[
                Item(
                    name="Health Potion",
                    rarity="common",
                    effect_type="health",
                    value=50,
                    description="Restores 50 health.",
                    price=10
                ),
                Item(
                    name="Sword of Strength",
                    rarity="rare",
                    effect_type="damage",
                    value=25,
                    description="Adds 25 damage.",
                    price=50
                )
            ]
        )

    def test_trader_initialization(self):
        """
        Test that the Trader class initializes correctly with items.
        """
        self.assertEqual(self.trader.name, "John the Trader")
        self.assertEqual(len(self.trader.items), 2)
        self.assertEqual(self.trader.items[0].name, "Health Potion")
        self.assertEqual(self.trader.items[1].name, "Sword of Strength")

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "traders": [
            {
                "name": "Merchant Bob",
                "description": "A grumpy trader.",
                "items": [
                    {"name": "Magic Wand",
                     "rarity": "legendary",
                     "effect_type": "damage",
                     "value": 100,
                     "description": "A powerful wand.",
                     "price": 200}
                ]
            }
        ]
    }))
    @patch('os.path.dirname', return_value='.')
    def test_load_traders_success(self, mock_dirname, mock_file):
        """
        Test loading Traders from a JSON file.
        """
        traders = Trader.load_traders()
        self.assertEqual(len(traders), 1)
        self.assertEqual(traders[0].name, "Merchant Bob")
        self.assertEqual(traders[0].items[0].name, "Magic Wand")
        self.assertEqual(traders[0].items[0].price, 200)

    @patch('builtins.input', side_effect=['0'])
    def test_trader_trade_success(self, mock_input):
        """
        Test trading an item with the Trader when the player has enough coins.
        """
        player = MagicMock()
        player.coins = 15
        player.inventory = []

        with patch('builtins.print') as mock_print:
            self.trader.trade(player)
            mock_print.assert_any_call("You have purchased \
Health Potion for10 coins!")
        self.assertEqual(player.coins, 5)
        self.assertEqual(len(player.inventory), 1)
        self.assertEqual(player.inventory[0].name, "Health Potion")

    @patch('builtins.input', side_effect=['0'])
    def test_trader_trade_not_enough_coins(self, mock_input):
        """
        Test trading an item with the Trader
        when the player doesn't have enough coins.
        """
        player = MagicMock()
        player.coins = 5
        player.inventory = []

        with patch('builtins.print') as mock_print:
            self.trader.trade(player)
            mock_print.assert_any_call("You don't have enough \
coins to buy this item.")
        self.assertEqual(player.coins, 5)
        self.assertEqual(len(player.inventory), 0)


if __name__ == '__main__':
    unittest.main()
