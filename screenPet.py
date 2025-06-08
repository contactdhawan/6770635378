from tkinter import HIDDEN, NORMAL, Tk, Canvas

root = Tk()
root.title("My screen pet")

# --- Sad timer variables ---
SAD_TIMEOUT = 20000  # 20 seconds in milliseconds before bunny gets sad
sad_timer_id = None  # To store the after() id for cancelling/resetting timer

def reset_sad_timer():
    # Reset the timer that makes the bunny sad after inactivity
    global sad_timer_id
    if sad_timer_id is not None:
        root.after_cancel(sad_timer_id)
    sad_timer_id = root.after(SAD_TIMEOUT, make_sad)

def make_sad():
    # Change bunny's face to sad expression
    c.itemconfigure(mouth_normal, state=HIDDEN)
    c.itemconfigure(mouth_happy, state=HIDDEN)
    c.itemconfigure(mouth_sad, state=NORMAL)
    c.itemconfigure(cheek_left, state=HIDDEN)
    c.itemconfigure(cheek_right, state=HIDDEN)

def toggle_eyes():
    # Toggle bunny's eyes between open and closed (for blinking)
    current_color = c.itemcget(eye_left, 'fill')
    new_color = c.body_color if current_color == 'white' else 'white'
    current_state = c.itemcget(pupil_left, 'state')
    new_state = NORMAL if current_state == HIDDEN else HIDDEN
    c.itemconfigure(pupil_left, state=new_state)
    c.itemconfigure(eye_left, fill=new_color)
    c.itemconfigure(pupil_right, state=new_state)
    c.itemconfigure(eye_right, fill=new_color)

def blink():
    # Make the bunny blink every few seconds
    toggle_eyes()
    root.after(250, toggle_eyes)
    root.after(3000, blink)

def show_happy(event):
    # Show happy face and cheeks when mouse moves over bunny
    reset_sad_timer()
    if (20 <= event.x and event.x <= 350) and (20 <= event.y and event.y <= 350):
        c.itemconfigure(cheek_left, state=NORMAL)
        c.itemconfigure(cheek_right, state=NORMAL)
        c.itemconfigure(mouth_happy, state=NORMAL)
        c.itemconfigure(mouth_normal, state=HIDDEN)
        c.itemconfigure(mouth_sad, state=HIDDEN)
    return

def hide_happy(event):
    # Hide happy face and cheeks when mouse leaves bunny
    reset_sad_timer()
    c.itemconfigure(cheek_left, state=HIDDEN)
    c.itemconfigure(cheek_right, state=HIDDEN)
    c.itemconfigure(mouth_happy, state=HIDDEN)
    c.itemconfigure(mouth_normal, state=NORMAL)
    c.itemconfigure(mouth_sad, state=HIDDEN)
    return

def toggle_tounge():
    # Show or hide the bunny's tongue
    reset_sad_timer()
    if not c.toungue_out:
        c.itemconfigure(tounge_tip, state=NORMAL)
        c.itemconfigure(tounge_main, state=NORMAL)
        c.toungue_out = True
    else:
        c.itemconfigure(tounge_tip, state=HIDDEN)
        c.itemconfigure(tounge_main, state=HIDDEN)
        c.toungue_out = False
    return

def toggle_pupil():
    # Cross or uncross the bunny's eyes
    reset_sad_timer()
    if not c.eyes_crossed:
        c.move(pupil_left, 10, -5)
        c.move(pupil_right, -10, -5)
        c.eyes_crossed = True
    else:
        c.move(pupil_left, -10, 5)
        c.move(pupil_right, 10, 5)
        c.eyes_crossed = False
    return

def cheeky(event):
    # Make the bunny cheeky: stick out tongue and cross eyes
    reset_sad_timer()
    toggle_tounge()
    toggle_pupil()
    hide_happy(event)
    root.after(1000, toggle_tounge)
    root.after(1000, toggle_pupil)
    return

def sad(event):
    # Set bunny's face to sad on certain events
    reset_sad_timer()
    c.itemconfigure(mouth_normal, state=HIDDEN)
    c.itemconfigure(mouth_happy, state=HIDDEN)
    c.itemconfigure(mouth_sad, state=NORMAL)
    return

# --- Drawing the bunny using canvas shapes ---
c = Canvas(root, width=400, height=400)
c.configure(bg='dark blue', highlightthickness=0)
c.body_color = 'skyBlue1'

# Bunny's body parts
body = c.create_oval(35, 20, 365, 350, outline=c.body_color, fill=c.body_color)
ear_left = c.create_polygon(75, 80, 75, 10, 165, 70, outline=c.body_color, fill=c.body_color)
ear_right = c.create_polygon(225, 45, 325, 10, 320, 70, outline=c.body_color, fill=c.body_color)
foot_left = c.create_oval(65, 320, 145, 360, outline=c.body_color, fill=c.body_color)
foot_right = c.create_oval(250, 320, 330, 360, outline=c.body_color, fill=c.body_color)

# Eyes and pupils
eye_left = c.create_oval(130, 110, 160, 170, outline='black', fill='white')
eye_right = c.create_oval(230, 110, 260, 170, outline='black', fill='white')
pupil_left = c.create_oval(140, 145, 150, 155, outline='black', fill='black')
pupil_right = c.create_oval(240, 145, 250, 155, outline='black', fill='black')

# Mouths for different expressions
mouth_normal = c.create_line(170, 250, 200, 272, 230, 250, smooth=1, width=2, state=NORMAL)
mouth_happy = c.create_line(170, 250, 200, 282, 230, 250, smooth=1, width=2, state=HIDDEN)
mouth_sad = c.create_line(170, 250, 200, 232, 230, 250, smooth=1, width=2, state=HIDDEN)

# Tongue (hidden by default)
tounge_main = c.create_rectangle(170, 250, 230, 290, outline='red', fill='red', state=HIDDEN)
tounge_tip = c.create_oval(170, 285, 230, 300, outline='red', fill='red', state=HIDDEN)

# Cheeks (hidden by default)
cheek_left = c.create_oval(70, 180, 120, 230, outline='pink', fill='pink', state=HIDDEN)
cheek_right = c.create_oval(280, 180, 330, 230, outline='pink', fill='pink', state=HIDDEN)

c.pack()

# --- Bind mouse events to bunny's reactions ---
c.bind('<Motion>', show_happy)      # Mouse moves over bunny
c.bind('<Leave>', hide_happy)       # Mouse leaves bunny
c.bind('<Double-1>', cheeky)        # Double-click for cheeky face

# --- Custom attributes for state ---
c.eyes_crossed = False
c.toungue_out = False

reset_sad_timer()  # Start the sad timer
root.after(1000, blink)  # Start blinking loop
root.mainloop()  # Start the Tkinter event loop
