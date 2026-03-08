from engine.story import load_scenes, load_volumes, show_scene
from engine.runner import run_player_code
from engine.validator import check_output


def get_multiline_input() -> str:
    print("Enter your Python code below.")
    print("Type END on its own line when you're done.\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines)


def main() -> None:
    print("=" * 60)
    print("SYSTEM TRAIL")
    print("=" * 60)
    print("You wake in the shattered remains of Data City.")
    print("Your memory is damaged. The System is broken.")
    print("Recover the Lost Volumes. Rebuild what was destroyed.")

    scenes = load_scenes()
    volumes = load_volumes()
    recovered = []

    for scene in scenes:
        solved = False
        clue__index = 0

        while not solved:
            show_scene(scene)
            player_code = get_multiline_input()

            success, result = run_player_code(player_code)

            print("\nYour result:")
            print(result)
            print("-" * 60)

            if not success:
               print("The terminal sparks. Something about that command is wrong.")

            if "clues" in scene:
                clues = scene["clues"]

                if clue_index < len(clues):
                        print("\nYou search the ruins and find a clue:")
                        print(clues[clue_index])
                        clue_index += 1
                else:
                        print("\nNo more clues remain for this puzzle.")

                continue

            if check_output(result, scene["expected_output"]):
                volume = volumes[scene["volume_key"]]
                recovered.append(volume["name"])

                print(f"\nSuccess! You recovered: {volume['name']}")
                print(volume["description"])
                solved = True
            else:
                print("Not quite right.")

                if "clues" in scene:
                    clues = scene["clues"]

                    if clue_index < len(clues):
                        print("\nYou search the ruins and find a clue:")
                        print(clues[clue_index])
                        clue_index += 1
                    else:
                        print("\nNo more clues remain for this puzzle.")

                print("\nTry again.")

    print("\n" + "=" * 60)
    print("You restored the first pieces of the System.")
    print("Recovered Volumes:")
    for name in recovered:
        print(f"- {name}")
    print("=" * 60)
    print("Prototype complete.")


if __name__ == "__main__":
    main()