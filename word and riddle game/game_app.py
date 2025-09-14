import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk  # Install pillow for image handling
import random


def load_words(filename):
    try:
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        exit(1)


def load_riddles(filename):
    riddles = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                riddle, answer = line.strip().split('|')
                riddles[riddle] = answer
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{filename}' not found.")
        exit(1)
    return riddles


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word & Riddle Guessing Game")
        self.root.geometry("800x600")
        self.current_score = 0  # Tracks the player's score

        # Load a background image
        self.background_image = Image.open("background.jpg").resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Apply styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14), padding=10, relief="flat")
        self.style.map("TButton", background=[("active", "#61dafb")])

        self.create_main_menu()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_frame()

        # Add background
        canvas = tk.Canvas(self.root, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

        # Title with vibrant color
        canvas.create_text(400, 100, text="Welcome to the Game!", font=("Helvetica", 30, "bold"), fill="#e91e63")

        # Buttons panel with a colored background
        panel = tk.Frame(self.root, bg="#800080", bd=5, relief="raised")  # Medium Purple
        panel.place(x=250, y=200, width=300, height=250)

        ttk.Button(panel, text="Word Guessing Game", command=self.start_word_game).pack(pady=10)
        ttk.Button(panel, text="Riddle Guessing Game", command=self.start_riddle_game).pack(pady=10)
        ttk.Button(panel, text="Exit", command=self.root.quit).pack(pady=12)

        # Score panel with a distinct color
        score_panel = tk.Frame(self.root, bg="#4caf50", bd=5, relief="sunken")
        score_panel.place(x=10, y=550, width=780, height=40)

        tk.Label(score_panel, text=f"Your Score: {self.current_score}", font=("Helvetica", 14, "bold"), fg="white", bg="#4caf50").pack()

    def start_word_game(self):
        self.clear_frame()
        self.words = load_words('words.txt')
        self.secret_word = random.choice(self.words).lower()
        self.clue = ['?' for _ in self.secret_word]
        self.lives = self.get_difficulty()
        self.incorrect_guesses = []
        self.create_game_screen("Word Guessing Game")

    def start_riddle_game(self):
        self.clear_frame()
        self.riddles = load_riddles('riddles.txt')
        self.riddle, self.secret_word = random.choice(list(self.riddles.items()))
        self.clue = ['?' for _ in self.secret_word]
        self.lives = self.get_difficulty()
        self.incorrect_guesses = []
        self.create_game_screen("Riddle Guessing Game", is_riddle=True)

    def get_difficulty(self):
        difficulty = simpledialog.askstring("Difficulty", "Choose difficulty (easy, medium, hard):").strip().lower()
        return {"easy": 12, "medium": 9, "hard": 6}.get(difficulty, 9)

    def create_game_screen(self, title, is_riddle=False):
        self.clear_frame()

        # Add background
        canvas = tk.Canvas(self.root, width=800, height=600)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

        # Title
        canvas.create_text(400, 50, text=title, font=("Helvetica", 24, "bold"), fill="#8A2BE2")

        # Riddle display
        if is_riddle:
            canvas.create_text(400, 120, text=f"Riddle: {self.riddle}", font=("Helvetica", 16), fill="hotpink")

        # Clue
        self.clue_label = tk.Label(self.root, text=" ".join(self.clue), font=("Courier", 20, "bold"), fg="yellow", bg="#282c34")
        self.clue_label.place(x=250, y=180)

        # Lives left
        self.lives_label = tk.Label(self.root, text=f"Lives: {'❤' * self.lives}", font=("Helvetica", 16), fg="red", bg="#282c34")
        self.lives_label.place(x=250, y=250)

        # Entry field
        self.guess_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.guess_entry.place(x=250, y=300, width=300)

        # Buttons
        ttk.Button(self.root, text="Submit Guess", command=self.process_guess).place(x=250, y=350, width=150)
        ttk.Button(self.root, text="Main Menu", command=self.create_main_menu).place(x=400, y=350, width=150)

        # Incorrect guesses panel
        incorrect_panel = tk.Frame(self.root, bg="#d32f2f", bd=5, relief="ridge")
        incorrect_panel.place(x=300, y=400, width=300, height=50)

        # Incorrect guesses panel
        incorrect_panel = tk.Frame(self.root, bg="#d32f2f", bd=5, relief="ridge")
        incorrect_panel.place(x=250, y=400, width=350, height=80)  # Adjusted size for better fit

        # Increase the font size and make it more prominent
        self.incorrect_label = tk.Label(
            incorrect_panel,
            text="Incorrect Guesses: None",
            font=("Helvetica", 18, "bold"),  # Increased font size to 18
            fg="white",
            bg="#d32f2f"
        )
        self.incorrect_label.pack(pady=15)  # Added padding for spacing

    def update_clue(self, guessed_letter):
        for index in range(len(self.secret_word)):
            if guessed_letter == self.secret_word[index]:
                self.clue[index] = guessed_letter

    def process_guess(self):
        guess = self.guess_entry.get().lower().strip()
        self.guess_entry.delete(0, tk.END)

        if not guess or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a valid letter or word.")
            return

        # Track consecutive incorrect guesses
        if not hasattr(self, 'consecutive_incorrect_guesses'):
            self.consecutive_incorrect_guesses = 0

        if len(guess) > 1:  # Whole word guess
            if guess == self.secret_word:
                self.end_game(True)
            else:
                self.lives -= 1
                self.consecutive_incorrect_guesses += 1
        else:  # Single letter guess
            if guess in self.secret_word:
                self.update_clue(guess)
                self.consecutive_incorrect_guesses = 0  # Reset counter if the guess is correct
            else:
                if guess not in self.incorrect_guesses:
                    self.incorrect_guesses.append(guess)
                self.lives -= 1
                self.consecutive_incorrect_guesses += 1

        # Provide a clue if there are 3 consecutive incorrect guesses
        if self.consecutive_incorrect_guesses == 3:
            self.consecutive_incorrect_guesses = 0  # Reset counter after giving a clue
            hidden_letters = [letter for letter, clue_char in zip(self.secret_word, self.clue) if clue_char == '?']
            if hidden_letters:
                hint_letter = random.choice(hidden_letters)
                messagebox.showinfo("Hint", f"Here's a clue! The word contains the letter: '{hint_letter}'.")
                self.update_clue(hint_letter)

        self.update_game_screen()

    def update_game_screen(self):
        self.clue_label.config(text=" ".join(self.clue))
        self.lives_label.config(text=f"Lives: {'❤' * self.lives}")
        incorrect_text = ", ".join(self.incorrect_guesses) if self.incorrect_guesses else "None"
        self.incorrect_label.config(text=f"Incorrect Guesses: {incorrect_text}")

        if '?' not in self.clue:
            self.end_game(True)
        elif self.lives <= 0:
            self.end_game(False)

    def end_game(self, won):
        if won:
            points = self.lives * 10  # Bonus points for remaining lives
            self.current_score += points
            message = f"You won! The word was '{self.secret_word}'.\nYou earned {points} points!\nYour Score: {self.current_score}"
        else:
            message = f"You lost! The word was '{self.secret_word}'."
            self.current_score = 0  # Reset score on loss

        messagebox.showinfo("Game Over", message)
        self.create_main_menu()


if __name__ == "__main__":
    root = tk.Tk()  # Create the main application window
    app = GameApp(root)  # Initialize the game application
    root.mainloop()  # Start the Tkinter event loop