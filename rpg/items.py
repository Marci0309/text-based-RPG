import json
import os


class Item:
    def __init__(
            self,
            name: str,
            rarity: str, effect_type: str,
            value: int,
            description: str,
            price: int
            ) -> None:
        """
        Initialize an Item object.

        Args:
            name (str): The name of the item.
            rarity (str): The rarity level of the item.
            effect_type (str):
            The type of effect the item has ('health' or 'damage').
            value (int): The value of the item's effect.
            description (str): A brief description of the item.
            price (int): The price of the item in the game's currency.

        Returns:
            None
        """
        self.name = name
        self.rarity = rarity
        self.effect_type = effect_type  # 'health' or 'damage'
        self.value = value
        self.description = description
        self.price = price

    def to_dict(self) -> dict:
        """
        Convert the item object into a dictionary representation.

        Args:
            None

        Returns:
            dict: A dictionary containing the item's attributes.
        """
        return {
            'name': self.name,
            'rarity': self.rarity,
            'effect_type': self.effect_type,
            'value': self.value,
            'description': self.description,
            'price': self.price
        }

    @classmethod
    def from_dict(cls, item_dict: dict) -> 'Item':
        """
        Create an Item object from a dictionary.

        Args:
            item_dict (dict): A dictionary containing the item's attributes.

        Returns:
            Item: An instance of the Item class created from the dictionary.
        """
        return cls(
            item_dict['name'],
            item_dict['rarity'],
            item_dict['effect_type'],
            item_dict['value'],
            item_dict['description'],
            item_dict['price']
        )

    @classmethod
    def load_items(cls) -> list:
        """
        Load items from a JSON file and return a list of Item instances.

        Args:
            None

        Returns:
            list: A list of Item objects loaded from the JSON file.
        """
        base_dir = os.path.dirname(__file__)
        items_file = os.path.join(base_dir, 'items.json')

        try:
            with open(items_file, 'r') as f:
                item_data = json.load(f)
                return [
                    cls(
                        item['name'],
                        item['rarity'],
                        item['effect_type'],
                        item['value'],
                        item["description"],
                        item["price"]
                        ) for item in item_data['items']
                    ]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading items: {e}")
            return []
