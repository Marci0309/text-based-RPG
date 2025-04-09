import random  # Import the random module
from rpg.player import player
from rpg.room import room
from rpg.io_utils import Scanner
from rpg.starting_room import StartingRoom
from rpg.enemy import Enemy
from rpg.cornelia import Cornelia
from rpg.npc import Trader
from rpg.game_save import save_game, load_game
from rpg.final_boss import FinalBoss
from rpg.vision_handler import show_next_vision


class Game:
    def __init__(self) -> None:
        """
        Initialize the Game object with an empty room list, the starting room,
        and player instance.
        """
        self.rooms = []
        self.current_room = room(name="Starting room")
        self.rooms.append(self.current_room)
        self.current_room.add_doors(self.rooms)
        self.player_instance = player(starting_room=self.current_room)
        self.scanner = Scanner()
        self.visited_rooms = set()
        self.monsters = Enemy.load_monsters()
        self.boss_fight_done = False
        self.played = False
        self.current_room.traders = Trader.load_traders()
        self.vision_index = 0

    def run(self) -> None:
        """
        Run the main game loop, handling player actions and game events.
        """
        starting_room = StartingRoom()
        player_name = starting_room.run()
        self.player_instance = player(
            starting_room=self.current_room, name=player_name
        )

        print("\nYou step inside the room and the door closes behind you."
              "\n\tYou get a vision from the past but its all blurry."
              "\n\t\tMaybe you have to explore more to get a clearer vision"
              "You think to yourself")
        question = "\nWhat do you want to do?"
        user_input = None
        game_end = random.randint(20, 25)

        try:
            while True:
                if (len(self.player_instance.visited_rooms) == 8
                        and not self.played):
                    cornelia = Cornelia()
                    cornelia.interact(self.player_instance)
                    self.played = True

                if (len(self.player_instance.visited_rooms) == game_end
                        and not self.boss_fight_done):
                    print("\nYou have entered the Final Room.")
                    final_boss = FinalBoss(self.player_instance)
                    final_boss.final_room_description()
                    final_boss.final_combat()
                    self.boss_fight_done = True
                    print("Exiting game...")
                    break

                print(question)
                self.scanner.options()
                user_input = self.scanner.read_int()

                if user_input == 0:
                    print(f"Visited rooms by {self.player_instance.name}: "
                          f"{self.player_instance.visited_rooms}")
                elif user_input == 1:
                    self.player_instance.inspect(self.current_room)
                elif user_input == 2:
                    self.player_instance.interact()
                    # Show the next vision and update the vision index
                    self.vision_index = show_next_vision(self.vision_index)
                elif user_input == 3:
                    self.player_instance.look_for_company()
                elif user_input == 4:  # Look for a fight
                    self.player_instance.look_for_fight()
                elif user_input == 5:  # View inventory
                    self.player_instance.show_inventory_and_use_item()
                elif user_input == 6:  # Look for items
                    self.player_instance.look_for_items()
                elif user_input == 7:  # Interact with trader
                    self.player_instance.interact_with_trader()
                elif user_input == 8:
                    print("\nDo you want to (1) Save or (2) Load the game?")
                    save_or_load = input().strip()

                    if save_or_load == '1':
                        save_game(self.player_instance)  # Save the game
                    elif save_or_load == '2':
                        player_name_to_load = input(
                            "Enter the player's name to load: "
                        ).strip()
                        load_game(self.player_instance, player_name_to_load)
                    else:
                        print("Invalid input. Please choose 1 for Save or 2 "
                              "for Load.")
                elif user_input == -1:
                    print("Exiting game...")
                    break  # Exit the game

        except ValueError as e:
            print(e)
