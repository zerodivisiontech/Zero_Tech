import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = BASE_DIR / "content"


def load_scenes() -> list[dict]:
    with open(CONTENT_DIR / "scenes.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_volumes() -> dict:
    with open(CONTENT_DIR / "volumes.json", "r", encoding="utf-8") as f:
        return json.load(f)


def show_scene(scene: dict) -> None:
    print("\n" + "=" * 60)
    print("title")
    print(scene["title"])
    print("=" * 60)
    print(scene["story"])
    print("\nChallenge:")
    print(scene["challenge_text"])
    print("-" * 60)