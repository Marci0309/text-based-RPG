# player.py

from .base_model import Interactable, Inspectable
from .enemy import Enemy
import random
from .items import Item


class player(Inspectable, Interactable):

    def __init__(
        self, starting_room, name: str = "Player",
        health: int = 100, damage: int = 10
    ) -> None:
        super().__init__()
        self.name = name
        self.health = health
        self.damage = damage
        self.visited_rooms = []
        self.heal_used = 0
        self.action_count = 0
        self.defeated_enemy = []
        self.inventory = []
        self.looked_for_items = False
        self.coins = 5
        self.trader_count = 0
        self.fought_in_room = {}

        if starting_room:
            self.current_room = starting_room
            self.visited_rooms.append(starting_room.name)

    def inspect(self, room_instance=None) -> None:
        if room_instance is None:
            room_instance = self.current_room
        room_instance.inspect()

    def interact(self) -> None:
        print("\nYou decide to look around for doors. You see:")

        if not self.current_room.doors:
            print("There are no doors in this room.")
            return

        for index, door in enumerate(self.current_room.doors.values()):
            print(f"  ({index}) {door.name}: {door.description}")

        door_choice = input("Select a door by number (or -1 to stay): ")
        if door_choice == "-1":
            print("\nYou chose to stay in the room.")
            return
        if (door_choice.isdigit()
                and 0 <= int(door_choice) < len(self.current_room.doors)):
            chosen_door = list(self.current_room.doors.values())[
                int(door_choice)
            ]

            if chosen_door.destination:
                print("  \nYou go through the door")
                self.current_room = chosen_door.destination
                self.visited_rooms.append(self.current_room.name)

                self.looked_for_items = False
                amount = 1
                self.coins += amount
                print(f"  You received {amount} coins, for clearing the room! "
                      f"Total coins: {self.coins}")

                if len(self.current_room.doors) == 0:
                    self.current_room.add_doors(self.visited_rooms)

                self.current_room.inspect()
            else:
                print("This door does not lead anywhere.")
        else:
            print("Invalid choice. Please select a valid door number.")

    def look_for_company(self) -> None:
        print("\nYou see the following characters:")

        all_characters = self.current_room.npcs

        if not all_characters:
            print("Unfortunately, there are no NPCs here.")
            return

        for index, character in enumerate(all_characters):
            print(f"  ({index}) {character.name}: {character.description}")

        character_choice = input(
            "\nSelect a character to interact with (or -1 to go back): "
        )

        if character_choice == '-1':
            print("You have chosen not to interact with anyone.")
            return

        if (character_choice.isdigit()
                and 0 <= int(character_choice) < len(all_characters)):
            chosen_character = all_characters[int(character_choice)]

            if isinstance(chosen_character, Enemy):
                self.start_combat(chosen_character)
            else:
                chosen_character.interact(self)
        else:
            print("Invalid choice. Please select a valid character number.")

    def start_combat(self, enemy) -> None:
        print(f"\n{enemy.name} appears! It has {enemy.health} health\
               and it deals {enemy.damage} damage.")

        while self.health > 0 and enemy.health > 0:
            print("\nCombat Menu:")
            print(f"     (0) Attack - Deal {self.damage} damage to the enemy.")
            print(
                f"     (1) Defend - Reduce damage taken from \
                    the next enemy attack. "
                f"You will take {enemy.damage // 2} damage."
            )
            print(
                "     (2) Heal - Restore health randomly from 10 to 30 health,"
                "can be used once every 3 actions."
            )
            print(
                "     (3) Use an Item - Use a healing or \
                    damage-boosting item from your inventory."
            )
            print(
                f"     (4) Run Away - Escape the fight, but\
                      lose 50% of your health. "
                f"You will end up with {self.health * 0.5} health."
            )

            combat_choice = input("Choose an action: ")

            if combat_choice == '0':
                attack_damage = self.damage
                enemy.health -= attack_damage
                self.action_count += 1
                if enemy.health <= 0:
                    print(f"     \nYou defeated {enemy.name}!")
                    self.defeated_enemy.append(enemy.name)
                    if enemy.difficulty == "easy":
                        amount = 2
                        self.coins += amount
                        print(f"     You received {amount} coins,\
                               for beating an easy monster! \
                              Your total coins: {self.coins}")
                    elif enemy.difficulty == "medium":
                        amount = 3
                        self.coins += amount
                        print(f"     You received {amount} coins, \
                              for beating a medium monster! \
                              Your total coins: {self.coins}")
                    elif enemy.difficulty == "hard":
                        amount = 5
                        self.coins += amount
                        print(f"     You received {amount} \
                              coins, for beating a hard monster!\
                               Your total coins: {self.coins}")
                    break
                else:
                    print(f"     \nYou attack {enemy.name} \
                          for {attack_damage} damage!")
                    print(f"          {enemy.name}\
                           has {enemy.health} health remaining")
            elif combat_choice == '1':
                print("     \nYou brace yourself for the next attack.")

                reduced_damage = max(enemy.damage // 2, 0)
                self.health -= reduced_damage
                print(f"     {enemy.name}'s attack is weakened!\
                       You take {reduced_damage} damage.")
                print(f"          Your current health \
                      is {self.health} health.")
                self.action_count += 1

            elif combat_choice == '2':
                if self.action_count >= 3:
                    heal_amount = random.randint(10, 30)
                    self.health += heal_amount
                    if self.health > 100:
                        self.health = 100
                        print(f"     \nYou healed yourself to full health!\
                               Your current health is {self.health}.")
                    else:
                        print(f"     \nYou healed yourself for {heal_amount}\
                               health! Your current health is {self.health}.")
                    self.action_count = 0
                else:
                    print("     \nYou need to take 3 \
                          actions before healing again.")
                # Enemy attacks after healing
                if enemy.health > 0:
                    self.health -= enemy.damage
                    print(f"     {enemy.name} attacks you\
                           for {enemy.damage} damage!")
                    print(f"          You have {self.health}\
                           health remaining.")
            elif combat_choice == '3':
                print("\nYou decide to use an item from inventory")
                if self.show_inventory_and_use_item():
                    print(f"          After using the item, \
                          your current health is {self.health}\
                              and damage is {self.damage}.")
                    self.action_count += 1
                else:
                    print("          You decided not to use any\
                           items or there was an invalid selection.")
            elif combat_choice == '4':
                lost_health = self.health * 0.5
                self.health -= lost_health
                print(f"     \nYou ran away but lost {lost_health} health.\
                       Your current health is {self.health}.")
                break
            else:
                print("Invalid choice. Please select a valid action.")

            # Enemy attacks after player's action (if not defeated)
            if enemy.health > 0 and combat_choice in ['0', '1', '3']:
                self.health -= enemy.damage
                print(f"     {enemy.name} attacks you for\
                       {enemy.damage} damage!")
                print(f"          You have {self.health} health remaining.")

            if self.health <= 0:
                print("     \nYou have been defeated!")
                print("Game Over!")
                exit(0)

        current_room_name = self.current_room.name
        self.fought_in_room[current_room_name] = True

    def look_for_fight(self) -> None:
        current_room_name = self.current_room.name

        if (current_room_name in self.fought_in_room
                and self.fought_in_room[current_room_name]):
            print("     There are no more enemies in this room.")
            return

        num_monsters = random.randint(0, 2)
        monsters_to_fight = []

        if num_monsters > 0:
            print(f"     \nYou encounter {num_monsters} monster(s)!")
            monsters_to_fight = random.sample(
                    Enemy.load_monsters(), num_monsters
                )
            remaining_monsters = [
                monster for monster in monsters_to_fight
                if monster.name not in self.defeated_enemy
            ]

            if not remaining_monsters:
                print("     There are no more monsters to fight in this room.")
                self.fought_in_room[current_room_name] = True
                return

            for index, monster in enumerate(remaining_monsters):
                print(f"({index}) {monster.name}: {monster.description} \
(Health: {monster.health}), \
Difficulty: {monster.difficulty}")

            choice = input("\nSelect a monster to fight by \
                           number (or -1 to back out): ")
            if choice.isdigit() and 0 <= int(choice) < len(remaining_monsters):
                chosen_monster = remaining_monsters[int(choice)]
                self.start_combat(chosen_monster)
            elif choice == '-1':
                print("     You decided to back out of the fight.")
            else:
                print("     Invalid choice. No monster selected.")
        else:
            print("     There are no monsters to fight right now.")

    def look_for_items(self) -> None:
        if self.looked_for_items:
            print("\nYou have already looked for items in this room.")
            return

        num_items_found = random.randint(1, 3)
        found_items = []

        rarities = ['common', 'rare', 'super rare', 'epic', 'legendary']
        probabilities = [0.5, 0.3, 0.15, 0.04, 0.01]

        for _ in range(num_items_found):
            rarity_choice = random.choices(rarities, probabilities)[0]
            items_of_rarity = [
                item for item in Item.load_items()
                if item.rarity == rarity_choice
            ]

            if items_of_rarity:
                selected_item = random.choice(items_of_rarity)
                found_items.append(selected_item)
                print(f"\nYou found a {selected_item.name}!\
                       It's a {selected_item.rarity} item.")
            else:
                print("No items found.")

        if found_items:
            self.inventory.extend(found_items)
            print(f"You now have {len(self.inventory)}\
                   items in your inventory.")
        else:
            print("No items found.")

        self.looked_for_items = True

    def show_inventory_and_use_item(self) -> bool:
        if not self.inventory:
            print("\nYour inventory is empty.")
            return False
        else:
            print("\nYour inventory:\n")
            for index, item in enumerate(self.inventory):
                print(f"({index}) {item.name}: {item.description}")

        print(f"You have {self.coins} coins.")

        if len(self.inventory) > 0:
            use_item_choice = input("Would you like to use\
                                     an item?\n (0) Yes \n (1) No \n \
                                    Your decision: ").strip().lower()
            if use_item_choice == "0":
                item_choice = input("Choose an item to use by \
                                    index (or -1 to go back): ").strip()

                try:
                    item_index = int(item_choice)
                    if item_index == -1:
                        print("Returning to menu.")
                        return False
                    elif 0 <= item_index < len(self.inventory):
                        item = self.inventory[item_index]

                        print(f"\nYour current health is: {self.health}")

                        if item.effect_type == "health":
                            print(f"\nYou used {item.name} and \
                                  healed for {item.value} health!")
                            self.health += item.value
                            if self.health > 100:
                                self.health = 100
                            print(f"Your updated health is now {self.health}.")

                        elif item.effect_type == "damage":
                            self.damage += item.value
                            print(f"\nYou equipped {item.name} and increased\
                                   your damage by {item.value}! \
                                    Your damage is now {self.damage}.")

                        self.inventory.remove(item)
                        return True
                    else:
                        print("Invalid item selection. Please\
                               choose a valid item index or -1 to go back.")
                        return False
                except ValueError:
                    print("Invalid choice. Please enter a valid\
                           item index or -1 to go back.")
                    return False

            elif use_item_choice == "1":
                print("You chose not to use any items.")
                return False

            else:
                print("Invalid choice. Please answer with (0) Yes or (1) No.")
                return False

    def interact_with_trader(self) -> None:
        if self.current_room.traders:
            trader_instance = self.current_room.traders[0]
            print(f"\nYou see a trader: {trader_instance.name}:\
                   {trader_instance.description}")
            while True:
                interact_choice = input("Do you want to interact \
                                        with \
                                        the trader? \n (0) Yes \n (1) No \n\
                                        Your decision: ").strip()
                if interact_choice == "0":
                    print(f"You currently have {self.coins} coins.")
                    trader_instance.trade(self)
                    break
                elif interact_choice == "1":
                    print("You chose not to interact with the trader.")
                    break
                else:
                    print("Invalid choice. Please answer with\
                           '0' (Yes) or '1' (No).")
        else:
            print("There is no trader here.")

    def use_item(self, item_index: int) -> bool:
        """
        Use an item from the inventory by its index.
        Returns True if the item was used successfully, False otherwise.
        """
        if 0 <= item_index < len(self.inventory):
            item = self.inventory.pop(item_index)
            print(f"\nYou used {item.name}: {item.description}")
            if item.effect_type == "health":
                self.health += item.value
                if self.health > 100:
                    self.health = 100
                print(f"Your health increased by {item.value}. \
                      Current health: {self.health}")
            elif item.effect_type == "damage":
                self.damage += item.value
                print(f"Your damage increased by {item.value}.\
                       Current damage: {self.damage}")
            # Add more item effects as needed
            return True
        else:
            print("Invalid item selection.")
            return False
