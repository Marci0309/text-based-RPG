from .base_model import Interactable, Inspectable
import json
import os
from .items import Item


class npc(Interactable, Inspectable):
    def __init__(
            self,
            name: str,
            description: str,
            dialogues: dict = None
            ) -> None:
        """
        Initialize an NPC object.

        Args:
            name (str): The name of the NPC.
            description (str): A brief description of the NPC.
            dialogues (dict, optional): A dictionary of dialogues
            the NPC can have (default is None).

        Returns:
            None
        """
        self.name = name
        self.description = description
        self.dialogues = dialogues if dialogues is not None else {}

    def interact(self, player) -> None:
        """
        Handle the interaction with the player. NPC starts the dialogue,
        and the player chooses a response.

        Args:
            player: The player object interacting with the NPC.

        Returns:
            None
        """
        dialogue_keys = list(self.dialogues.keys())
        selected_dialogue = dialogue_keys[0]
        print(f"\n{self.name} says: {selected_dialogue}")

        responses = self.dialogues[selected_dialogue]['options']

        for index, response in enumerate(responses.keys()):
            print(f"  ({index}) {response}")

        response_choice = input(
            "Select a response by number (or -1 to go back): "
            )

        if response_choice == '-1':
            print("You have chosen to end the conversation.")
            return

        if response_choice.isdigit():
            if 0 <= int(response_choice) < len(responses):
                response_index = int(response_choice)
                selected_response_key = list(responses.keys())[response_index]
            print(
                f"\n{self.name} responds:\
                {responses[selected_response_key][0]}"
                )
        else:
            print("Invalid choice.")

    def inspect(self) -> None:
        """
        Provide a brief description of the NPC.

        Args:
            None

        Returns:
            None
        """
        print(f"NPC: {self.name}, Description: {self.description}")

    @classmethod
    def load_npcs(cls) -> list:
        """
        Load NPCs from a JSON file.

        Args:
            None

        Returns:
            list: A list of NPC objects loaded from the JSON file.
        """
        base_dir = os.path.dirname(__file__)
        npcs_file = os.path.join(base_dir, 'npc_diaologues.json')

        try:
            with open(npcs_file, 'r') as f:
                npc_data = json.load(f)
                return [
                    cls(
                        name=npc['name'],
                        description=npc['description'],
                        dialogues=npc['dialogues']
                        ) for npc in npc_data['npcs']
                    ]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading NPCs: {e}")
            return []


class Enemy(npc):
    def __init__(
            self,
            name: str,
            description: str,
            health: int,
            damage: int
            ) -> None:
        """
        Initialize an Enemy object, inheriting from NPC.

        Args:
            name (str): The name of the enemy.
            description (str): A brief description of the enemy.
            health (int): The health points of the enemy.
            damage (int): The damage the enemy can inflict.

        Returns:
            None
        """
        super().__init__(name, description)
        self.health = health
        self.damage = damage

    def attack(self, player) -> bool:
        """
        Attack the player,
        reducing their health and checking if the player has been defeated.

        Args:
            player: The player object being attacked by the enemy.

        Returns:
            bool: True if the player has been defeated, False otherwise.
        """
        print(f"{self.name} attacks you for {self.damage} damage!")
        player.health -= self.damage
        if player.health <= 0:
            print(f"You have been defeated by {self.name}!")
            return True  # Indicates the player has died
        return False


class Trader(npc):
    def __init__(
            self,
            name: str,
            description: str,
            dialogues: dict = None,
            items: list = None
            ) -> None:
        """
        Initialize a Trader object, inheriting from NPC.

        Args:
            name (str): The name of the trader.
            description (str): A brief description of the trader.
            dialogues (dict, optional):
            A dictionary of dialogues the trader can have (default is None).
            items (list, optional):
            A list of items the trader has for sale (default is None).

        Returns:
            None
        """
        super().__init__(name, description, dialogues)
        self.items = items if items is not None else []

    @classmethod
    def load_traders(cls) -> list:
        """
        Load traders from a JSON file and return a list of Trader instances.

        Args:
            None

        Returns:
            list: A list of Trader objects loaded from the JSON file.
        """
        base_dir = os.path.dirname(__file__)
        traders_file = os.path.join(base_dir, 'npc_diaologues.json')

        try:
            with open(traders_file, 'r') as f:
                trader_data = json.load(f)
                traders = []
                for trader in trader_data['traders']:
                    # Convert each item dictionary into an Item object
                    items = []
                    for item in trader.get('items', []):
                        # Enforce conversion from dict to Item object
                        if isinstance(item, dict):
                            item_object = Item.from_dict(item)
                            items.append(item_object)
                        else:
                            print(
                                "Warning:"
                                f"Item is not a valid dictionary: {item}"
                            )

                    traders.append(cls(
                        name=trader['name'],
                        description=trader['description'],
                        dialogues=trader.get('dialogues', {}),
                        items=items
                    ))
                return traders
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading traders: {e}")
            return []

    def trade(self, player) -> None:
        """
        Offer items for sale to the player, allowing them to
        purchase items if they have enough coins.

        Args:
            player: The player object interacting with the trader.

        Returns:
            None
        """
        print(
            f"{self.name}: "
            "'Welcome to my shop! Here are the items I have for sale:'"
            )

        for index, item in enumerate(self.items):
            extra_effect = ''
            if item.effect_type == 'health':
                extra_effect = f", Adds extra: {item.value} health"
            elif item.effect_type == 'damage':
                extra_effect = f", Adds extra: {item.value} damage"

            print(
                f"\n {index}: {item.name} - {item.price} \
coins: {item.description}"
                f"{extra_effect}")
        choice = input("Select an item to buy by number (or -1 to leave): ")
        if choice.isdigit() and 0 <= int(choice) < len(self.items):
            item_to_buy = self.items[int(choice)]
            if player.coins >= item_to_buy.price:
                player.coins -= item_to_buy.price
                player.inventory.append(item_to_buy)
                print(
                    f"You have purchased {item_to_buy.name} for\
{item_to_buy.price} coins!"
                    )
            else:
                print("You don't have enough coins to buy this item.")
        elif choice == '-1':
            print("Thank you for visiting!")
        else:
            print("Invalid choice. Please select a valid item number.")
