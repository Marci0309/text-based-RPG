# door.py

from .base_model import Inspectable, Interactable


class door(Inspectable, Interactable):
    def __init__(
            self, name: str,
            description: str,
            destination=None,
            locked: bool = False
            ) -> None:
        """
        Initialize a Door object.

        Args:
            name (str): The name of the door.
            description (str): A brief description of the door.
            destination: The destination room the door leads to (default: None)
            locked (bool): Whether the door is locked or not (default: False).

        Returns:
            None
        """
        self.name = name
        self.description = description
        self.destination = destination
        self.locked = locked

    def interact(self, player) -> None:
        """
        Interact with the door, allowing the player
        to move to the destination room if available.

        Args:
            player: The player object interacting with the door.

        Returns:
            None
        """
        if self.locked:
            print(f"The {self.name} is locked. You cannot go through it.")
        elif self.destination is not None:
            print(f"You go through the {self.name}.")
            player.current_room = self.destination
        else:
            print("This door does not lead anywhere.")

    def inspect(self) -> None:
        """
        Inspect the door, displaying its name and locked status.

        Args:
            None

        Returns:
            None
        """
        print(f"Door: {self.name}, \
Description: {self.description}, Locked: {self.locked}")
