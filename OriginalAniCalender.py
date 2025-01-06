from tkinter import Tk, Canvas
from datetime import date, datetime
def getCurrentEvent(event_details):
    current_event = event_details.split(',')
    event_date = datetime.strptime(current_event[1], '%m/%d/%y').date()
    current_event[1] = event_date
    return current_event

def get_events():
    list_events = []
    list_events.append(getCurrentEvent('School Starts,1/7/25'))
    list_events.append(getCurrentEvent('Anirudh\'s Birthday,05/06/25'))
    list_events.append(getCurrentEvent('Mumma\'s Birthday,07/06/25'))
    list_events.append(getCurrentEvent('Papa\'s Birthday,01/03/26'))
    list_events.append(getCurrentEvent('Book Share Commercial,01/31/25'))
    list_events.append(getCurrentEvent('New Book Share Commercial,02/27/25'))
    return list_events
    
def days_between_dates(date1, date2):
    time_between = str(date1-date2)
    number_of_days = time_between.split(' ')
    return number_of_days[0]

root = Tk()
c = Canvas(root , width=10000, height=10000, bg='black')
c.pack()
c.create_text(100, 50, anchor='w', fill='blue', font='Arial 36 bold underline', text = 'Anirudh\'s Countdown Calendar')

events = get_events()
today = date.today()
verticle_sapce = 100
events.sort(key=lambda x: x[1])
for event in events:
    event_name = event[0]
    days_until = days_between_dates(event[1], today)
    display = 'It is %s days until %s ' % (days_until, event_name)
    if (int(days_until) <=7):
        text_col = 'red'
    elif (int(days_until) <=14):
        text_col = 'yellow'
    else:
        text_col = 'green'
    c.create_text(100, verticle_sapce, anchor='w', fill=text_col, font='Courier 28 ', text = display)
    verticle_sapce += 30

root.mainloop()


