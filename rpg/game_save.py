import json
import os
from rpg.items import Item


def save_game(player_instance, filename: str = "game_save.json") -> None:
    """
    Save the player's game data to a JSON file.

    Args:
        player_instance: The player object containing the game state to save.
        filename (str, optional): The name of the file to save the game data
        (default is "game_save.json").

    Returns:
        None
    """
    # Convert items to a list of dictionaries
    inventory_data = [item.to_dict() for item in player_instance.inventory]

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            all_game_data = json.load(f)
    else:
        all_game_data = {}

    game_data = {
        "name": player_instance.name,
        "health": player_instance.health,
        "damage": player_instance.damage,
        "visited_rooms": player_instance.visited_rooms,
        "heal_used": player_instance.heal_used,
        "action_count": player_instance.action_count,
        "defeated_enemy": player_instance.defeated_enemy,
        "inventory": inventory_data,
        "coins": player_instance.coins
    }

    all_game_data[player_instance.name] = game_data

    # Write the updated data back to the JSON file
    with open(filename, 'w') as f:
        json.dump(all_game_data, f, indent=4)

    print(f"Game for player {player_instance.name} saved successfully!")


def load_game(
        player_instance,
        player_name: str,
        filename: str = "game_save.json"
        ) -> None:
    """
    Load the player's game data from a JSON file.

    Args:
        player_instance: The player object to load the game data into.
        player_name (str): The name of the player whose game data to load.
        filename (str, optional): The name of the file to load the game data
        from (default is "game_save.json").

    Returns:
        None
    """
    try:
        with open(filename, 'r') as f:
            all_game_data = json.load(f)

        if player_name not in all_game_data:
            print(f"No saved game found for player {player_name}.")
            return

        game_data = all_game_data[player_name]

        player_instance.inventory = [
            Item.from_dict(item) for item in game_data["inventory"]
            ]
        player_instance.name = game_data["name"]
        player_instance.health = game_data["health"]
        player_instance.damage = game_data["damage"]
        player_instance.visited_rooms = game_data["visited_rooms"]
        player_instance.heal_used = game_data["heal_used"]
        player_instance.action_count = game_data["action_count"]
        player_instance.defeated_enemy = game_data["defeated_enemy"]
        player_instance.coins = game_data["coins"]

        print(f"Game for player {player_name} loaded successfully!")
    except FileNotFoundError:
        print(f"No save file found at {filename}. Starting a new game.")
