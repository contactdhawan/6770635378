import random
import time
from tkinter import Tk, Canvas, HIDDEN, NORMAL

root = Tk()
root.title('Snap')
c = Canvas(root, width=400, height=400)
c.pack()

colors = ['black', 'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink']
shapes = []

# Circles
for color in colors:
    shape = c.create_oval(35, 20, 365, 350, outline=color, fill=color, state=HIDDEN)
    shapes.append(('circle', color, shape))

# Rectangles
for color in colors:
    shape = c.create_rectangle(35, 100, 365, 270, outline=color, fill=color, state=HIDDEN)
    shapes.append(('rectangle', color, shape))

# Squares
for color in colors:
    shape = c.create_rectangle(100, 100, 300, 300, outline=color, fill=color, state=HIDDEN)
    shapes.append(('square', color, shape))

# Triangles
for color in colors:
    shape = c.create_polygon(200, 40, 360, 340, 40, 340, outline=color, fill=color, state=HIDDEN)
    shapes.append(('triangle', color, shape))

# Hexagons
for color in colors:
    shape = c.create_polygon(
        200, 30, 350, 120, 350, 280, 200, 370, 50, 280, 50, 120,
        outline=color, fill=color, state=HIDDEN)
    shapes.append(('hexagon', color, shape))

random.shuffle(shapes)

current_shape = None
previous_color = ''
current_color = ''
player1_score = 0
player2_score = 0

# Pass tracking
player1_passed = False
player2_passed = False

def next_shape():
    global current_shape, previous_color, current_color, player1_passed, player2_passed
    if current_shape is not None:
        c.itemconfigure(current_shape, state=HIDDEN)
    previous_color = current_color
    player1_passed = False
    player2_passed = False
    if len(shapes) > 0:
        shape_type, color, shape_id = shapes.pop()
        current_shape = shape_id
        current_color = color
        c.itemconfigure(current_shape, state=NORMAL)
    else:
        c.unbind('q')
        c.unbind('p')
        c.unbind('a')
        c.unbind('l')
        if player1_score > player2_score:
            c.create_text(200, 200, text='Winner : Player 1!')
        elif player1_score < player2_score:
            c.create_text(200, 200, text='Winner : Player 2!')
        else:
            c.create_text(200, 200, text='Draw')

def snap(event):
    global current_shape, player1_score, player2_score, player1_passed, player2_passed
    key = event.char.lower()
    valid = False
    if key == 'q' or key == 'p':
        if current_shape is not None:
            c.itemconfigure(current_shape, state=HIDDEN)
        if previous_color == current_color and previous_color != '':
            valid = True
        if valid:
            if key == 'q':
                player1_score += 1
            else:
                player2_score += 1
            msg = 'SNAP! You score 1 point!'
        else:
            if key == 'q':
                player1_score -= 1
            else:
                player2_score -= 1
            msg = 'Wrong! You lose 1 point!'
        temp_text = c.create_text(200, 200, text=msg)
        root.update_idletasks()
        time.sleep(2)
        c.delete(temp_text)
        next_shape()
    elif key == 'a':
        player1_passed = True
    elif key == 'l':
        player2_passed = True

    if player1_passed and player2_passed:
        if current_shape is not None:
            c.itemconfigure(current_shape, state=HIDDEN)
        next_shape()

c.bind('q', snap)
c.bind('p', snap)
c.bind('a', snap)
c.bind('l', snap)
c.focus_set()

root.after(3000, next_shape)
root.mainloop()