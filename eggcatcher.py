from tkinter import Tk, Canvas, HIDDEN, NW
import random
import time

# Constants
canvas_width = 800
canvas_height = 400
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty_factor = 0.95
catcher_color = 'blue'
catcher_width = 100
catcher_height = 100
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height - 20
catcher_startx2 = catcher_startx + catcher_width
catcher_starty2 = catcher_starty + catcher_height
game_font = ('Helvetica', 18)
score_color = 'darkblue'
lives_color = 'darkred'
background_color = 'deep sky blue'

# Tkinter Setup
root = Tk()
root.title("Egg Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height, background=background_color)
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill='light green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

# Score and lives
score = 0
lives_remaining = 3
score_text = c.create_text(10, 10, anchor=NW, font=game_font, fill=score_color,
                           text='Score: ' + str(score))
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=game_font, fill=lives_color,
                           text='Lives: ' + str(lives_remaining))

# Egg management
eggs = []
def create_egg():
    x = random.randint(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill='white', width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        c.move(egg, 0, 10)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        c.create_text(canvas_width/2, canvas_height/2, text='GAME OVER!', fill='red', font=('Helvetica', 30))
        c.create_text(canvas_width/2, canvas_height/2 + 40, text='Final Score: ' + str(score),
                      fill='black', font=('Helvetica', 24))
        c.update()
        time.sleep(3)
        root.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text='Lives: ' + str(lives_remaining))

def check_catch():
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text, text='Score: ' + str(score))

# Catcher
catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2,
                       start=200, extent=140, style='arc', outline=catcher_color, width=3)

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind_all('<Left>', move_left)
c.bind_all('<Right>', move_right)

# Start the game
create_egg()
move_eggs()
check_catch()
root.mainloop()
