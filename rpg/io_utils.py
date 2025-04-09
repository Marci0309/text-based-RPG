class Scanner:
    def __init__(self) -> None:
        """
        Initialize the Scanner object.

        Args:
            None

        Returns:
            None
        """
        super().__init__()

    def options(self) -> None:
        """
        Display the available options for the player to choose from.

        Args:
            None

        Returns:
            None
        """
        print("    (-1) Quit the game")
        print("     (0) Show visited rooms")
        print("     (1) Look around")
        print("     (2) Look for a way out")
        print("     (3) Look for company")
        print("     (4) Look for a fight")
        print("     (5) View inventory")
        print("     (6) Look for items")
        print("     (7) Interact with trader")
        print("     (8) Save/Load the game")

    def read_int(self) -> int:
        """
        Continuously prompt the user to input a valid option,
        returning the selected option as an integer.

        Args:
            None

        Returns:
            int: The user's selected option,
            or -1 if they choose to quit the game.
        """
        while True:
            user_input = input("Select an option: ")
            if user_input.strip() == "-1":
                print("You chose to quit the game")
                return -1
            if user_input.isdigit() and 8 >= int(user_input) >= 0:
                return int(user_input)
            else:
                print("Invalid input: Please enter a positive whole number.")
