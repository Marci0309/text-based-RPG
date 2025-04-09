import random
import os
import json
from .base_model import Interactable, Inspectable
from .door import door
from .npc import npc, Trader
from .items import Item


class room(Inspectable, Interactable):
    # Load descriptions from JSON file
    base_dir = os.path.dirname(__file__)
    descriptions_file = os.path.join(base_dir, 'descriptions.json')

    try:
        with open(descriptions_file, 'r') as f:
            descriptions_data = json.load(f)
            room_descriptions = descriptions_data['room_descriptions']
            door_descriptions = descriptions_data['door_descriptions']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading descriptions: {e}")
        room_descriptions = ["An empty room."]
        door_descriptions = ["A plain door."]

    def __init__(self, name: str, description: str = None) -> None:
        """
        Initialize a Room object.

        Args:
            name (str): The name of the room.
            description (str, optional): A description of the room.
                Defaults to None, which selects a random description.

        Returns:
            None
        """
        super().__init__()
        self.name = name
        # Set a default room description if none is provided
        self.description = (random.choice(self.room_descriptions)
                            if description is None else description)
        self.doors = {}
        self.items = []
        self.characters = []
        self.monsters = []
        self.locked = False
        self.npcs = []
        self.traders = []  # Use plural for clarity
        self.initialize_npcs()  # Initialize NPCs

    def add_doors(self, existing_rooms: list) -> None:
        """
        Add a random number of doors to the room.

        Args:
            existing_rooms (list): A list of rooms that already exist.

        Returns:
            None
        """
        num_doors = random.randint(2, 4)  # Generate a random number of doors
        descriptions = self.door_descriptions.copy()
        random.shuffle(descriptions)

        for i in range(num_doors):
            door_name = f"Door {i + 1}"
            if descriptions:
                door_description = descriptions.pop()
            else:
                door_description = "A simple door."
            destination_room_name = (f"Room {len(existing_rooms) + 1}")
            # Create a new room for the door
            destination_room = room(destination_room_name)

            # Add the door to the current room
            self.doors[door_name] = door(
                name=door_name, description=door_description,
                destination=destination_room
            )

    def initialize_npcs(self) -> None:
        """
        Initialize a random number of NPCs in the room (0 to 3) and ensure
        only one trader is present.

        Args:
            None

        Returns:
            None
        """
        npcs_file = os.path.join(
            os.path.dirname(__file__), 'npc_diaologues.json'
        )

        try:
            with open(npcs_file, 'r') as f:
                npc_data = json.load(f)

                # Initialize NPCs
                num_npcs = random.randint(0, 3)
                selected_npcs = random.sample(
                    npc_data['npcs'], min(num_npcs, len(npc_data['npcs']))
                )
                for npc_info in selected_npcs:
                    new_npc = npc(
                        name=npc_info['name'],
                        description=npc_info['description'],
                        dialogues=npc_info['dialogues']
                    )
                    self.npcs.append(new_npc)

                # Ensure only one trader is added
                if not self.traders:
                    num_traders = 1
                    if num_traders == 1:
                        selected_trader = random.choice(npc_data['traders'])
                        new_trader = Trader(
                            name=selected_trader['name'],
                            description=selected_trader['description'],
                            dialogues=selected_trader['dialogues'],
                            items=[
                                Item.from_dict(item)
                                for item in selected_trader['items']
                            ]
                        )
                        self.traders.append(new_trader)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading NPCs: {e}")

    def inspect(self) -> None:
        """
        Display the room description and the doors and NPCs in the room.

        Args:
            None

        Returns:
            None
        """
        print(f"\nYou decide to look around and see: {self.description} "
              f"There are {len(self.doors)} doors in this room.")

    def interact(self) -> None:
        """
        Interact with the room, allowing exploration and looking for NPCs.

        Args:
            None

        Returns:
            None
        """
        print("You can explore the room or look for NPCs.")
