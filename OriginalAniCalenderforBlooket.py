from tkinter import Tk, Canvas
from datetime import datetime
from zoneinfo import ZoneInfo  # Requires Python 3.9+

def getCurrentEvent(event_details):
    # Split the string into event name and datetime string
    current_event = event_details.split(',')
    # Parse the event datetime using the given format (day/month/year hour:minute)
    event_datetime = datetime.strptime(current_event[1], '%d/%m/%y %H:%M')
    # Attach the CST timezone (America/Chicago)
    
    # event_datetime = event_datetime.replace(tzinfo=ZoneInfo("America/Chicago"))
    current_event[1] = event_datetime
    return current_event

def get_events():
    # Change the event to something happening at 10:28 (22:28) today.
    return [
    # Put events here, should be in the format "Event Name,DD/MM/YY HH:MM"
        getCurrentEvent("Gold Quest-Infinite Coins Daily30mins,14/04/25 16:28"),
        getCurrentEvent("Monster Brawl-Infinite Coins Daily30mins,14/04/25 18:30"),    
        getCurrentEvent("Crypto Hack-Infinite Coins Daily30mins,13/04/25 12:30"),
        getCurrentEvent("Test Event 2,05/04/25 15:30"),
        getCurrentEvent("Test Event 3,06/04/25 15:30")
    ]

def get_time_left(future_datetime, now_datetime):
    print (future_datetime, now_datetime)
    delta = future_datetime - now_datetime
    seconds_left = delta.total_seconds()
    if seconds_left < 0:
        return "Event Passed", "gray"
    hours = int(seconds_left / 3600)
    minutes = int((seconds_left % 3600) // 60)

    # Determine the color based on hours left
    if hours >= 5:
        color = "lightgreen"
    elif 3 <= hours < 5:
        color = "yellow"
    else:
        color = "red"

    return f"{hours} hrs {minutes} mins", color

# Setup the main GUI window
root = Tk()
c = Canvas(root, width=1500, height=1500, bg='black')
c.pack()

# Title text (unchanged design)
c.create_text(100, 50, anchor='w', fill='orange', font='Arial 28 bold underline',
              text='Blooket Live Countdown Calendar for SG Tournaments')

# Retrieve events and initialize canvas text items for each event
events = get_events()
text_items = []
start_y = 100
for i in range(len(events)):
    text_item = c.create_text(100, start_y + i * 40, anchor='w', fill='lightblue',
                              font='Arial 28 bold', text='')
    text_items.append(text_item)

def update_countdowns():
    now = datetime.now()
    print("Current time:", now)
    for i, event in enumerate(events):
        name = event[0]
        event_time = event[1]
        time_left_str, color = get_time_left(event_time, now)
        c.itemconfig(text_items[i], text=f"It is {time_left_str} until {name}", fill=color)
    # Update the countdown every second
    root.after(1000, update_countdowns)

update_countdowns()
root.mainloop()
