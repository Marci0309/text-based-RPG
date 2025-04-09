import json
import os
from .base_model import Interactable, Inspectable


class Enemy(Inspectable, Interactable):
    def __init__(
            self,
            name: str,
            description: str,
            health: int,
            damage: int,
            difficulty: str
            ) -> None:
        """
        Initialize an Enemy object.

        Args:
            name (str): The name of the enemy.
            description (str): A brief description of the enemy.
            health (int): The health points of the enemy.
            damage (int): The damage the enemy can inflict.
            difficulty (str): The difficulty level of the enemy.

        Returns:
            None
        """
        super().__init__()
        self.name = name
        self.description = description
        self.health = health
        self.damage = damage
        self.difficulty = difficulty
        self.defeated_monsters = []

    def inspect(self) -> None:
        """
        Provide a description of the enemy.

        Args:
            None

        Returns:
            None
        """
        print(
            f"{self.name}:"
            f"{self.description}, Health: {self.health}, Damage: {self.damage}"
            )

    def interact(self, player) -> None:
        """
        Interact with the player,
        initiating combat if the enemy has not been defeated.

        Args:
            player: The player object engaging with the enemy.

        Returns:
            None
        """
        if self.name not in self.defeated_monsters:
            print(f"A wild {self.name} appears!")
            player.start_combat(self)
            self.defeated_monsters.append(self.name)

    def attack(self, player) -> bool:
        """
        Enemy attacks the player, checking if the player has been defeated.

        Args:
            player: The player object being attacked by the enemy.

        Returns:
            bool: True if the player has been defeated,
            False if the player is still alive.
        """
        if player.health <= 0:
            print("You have been defeated by the enemy!")
            return True
        return False

    @classmethod
    def load_monsters(cls) -> list:
        """
        Load monsters from a JSON file and return a list of Enemy instances.

        Args:
            None

        Returns:
            list: A list of Enemy objects loaded from the JSON file.
        """
        base_dir = os.path.dirname(__file__)
        monsters_file = os.path.join(base_dir, 'monsters.json')

        try:
            with open(monsters_file, 'r') as f:
                monster_data = json.load(f)
                return [
                    cls(
                        monster['name'],
                        monster['description'],
                        monster['health'],
                        monster['damage'],
                        monster['difficulty']
                    ) for monster in monster_data['monsters']
                ]

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading monsters: {e}")
            return []
