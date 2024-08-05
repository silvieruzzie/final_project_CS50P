import pytest
from project import player, levels, sword_used, Cs50_Silvia_game, set_level, progress_to_next_level, check_answer, use_item
import tkinter as tk

@pytest.fixture
def game():
    root = tk.Tk()
    game_instance = Cs50_Silvia_game(root)
    yield game_instance
    root.destroy()

def test_set_level():
    set_level("cookie jar")
    assert player["level"] == "cookie jar"

def test_progress_to_next_level(game):
    player["level"] = "intro"
    progress_to_next_level(game.master, game.text_area)
    assert player["level"] == "cookie jar"
    
    progress_to_next_level(game.master, game.text_area)
    assert player["level"] == "working 9 to 5"
    
    progress_to_next_level(game.master, game.text_area)
    assert player["level"] == "python lair"

def test_check_answer_correct(game):
    player["level"] = "cookie jar"
    game.answer_entry.insert(0, levels["cookie jar"]["answer"])
    check_answer(game)
    assert "cookie crumble" in player["inventory"]

def test_check_answer_incorrect(game):
    if player["level"] == "cookie jar" and game.answer_entry.insert(0, "cat"):
        check_answer(game)
        assert "cookie crumble" not in player["inventory"]

def test_use_sword(game):
    if player["level"] == "python lair" and game.answer_entry.insert(0, "use sword"):
        check_answer(game)
        assert sword_used == True

def test_use_armor(game):
    player["level"] = "python lair"
    player["inventory"].append("armor")
    game.answer_entry.insert(0, "use armor")
    check_answer(game)
    assert sword_used is False

def test_split_python_no_sword(game):
    player["level"] = "python lair"
    game.answer_entry.insert(0, levels["python lair"]["answer"])
    check_answer(game)
    assert player["level"] == "python lair"

def test_split_python_with_sword(game):
    global sword_used
    player["level"] = "python lair"
    sword_used = True
    game.answer_entry.insert(0, levels["python lair"]["answer"])
    check_answer(game)
    assert game.master.after(5000, game.master.quit)