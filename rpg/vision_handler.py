visions = [
    "A dimly lit room flickers into view. You’re sitting at a table, staring"
    "\n\tat an old clock on the wall."
    "Its ticking feels unnaturally loud, and the"
    "\n\thands move too fast.",

    "A voice echoes in the distance, calling your name."
    "\n\tYou stand up from the table, but the voice grows faint and distant"
    "\n\tas you move toward it.",

    "You find yourself standing in the middle of a long corridor."
    "\n\tThe walls are lined with framed photographs, but every face"
    "\n\tin the pictures is blurred.",

    "Suddenly, the corridor darkens. You hear footsteps behind you,"
    "\n\tbut when you turn, no one is there. You feel watched, but by whom?",

    "You stumble into a room with a single window. Outside, you see"
    "\n\ta city covered in rain. A car speeds by, and for a moment,"
    "\n\tyou catch a glimpse of someone in the passenger seat.",

    "The room shifts, and you’re standing outside on a street at night."
    "\n\tA streetlight flickers overhead, and in the distance, you"
    "\n\tsee a figure. They’re watching you.",

    "The figure begins to move, walking away into the fog."
    "\n\tInstinctively, you follow, but no matter how fast you walk,"
    "\n\tthey stay just out of reach.",

    "You turn a corner and find yourself in front of a house."
    "\n\tIt’s familiar, but not quite how you remember it."
    "\n\tThe windows are dark, and the door is slightly ajar.",

    "Inside the house, the air is heavy with silence."
    "\n\tAs you step in, you hear the faint sound of crying from upstairs."
    "\n\tYour chest tightens—you’ve been here before.",

    "At the top of the stairs, you find a closed door."
    "\n\tThe crying stops. Your hand trembles as you reach for the doorknob.",

    "You open the door and find a small, empty room."
    "\n\tOn the floor, a single toy lies discarded—a stuffed bear."
    "\n\tYou recognize it. It was yours.",

    "A wave of unease hits you. The house is yours, but it feels wrong."
    "\n\tThe furniture is misplaced, and the walls are painted a color"
    "\n\tthey never were.",

    "As you move through the house, you hear voices."
    "\n\tThey’re muffled, distant, as if behind a wall."
    "\n\tYou press your ear to the floor, but the voices fade away.",

    "Suddenly, you’re outside again, standing on a bridge at night."
    "\n\tBelow, the water churns violently. You hear a scream,"
    "\n\tbut you can’t see where it’s coming from.",

    "You lean over the edge of the bridge, and for a moment,"
    "\n\tyou see a reflection in the water. It’s you, but you look different"
    "\n\t—older, weary, afraid.",

    "You turn away from the water and face the street."
    "\n\tA car speeds past you, and in the rear window,"
    "\n\tyou see the shadowy figure again, watching.",

    "You start running down the street. Your heart races as you realize"
    "\n\tthat something terrible is about to happen."
    "\n\tYou know this street, this moment—it’s coming back to you.",

    "You stop suddenly in front of a hospital."
    "\n\tThe entrance doors slide open, and "
    "you’re pulled inside by a rush of wind."
    "\n\tThe place is empty, but you feel like you’re not alone.",

    "In the hospital, you hear a voice calling your name again."
    "\n\tThis time, it’s clearer. It’s someone you know well,"
    "\n\tsomeone you lost. The realization shakes you to your core.",

    "The final vision hits you with the force of a memory long buried."
    "\n\tYou’re in the hospital room, standing by a bed."
    "\n\tThe person in the bed is gone,"
    " but the heart monitor still beeps faintly."
    "\n\tYou remember now—you were there when they died."
]


def get_next_vision(vision_index: int) -> tuple:
    """
    Return the next vision in sequence. If all visions have been shown,
    return a final message.

    Args:
        vision_index (int): The index of the current vision.

    Returns:
        tuple: A tuple containing the next vision (str) and the updated index
        (int).
    """
    if vision_index >= len(visions):
        return "You have recalled all you can from your past.", vision_index

    # Get the next vision
    vision = visions[vision_index]
    return vision, vision_index + 1


def show_next_vision(vision_index: int) -> int:
    """
    Show the next vision in sequence every time the player enters a new room.

    Args:
        vision_index (int): The index of the current vision.

    Returns:
        int: The updated vision index.
    """
    vision, updated_index = get_next_vision(vision_index)
    print(f"\n** Vision from the past: **\n{vision}\n")
    return updated_index


def reveal_truth() -> None:
    """
    Reveal the final truth after the player defeats the final boss.
    """
    final_truth = (
        "As the dust settles and the final battle ends,"
        "the truth is revealed...\n\n"
        "Everything you've experienced here has been leading to this moment."
        "The visions, the memories,"
        "the challenges—they were all a reflection of"
        "your past. You now understand that the Labyrinth is a construct of "
        "your own mind, a way to come to terms with the truths you've buried "
        "deep within yourself. With the final boss defeated, you are free from"
        "the labyrinth, and the memories of your past can finally rest."
    )
    print("\n=== The Truth Revealed ===\n")
    print(final_truth)
