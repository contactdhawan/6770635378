import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

SAVE_FILE = "raise_bob_save.json"

class RaiseBobFullGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Raise Bob - Full Version")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Game variables
        self.hunger = 100
        self.happiness = 100
        self.cleanliness = 100
        self.age = 0
        self.money = 0
        self.bank = 0
        self.neglect_time = 0
        self.cosmetic = ""
        
        # Upgrades
        self.auto_feeder = False
        self.auto_cleaner = False
        self.auto_player = False
        self.multiplier = 1

        self.load_game()
        self.create_ui()
        self.update_stats()
        self.update_age()
        self.generate_money()
        self.auto_save()

    def create_ui(self):
        tk.Label(self.root, text="Raise Bob", font=("Arial", 18, "bold")).pack(pady=5)
        self.bob_label = tk.Label(self.root, text="👶", font=("Arial", 50))
        self.bob_label.pack(pady=5)
        self.create_progress_bar("Hunger", "hunger")
        self.create_progress_bar("Happiness", "happiness")
        self.create_progress_bar("Cleanliness", "cleanliness")

        self.money_label = tk.Label(self.root, text=f"Money: ${self.money}", font=("Arial", 12))
        self.money_label.pack(pady=5)

        self.bank_label = tk.Label(self.root, text=f"💰 Click to collect: ${self.bank}", fg="green", cursor="hand2")
        self.bank_label.pack()
        self.bank_label.bind("<Button-1>", lambda e: self.collect_money())

        tk.Button(self.root, text="Feed ($10)", command=self.feed_bob).pack(pady=2)
        tk.Button(self.root, text="Play 🎈", command=self.play_bob).pack(pady=2)
        tk.Button(self.root, text="Clean 🧽", command=self.clean_bob).pack(pady=2)
        tk.Button(self.root, text="Open Store 🛒", command=self.open_store).pack(pady=5)
        tk.Button(self.root, text="Save Game 💾", command=self.save_game).pack(pady=2)

        self.age_label = tk.Label(self.root, text="Age: 0s", font=("Arial", 12))
        self.age_label.pack(pady=5)

    def create_progress_bar(self, label_text, attr_name):
        tk.Label(self.root, text=label_text).pack()
        bar = ttk.Progressbar(self.root, maximum=100)
        bar.pack(pady=1)
        setattr(self, f"{attr_name}_bar", bar)

    def update_stats(self):
        self.hunger = max(self.hunger - 1, 0)
        self.happiness = max(self.happiness - 0.7, 0)
        self.cleanliness = max(self.cleanliness - 0.5, 0)

        if self.auto_feeder and self.hunger < 80:
            self.hunger = min(self.hunger + 1, 100)
        if self.auto_player and self.happiness < 80:
            self.happiness = min(self.happiness + 0.5, 100)
        if self.auto_cleaner and self.cleanliness < 80:
            self.cleanliness = min(self.cleanliness + 0.5, 100)

        if self.hunger <= 0 and self.happiness <= 0 and self.cleanliness <= 0:
            self.neglect_time += 1
        else:
            self.neglect_time = 0

        if self.neglect_time >= 10:
            self.game_over()

        self.hunger_bar['value'] = self.hunger
        self.happiness_bar['value'] = self.happiness
        self.cleanliness_bar['value'] = self.cleanliness
        self.update_bob_expression()

        self.root.after(1000, self.update_stats)

    def update_bob_expression(self):
        mood = "🙂"
        if self.hunger < 30 or self.happiness < 30 or self.cleanliness < 30:
            mood = "😢"
        elif self.hunger > 80 and self.happiness > 80 and self.cleanliness > 80:
            mood = "😄"
        if self.age > 180:
            base = "👴"
        elif self.age > 120:
            base = "🧑"
        elif self.age > 60:
            base = "🧒"
        else:
            base = "👶"
        self.bob_label.config(text=base + self.cosmetic + " " + mood)

    def feed_bob(self):
        if self.money >= 10:
            self.money -= 10
            self.hunger = min(self.hunger + 25, 100)
            self.update_money_display()

    def play_bob(self):
        self.happiness = min(self.happiness + 15, 100)

    def clean_bob(self):
        self.cleanliness = min(self.cleanliness + 20, 100)

    def update_money_display(self):
        self.money_label.config(text=f"Money: ${int(self.money)}")

    def update_age(self):
        self.age += 1
        self.age_label.config(text=f"Age: {self.age} seconds")
        self.root.after(1000, self.update_age)

    def generate_money(self):
        income = 5 * self.multiplier
        self.bank += income
        self.bank_label.config(text=f"💰 Click to collect: ${self.bank}")
        self.root.after(5000, self.generate_money)

    def collect_money(self):
        self.money += self.bank
        self.bank = 0
        self.update_money_display()
        self.bank_label.config(text="💰 Click to collect: $0")

    def open_store(self):
        store = tk.Toplevel(self.root)
        store.title("Bob's Store")
        store.geometry("300x300")

        tk.Label(store, text="Upgrades Store", font=("Arial", 14)).pack(pady=10)
        tk.Button(store, text="Auto-Feeder ($50)", command=lambda: self.buy_upgrade("feeder", 50)).pack(pady=5)
        tk.Button(store, text="Auto-Player ($75)", command=lambda: self.buy_upgrade("player", 75)).pack(pady=5)
        tk.Button(store, text="Auto-Cleaner ($100)", command=lambda: self.buy_upgrade("cleaner", 100)).pack(pady=5)
        tk.Button(store, text="Money Multiplier ($150)", command=lambda: self.buy_upgrade("multiplier", 150)).pack(pady=5)
        tk.Button(store, text="Hat Cosmetic ($30)", command=lambda: self.buy_upgrade("hat", 30)).pack(pady=5)

    def buy_upgrade(self, upgrade, cost):
        if self.money < cost:
            messagebox.showwarning("Store", "Not enough money!")
            return

        if upgrade == "feeder" and not self.auto_feeder:
            self.auto_feeder = True
        elif upgrade == "player" and not self.auto_player:
            self.auto_player = True
        elif upgrade == "cleaner" and not self.auto_cleaner:
            self.auto_cleaner = True
        elif upgrade == "multiplier" and self.multiplier == 1:
            self.multiplier = 2
        elif upgrade == "hat" and self.cosmetic == "":
            self.cosmetic = "🎩"
        else:
            messagebox.showinfo("Store", "Already purchased!")
            return

        self.money -= cost
        self.update_money_display()
        messagebox.showinfo("Store", f"Purchased {upgrade}!")

    def game_over(self):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        messagebox.showerror("Game Over", "You neglected Bob too long!\nHe left 😢")
        self.root.destroy()

    def save_game(self):
        data = {
            "hunger": self.hunger,
            "happiness": self.happiness,
            "cleanliness": self.cleanliness,
            "age": self.age,
            "money": self.money,
            "bank": self.bank,
            "auto_feeder": self.auto_feeder,
            "auto_cleaner": self.auto_cleaner,
            "auto_player": self.auto_player,
            "multiplier": self.multiplier,
            "cosmetic": self.cosmetic
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Save", "Game saved successfully!")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            self.hunger = data.get("hunger", 100)
            self.happiness = data.get("happiness", 100)
            self.cleanliness = data.get("cleanliness", 100)
            self.age = data.get("age", 0)
            self.money = data.get("money", 0)
            self.bank = data.get("bank", 0)
            self.auto_feeder = data.get("auto_feeder", False)
            self.auto_cleaner = data.get("auto_cleaner", False)
            self.auto_player = data.get("auto_player", False)
            self.multiplier = data.get("multiplier", 1)
            self.cosmetic = data.get("cosmetic", "")

    def auto_save(self):
        self.save_game()
        self.root.after(30000, self.auto_save)

# Start the game
root = tk.Tk()
game = RaiseBobFullGame(root)
root.mainloop()
