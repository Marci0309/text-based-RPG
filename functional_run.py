import subprocess
from unittest.mock import patch
from rpg.game import Game  # Import the Game class from your main.py


def test_starting_room_interaction(capfd):
    # Simulate the inputs for the starting room
    simulated_inputs = [
        'TestPlayer',      # Player enters their name
        '1',  # Player interacts with the NPC
        '1',  # Player ask a question
        '0',  # Player does not ask more question
        '0',  # Attack
        '0',  # Attack
        '0',  # Kill the training dummy
        '2',  # Leave the starting room
        '2',  # Leave to a new room
        '0',  # Choose a door
        '7',  # Interact with trader
        '0',  # Interact with trader
        '-1',  # Leave the trader
        '1',  # Look around
        '6',  # Look for items
        '5',  # Check Inventory
        '1',  # Not use anything
        '8',  # Save menu
        '1',  # Save
        '2',  # Look for a way out
        '0',  # Leave to a new room
        '3',  # Use Item
        '0',  # Use Item
        '0',  # Use Item (0)
        '0',

    ]

    # Patch the 'input' function to simulate the user inputs
    with patch('builtins.input', side_effect=simulated_inputs), \
         patch('random.randint', return_value=3):
        # Create an instance of the Game class
        game_instance = Game()

        # Run the game (this starts the interaction with the starting room)
        game_instance.run()

        # Capture the printed output
        out, err = capfd.readouterr()

        # Print the captured output so that you can see it during the test
        print(out)

        # Check if the player's name is correctly used in the game
        assert "TestPlayer" in out
        # Check if the player's name is correctly used in the game
        assert "Ah, TestPlayer! A fine name you have indeed!" in out

        # Verify that the player fought the dummy and defeated it
        assert "You defeated Training Dummy!" in out

        # Check that the player was able to open the door
        assert "You decide to look around for doors. You see:" in out


def run_tests():
    """
    This function runs pytest with the -s flag
    (which prevents output capturing).
    """
    # Run pytest with the -s option
    result = subprocess.run(['pytest', '-s', 'functional_run.py'],
                            capture_output=False)

    # Optionally, check the return code to see if pytest ran successfully
    if result.returncode == 0:
        print("All tests passed!")
    else:
        print(f"Some tests failed. Return code: {result.returncode}")


if __name__ == "__main__":
    run_tests()
