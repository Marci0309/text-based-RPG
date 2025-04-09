# final_boss.py

from rpg.enemy import Enemy
import random
from rpg.vision_handler import reveal_truth


class FinalBoss:
    def __init__(self, player) -> None:
        """
        Initialize the FinalBoss with the player's attributes.

        Args:
            player: The player object whose
            attributes are used in the final boss fight.

        Returns:
            None
        """
        self.player = player
        self.final_boss = Enemy(
            name="FINAL BOSS",
            health=random.randint(250, 300),
            damage=random.randint(10, 20),
            description="The final exam for OOP",
            difficulty="FINAL BOSS"
        )
        # Flag to indicate if defend action is active
        self.defend_active = False

    def final_room_description(self) -> None:
        """
        Display the description of the final
        room where the final boss fight takes place.

        Args:
            None

        Returns:
            None
        """
        print(
            f"{self.player.name}, you stand in a dark, ominous chamber."
            "This is the final test of your strength and courage."
            "The air is thick with tension."
        )
        print(
            f"\nYour current health: {self.player.health},"
            f" strength: {self.player.damage},"
            f" and you have {len(self.player.inventory)} item(s)"
            " in your inventory."
        )

    def final_combat(self) -> None:
        """
        Engage the player in a final combat sequence against the Final Boss.

        Args:
            None

        Returns:
            None
        """
        print("\n      The Final Boss, Lord of Shadows, stands before you")

        while self.final_boss.health > 0 and self.player.health > 0:
            print(f"        {self.final_boss.name} has\
 {self.final_boss.health} health.")
            print(f"            Your current health: {self.player.health}")
            print("\nChoose your action:")

            print(
                f"    (0) Attack - Deal {self.player.damage} damage \
to the enemy."
            )
            print(
                "     (1) Defend - Reduce damage taken from the next \
enemy attack. Enemy will deal half damage."
            )
            print(
                "     (2) Heal - Restore from 10 - 30 health, \
can be used once every 3 actions."
            )
            print(
                "     (3) Use Item - Access your inventory to use an item."
            )
            print(
                "     (4) Run Away - No escape from the final battle!"
            )

            choice = input("Select an action by number: ")

            if choice == '0':
                damage_dealt = self.player.damage
                print(
                    f"\nYou attack {self.final_boss.name} for\
 {damage_dealt} damage"
                )
                self.final_boss.health -= damage_dealt
                self.player.action_count += 1
                if self.final_boss.health <= 0:
                    print(f"  You defeated the {self.final_boss.name}!")
                    reveal_truth()  # Reveal the final truth here
                    break

            elif choice == '1':
                print("You brace yourself for the next attack. \
Your defense will reduce the damage taken.")
                self.defend_active = True
                self.player.action_count += 1

            elif choice == '2':
                if self.player.action_count >= 3:
                    heal_amount = random.randint(10, 30)
                    self.player.health = min(
                        self.player.health + heal_amount, 100
                    )
                    print(f"\nYou heal yourself for {heal_amount} health! \
Your current health is now {self.player.health}.")
                    self.player.action_count = 0
                else:
                    print("\nYou cannot heal again in this combat!")

            elif choice == '3':
                if self.player.show_inventory_and_use_item():
                    continue

            elif choice == '4':  # Run Away
                print("\nThere is no escape from the final battle!")
            else:
                print("Invalid choice. Please select a valid action.")

            # Enemy's turn to attack if still alive
            if self.final_boss.health > 0:
                final_boss_damage = random.randint(20, 40)
                if self.defend_active:
                    final_boss_damage = max(final_boss_damage // 2, 0)
                    self.defend_active = False  # Reset defend status
                    print(f"\n{self.final_boss.name} attacks you, \
but you defend! You take {final_boss_damage} damage.")
                else:
                    print(f"\n{self.final_boss.name} attacks \
you for {final_boss_damage} damage!")
                self.player.health -= final_boss_damage
                if self.player.health <= 0:
                    print("You have fallen in battle...")
                    break
