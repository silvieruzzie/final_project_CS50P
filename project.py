import tkinter as tk
from tkinter import scrolledtext, Entry, Button

sword_used = False
player = {"level": "", "inventory": []}
levels = {
    "intro": {
        "description": (
            "Hello fellow student! I desperately need your help!\nOur beloved professor, David Malan, has mysteriously gone missing.\nYou, the protagonist, are a brave coder determined to rescue him.\nYour quest begins as you explore the Harvard campus,\nseeking any clues that might lead you to his whereabouts."
        )
    },
    "cookie jar": {
        "description": (
            "Your journey starts in the cafeteria.\nAs you enter the hall, you notice an enormous jar in the middle of the room.\nBeside it is a ladder that extends up to the jar's lid.\nYou decide to climb the ladder.\nAs you reach the top, you lean in to take a closer look,\ndrawn by the delightful aroma emanating from within.\nSuddenly, you lose your balance and tumble headfirst into the jar,\nlanding amidst a pile of giant, now crumbled, chocolate chip cookies.\nYou find a small piece of parchment among the cookie crumbs. It reads:"
        ),
        "riddle": (
            "Solve this puzzle to find the key,\n"
            "And out of this jar, you will be free.\n"
            "I am a blueprint for object creation,\n"
            "With attributes and methods of your imagination,\n"
            "Instantiated by calling my name,\n"
            "Type it right out to solve the game."
        ),
        "items": ["cookie crumble"],
        "answer": "class",
        "outro": "The lid of the cookie jar clicks open. You climb out and take a deep breath of fresh air.\n\n\n",
    },
    "working 9 to 5": {
        "description": (
            "...You make your way to the drama center,\nhoping to find some clues along the way.\nAs you approach a beautiful theater,\nthe sound of music fills the air.\nCenter-stage, you see Dolly Parton herself,\nperforming her iconic song '9 to 5'.\nYou applaud as Dolly finishes her song,\nbut to your surprise, she starts singing it again.\nShe appears visibly distressed and motions for you to approach.\nWith a concerned expression, she hands you a piece of paper.\nIt explains that she is unable to stop singing until someone solves the following riddle:"
        ),
        "riddle": (
            "I sing my song with all my might,\n"
            "But stuck in a loop, it's quite a plight.\n"
            "To break this cycle, here's the key,\n"
            "Match my pattern and set me free.\n"
            "In Python's realm, it's quite renowned,\n"
            "For matching strings, it's often found.\n"
            "With patterns complex or plain to see,\n"
            "Use it right, and you'll save me."
        ),
        "items": ["armor", "sword"],
        "answer": "regex",
        "outro": (
            "You've solved the riddle! Dolly Parton stops singing '9 to 5' and thanks you profusely.\nYou head backstage to search for anything useful.\nAmid the countless costumes, you find a fake armor and sword.\nYou grab them.\n\n\n"
        ),
    },
    "python lair": {
        "description": "...Workin' nine to five, what a way to make a livin' barely gettin' by...\nwhoops I'm sorry I got distracted...\nwhere were we?\nThis song is going to be stuck in our head for the rest of this, isn't it?\nAnyway...\nAs you descend into Harvard's underground tunnels,\nyou see a giant Python coiled tightly around Professor Malan,\nsqueezing him tighter and tighter.\nThe Python hisses:\n'Solve my riddle or watch him die!'",
        "riddle": "In Python's realm, where strings do dance,\n"
        "With slicing and dicing, you'll have your chance.\n"
        "Show me the code that splits me right,\n"
        "And save your professor from his plight.",
        "items": [],
        "answer": "python[:3], python[3:]",
        "outro": "You correctly split the word 'PYTHON'! The giant Python releases Professor Malan and slithers away in defeat.\nProfessor Malan thanks you for your bravery and ingenuity. Now he can go back to sharing his knowledge with the world. Yay!\n\n\n",
    },
}

def set_level(level_name):
    player["level"] = level_name

def progress_to_next_level(master, text_area):
    current_level = player["level"]
    if current_level == "intro":
        clear_window(text_area)
        set_level("cookie jar")
        display_description(text_area, master)
    elif current_level == "cookie jar":
        set_level("working 9 to 5")
        display_description(text_area, master)
    elif current_level == "working 9 to 5":
        set_level("python lair")
        display_description(text_area, master)
    elif current_level == "python lair":
        text_area.insert(tk.END, "\nYou have finished the game!\n")
        master.after(5000, master.quit)

def display_description(text_area, master):
    level_name = player["level"]
    sentences = levels[level_name]["description"].split("\n")
    current_sentence = 0

    def display_next_sentence(event):
        nonlocal current_sentence
        if current_sentence < len(sentences):
            text_area.insert(tk.END, sentences[current_sentence] + "\n")
            text_area.see(tk.END)
            current_sentence += 1
        else:
            clear_window(text_area)
            if "riddle" in levels[player["level"]]:
                display_riddle(text_area)
            else:
                progress_to_next_level(master, text_area)

    master.bind("<Return>", display_next_sentence)
    display_next_sentence(None)

def clear_window(text_area):
    text_area.delete(1.0, tk.END)

def display_riddle(text_area):
    if "riddle" in levels[player["level"]]:
        riddle_text = levels[player["level"]]["riddle"]
        clear_window(text_area)
        text_area.insert(tk.END, "\n" + riddle_text + "\n")
        text_area.see(tk.END)

def check_answer(game):
    global sword_used
    current_level = player["level"]
    answer = game.answer_entry.get().strip()

    if current_level == "python lair" and answer == "use sword":
        use_item(game, "sword")
    elif current_level == "python lair" and answer == "use cookie crumble":
        use_item(game, "cookie crumble")
    elif current_level == "python lair" and answer == "use armor":
        use_item(game, "armor")

    if current_level == "python lair" and answer == "python[:3], python[3:]" and sword_used:
        clear_window(game.text_area)
        display_outro(game.text_area)
        progress_to_next_level(game.master, game.text_area)
    elif current_level == "python lair" and answer == "python[:3], python[3:]" and not sword_used:
        game.text_area.insert(tk.END, "\nThe answer is correct! But the python is too strong! Looks like you'll have to try again, maybe use something from your inventory ;)\n")

    if (current_level == "cookie jar" or current_level == "working 9 to 5") and answer == levels[current_level]["answer"]:
        clear_window(game.text_area)
        display_outro(game.text_area)
        progress_to_next_level(game.master, game.text_area)
        if current_level == "cookie jar":
            player["inventory"].append("cookie crumble")
        elif current_level == "working 9 to 5":
            player["inventory"].append("armor")
            player["inventory"].append("sword")
    elif answer != levels[current_level]["answer"]:
        game.text_area.insert(tk.END, "\nTry again!\n")
    game.answer_entry.delete(0, 'end')

def display_outro(text_area):
    if "outro" in levels[player["level"]]:
        outro_text = levels[player["level"]]["outro"]
        text_area.insert(tk.END, "\n" + outro_text + "\n")
        text_area.see(tk.END)

def use_item(game, item):
    global sword_used
    if item in player["inventory"]:
        if item == "cookie crumble":
            game.text_area.insert(tk.END, "nom, nom, nom... mmmh")
            game.text_area.see(tk.END)
        elif item == "sword":
            sword_used = True
            game.text_area.insert(tk.END, "Good idea, this might help you split the python but you still need to answer the riddle!")
            game.text_area.see(tk.END)
        elif item == "armor":
            game.text_area.insert(tk.END, "This armor is extremely heavy, I doubt it's going to help, you toss it to the side.")
            game.text_area.see(tk.END)
    else:
        game.text_area.insert(tk.END, "You don't have that in your inventory!")
        game.text_area.see(tk.END)

class Cs50_Silvia_game:
    def __init__(self, master):
        self.master = master
        self.master.title("Operation Python")
        self.master.configure(bg="black")

        self.text_area = scrolledtext.ScrolledText(
            self.master,
            width=50,
            height=20,
            wrap=tk.WORD,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Lucida Console", 16),
        )
        self.text_area.pack(padx=10, pady=10)

        self.answer_entry = Entry(
            self.master,
            font=("Lucida Console", 16),
            bg="black",
            fg="white",
            insertbackground="white",
        )
        self.answer_entry.pack(pady=5)

        self.submit_button = Button(
            self.master, text="Submit", command=lambda: check_answer(self)
        )
        self.submit_button.pack(pady=5)

        self.init_game()

    def init_game(self):
        set_level("intro")
        display_description(self.text_area, self.master)

def main():
    root = tk.Tk()
    game_gui = Cs50_Silvia_game(root)
    root.mainloop()

if __name__ == "__main__":
    main()