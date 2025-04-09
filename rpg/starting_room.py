import json
import os
import random
from .enemy import Enemy


class StartingRoom:
    def __init__(self) -> None:
        """
        Initialize the StartingRoom with default values.
        """
        self.npc_present = True
        self.door_locked = True
        self.has_interacted_with_npc = False
        self.player_name = None
        self.defeated = False
        self.health = 100
        self.heal_used = 0
        self.action_count = 3
        self.told = False
        self.wrong = False

    def ask_player_name(self) -> None:
        """
        Ask the player for their name, ensuring it's unique.
        """
        saved_players = self.load_saved_players()
        while True:
            name = input("Welcome, adventurer! What is your name? ").strip()
            if not name:
                print("Please enter a valid name.")
                continue

            if name in saved_players:
                print(f"The name '{name}' is already taken. Please choose a "
                      "different name.")
            else:
                self.player_name = name
                print(f"\nAh, {self.player_name}! A fine name you have "
                      "indeed!")
                break

    def load_saved_players(self) -> dict:
        """
        Load the saved player names from the JSON file.

        Returns:
            dict: A dictionary of saved player names.
        """
        base_dir = os.path.dirname(__file__)
        save_file = os.path.join(base_dir, 'game_save.json')

        if not os.path.exists(save_file):
            return {}

        try:
            with open(save_file, 'r') as f:
                all_game_data = json.load(f)
                return all_game_data.keys()
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading save file. Starting with a fresh game.")
            return {}

    def show_room_description(self) -> None:
        """
        Show the description of the starting room.
        """
        print(f"\t{self.player_name}, you find yourself"
              " in a small room with one"
              "door. You are probably wondering how you got here, but that's "
              "for you to find out, adventurer.")

    def interact_with_npc(self) -> None:
        """
        Allow the player to interact with the NPC.
        """
        if not self.defeated:
            print(f"\nGame guide: Greetings, {self.player_name}! I see you're "
                  "ready for the adventure ahead.'")
            while True:
                self.offer_additional_options()
                continue_choice = input("\nWould you like to ask something "
                                        "else? \n(0) No \n (1) Yes: "
                                        "\nChoose an option: ")
                if continue_choice == '0':
                    print("\nBefore you head out on your journey, let's "
                          "practice some combat!")
                    break
                elif continue_choice == '1':
                    continue
                else:
                    print("Game guide: Please select a valid option.")
            self.start_combat_tutorial()
            self.has_interacted_with_npc = True
            self.door_locked = False
        elif self.defeated and not self.told:
            print("\nGame guide: 'Well done, adventurer! You've proven your "
                  "mettle. The door is now unlocked.'")
            print("As a starting bonus, I gift you 5 coins. Your health is "
                  "also restored to 100.")
            self.door_locked = False
            self.told = True
        else:
            print("\nGame guide: I already told you everything that needs to "
                  "be told. Now go and explore the world.")

    def start_combat_tutorial(self) -> None:
        """
        Start a combat tutorial with a dummy enemy.
        """
        print("\nA Training Dummy appears! He is not as\
               friendly as he looks unfortunately.")
        dummy_enemy = Enemy(
            name="Training Dummy", health=30, damage=5,
            description="A wooden training dummy.", difficulty="Easy"
        )

        while dummy_enemy.health > 0 and self.health > 0:
            print(f"{dummy_enemy.name} has {dummy_enemy.health} health.")
            print(f"Your current health: {self.health}")
            print("\nChoose your action:")
            print(" (0) Attack - Deal 10 damage to the enemy.")
            print(" (1) Defend - Reduce damage from the next attack.")
            print(" (2) Heal - Restore health, can be used \
                  once every 3 actions.")
            print(" (3) Run Away - Lose 50% health, escape the fight.")

            choice = input("Select an action by number: ")

            is_defending = False  # Reset defending status each turn

            if choice == '0':
                damage_dealt = 10
                print(f"\nYou attack {dummy_enemy.name} \
                      for {damage_dealt} damage!")
                dummy_enemy.health -= damage_dealt
                self.action_count += 1
                if dummy_enemy.health <= 0:
                    print(f"You defeated {dummy_enemy.name}!")
                    self.defeated = True
                    break
            elif choice == '1':
                print("You brace yourself for the next attack.")
                is_defending = True
                self.action_count += 1
            elif choice == '2':
                if self.action_count >= 3:
                    heal_amount = random.randint(7, 15)
                    self.health = min(self.health + heal_amount, 100)
                    print(f"\nYou heal yourself for {heal_amount} health!\
                           Current health: {self.health}.")
                    self.action_count = 0
                else:
                    print("\nYou cannot heal again in this combat!")
            elif choice == '3':
                print("\nCome oooonn! You can do better than that!")
                self.health = max(self.health // 2, 1)
                return
            else:
                print("Invalid choice. Please select a valid action.")
                continue  # Skip enemy's attack

            # Enemy's turn
            if dummy_enemy.health > 0:
                if is_defending:
                    damage_received = max(dummy_enemy.damage // 2, 0)
                    print(f"{dummy_enemy.name} attacks\
                           you for {damage_received} damage!")
                    self.health -= damage_received
                else:
                    print(f"{dummy_enemy.name} attacks\
                           you for {dummy_enemy.damage} damage!")
                    self.health -= dummy_enemy.damage

                if self.health <= 0:
                    print("You have been defeated by the Training Dummy!")
                    break

                if self.health <= 50:
                    print("You are losing! I'll restore your health to 100.")
                    self.health = 100

    def try_open_door(self) -> bool:
        """
        Attempt to open the door.

        Returns:
            bool: True if the door is opened, False if it is locked.
        """
        if self.door_locked:
            print(f"\nThe door is locked, {self.player_name}. Perhaps you "
                  "should talk to the Game guide first.")
        else:
            print(f"\nThe door creaks open, {self.player_name}. You step "
                  "through into the next phase of your adventure.")
            return True
        return False

    def run(self) -> str:
        """
        Run the starting room logic.

        Returns:
            str: The player's name to be used in the main game.
        """
        self.ask_player_name()
        self.show_room_description()

        while True:
            print("\nWhat do you want to do?")
            print(" (1) Talk to the Game guide.")
            print(" (2) Try to open the door.")
            print(" (3) Look around.")
            print(" (4) Exit the game.")

            choice = input("Choose an option: ")

            if choice == '1':
                self.interact_with_npc()
            elif choice == '2':
                if self.try_open_door():
                    break
            elif choice == '3':
                print("\nThe room is small. There's not much besides the Game "
                      "guide and the door.")
            elif choice == '4':
                print("Exiting game...")
                exit(0)
            else:
                print("Invalid choice. Please select a valid option.")

        return self.player_name

    def offer_additional_options(self) -> None:
        """
        Offer additional options after interacting with the Game guide.
        """
        while True:
            print("\nGame guide: 'What would you like to know?'")
            print(" (1) Find out about the place.")
            print(" (2) Tell me the story of the place.")
            print(" (3) Is there any advice?")

            choice = input("Choose an option (1-3): ")

            if choice == '1':
                print("""\nGame guide: This is the starting room. My purpose is
    to teach you what you can do throughout the game.""")
                break
            elif choice == '2':
                print(f"""\nGame guide: 'Legend has it that this land was once
  ruled by a mighty king who vanished without a trace.
    The people of the land have been searching for him ever
       since, but none have succeeded.
          Now, the land is in turmoil, and it's up to you to bring
             peace and order back to the kingdom.
                       Go forth, {self.player_name},
                        and make your mark on this world!'""")
                break
            elif choice == '3':
                print("""\nGame guide: Stay away from the black cards; they are
    not your friends. Your health can't go above 100, so
        use your healing items wisely.""")
                break
            else:
                print("\nGame guide: 'That's not a valid choice, adventurer. "
                      "Choose wisely next time!'")
