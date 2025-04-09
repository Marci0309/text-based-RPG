from abc import ABC, abstractmethod


class Inspectable(ABC):
    @abstractmethod
    def inspect(self) -> str:
        """
        Inspect the object and return information about its current state.

        Args:
            None

        Returns:
            str: Information about the object’s current state.
        """
        pass


class Interactable(ABC):
    @abstractmethod
    def interact(self) -> str:
        """
        Interact with the object and trigger a specific action or behavior.

        Args:
            None

        Returns:
            str: The result of the interaction,
            which may vary depending on the object.
        """
        pass
