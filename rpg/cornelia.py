import random
from .items import Item


class Cornelia:
    def __init__(self):
        """
        Initialize Cornelia with a flag to track
        if the player has played the game.

        Args:
            None

        Returns:
            None
        """
        self.played = False

    def interact(self, player) -> None:
        """
        Interact with Cornelia,
        offering the player a card game or the option to quit.

        Args:
            player: The player object interacting with Cornelia.

        Returns:
            None
        """
        while not self.played:
            print("\nBeautiful Mermade Cornelia: 'Welcome, adventurer!"
                  " Would you like to play a game with me or not?'")
            print("      You will be rewarded if you do :)")
            choice = input(
                "\n(0) Yes, play the game \n(1) No, I would like to skip it \n"
                "Your decision: "
                ).strip().lower()

            if choice == '0':
                self.play_game(player)
                break
            elif choice == '1':
                print(
                    "Mermade Cornelia:"
                    "'Farewell, brave adventurer! Until we meet again.'"
                    )
                break
            else:
                print(
                    "Invalid choice."
                    " Please enter (0) to play or (1) to quit the game."
                    )

    def play_game(self, player) -> None:
        """
        Handle the card game interaction
        and apply the outcome based on the player's choice.

        Args:
            player: The player object playing the game with Cornelia.

        Returns:
            None
        """
        print(
            "\n Mermade Cornelia:"
            "'It's a simple game with 4 cards, just choose the card,"
            "trust your instinct:"
            " \n (0) Hearts \n (1) Diamonds \n (2) Spades  \n (3) Clubs'"
            )
        cards = ["0", "1", "2", "3"]

        chosen_card = input(
            "Which card do you choose? Choose wisely! \nSelect by the number: "
            )

        if chosen_card not in cards:
            print("Invalid card choice. You lost your chance!")
            return

        if chosen_card == "2":
            print(
                "\n Mermade Cornelia: 'Oh no! You've chosen Spades!"
                "You will be punished for not paying attention!'"
                )
            player.health = player.health * 0.5
            print(
                "     You lose half your health!"
                f"Current health: {player.health}"
                )
            print("     Mermade Cornelia: 'Now, go away from me!'")
            return
        else:
            epic_item = self.get_random_epic_item()
            player.inventory.append(epic_item)
            print(
                "\n Mermade Cornelia: 'Congratulations!"
                f" You've received a {epic_item.name} as a reward!"
                f"That deals {epic_item.value} damage.'"
                )
            self.played = True

    def get_random_epic_item(self) -> Item:
        """
        Return a random epic item as an instance of the Item class.

        Args:
            None

        Returns:
            Item:
            An epic item with attributes such as name,
            rarity, effect type, and value.
        """
        epic_items_data = [
            {
                "name": "Epic Sword",
                "description": "A sword of epic proportions.",
                "effect_type": "damage",
                "value": 20,
                "price": 0
                },
            {
                "name": "Epic Axe",
                "description": "An axe with unstoppable power.",
                "effect_type": "damage",
                "value": 15,
                "price": 0
            },
            {
                "name": "Epic Bow",
                "description": "A bow that shoots arrows with great precision",
                "effect_type": "damage",
                "value": 18,
                "price": 0
            }

        ]
        selected_item_data = random.choice(epic_items_data)

        return Item(
            name=selected_item_data['name'],
            rarity="epic",
            effect_type=selected_item_data['effect_type'],
            value=selected_item_data['value'],
            description=selected_item_data['description'],
            price=selected_item_data['price']
        )
