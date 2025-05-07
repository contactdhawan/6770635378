import random
import turtle as t

t.bgcolor('yellow')

caterpillar = t.Turtle()
caterpillar.shape('square')
caterpillar.color('red')
caterpillar.speed(0)
caterpillar.penup()
caterpillar.hideturtle()
caterpillar2 = t.Turtle()
caterpillar2.shape('square')
caterpillar2.color('blue')
caterpillar2.penup()
caterpillar2.speed(0)
caterpillar2.hideturtle()

leaf = t.Turtle()
leaf_shape = ((0, 0), (14, 2), (18, 6), (20, 20), (6, 18), (2, 14))
t.register_shape('leaf', leaf_shape)
leaf.shape('leaf')
leaf.color('green')
leaf.penup()
leaf.hideturtle()
leaf.speed(0)

game_started = False
text_turtle = t.Turtle()
text_turtle.write('Press "space" to start the game', align='center', font=('Arial', 16, 'bold'))
text_turtle.hideturtle()

score_turtle = t.Turtle()
score_turtle.hideturtle()
score_turtle.speed(0)

game_over_turtle = t.Turtle()
game_over_turtle.hideturtle()

def outside_window(caterpillar):
    left_wall = -t.window_width() / 2
    right_wall = t.window_width() / 2
    top_wall = t.window_height() / 2
    bottom_wall = -t.window_height() / 2
    (x, y) = caterpillar.pos()
    return x < left_wall or x > right_wall or y < bottom_wall or y > top_wall

def game_over():
    caterpillar.color('yellow')
    caterpillar2.color('yellow')
    leaf.color('yellow')
    game_over_turtle.clear()  # Clear any previous "GAME OVER!" text
    game_over_turtle.penup()
    game_over_turtle.hideturtle()
    game_over_turtle.write('GAME OVER! Press "R" to restart', align='center', font=('Arial', 30, 'normal'))

def reset_game():
    global game_started
    game_started = False
    caterpillar.hideturtle()
    caterpillar.setpos(0, 0)
    caterpillar.setheading(0)
    caterpillar.shapesize(1, 3, 1)
    caterpillar.color('red')
    caterpillar2.hideturtle()
    caterpillar2.setpos(0, 0)
    caterpillar2.setheading(0)
    caterpillar2.shapesize(1, 3, 1)
    caterpillar2.color('blue')
    text_turtle.clear()  # Clear the text turtle
    score_turtle.clear()  # Clear the score turtle
    game_over_turtle.clear()  # Clear the "GAME OVER!" text
    text_turtle.write('Press "space" to start the game', align='center', font=('Arial', 16, 'bold'))
    place_leaf()  # Ensure the leaf is placed and visible

def display_score(current_score):
    score_turtle.clear()
    score_turtle.penup()
    x = (t.window_width() / 2) - 50
    y = (t.window_height() / 2) - 50
    score_turtle.setpos(x, y)
    score_turtle.write(str(current_score), align='right', font=('Arial', 40, 'bold'))

def place_leaf():
    random_number = random.randint(1, 10000000)  # Generate a random number between 1 and 10000000
    print(f"Placing Leaf.......{random_number}")  # Debugging message with random number
    leaf.color('green')
    leaf.ht()  # Hide the leaf while repositioning
    max_x = (t.window_width() // 2) - 40  # Ensure the leaf stays visible
    max_y = (t.window_height() // 2) - 40  # Ensure the leaf stays visible
    leaf.setx(random.randint(-max_x, max_x))
    leaf.sety(random.randint(-max_y, max_y))
    leaf.st()  # Show the leaf after repositioning

def start_game():
    global game_started
    if game_started:
        return
    game_started = True

    score = 0
    text_turtle.clear()
    game_over_turtle.clear()  # Clear the "GAME OVER!" text when starting a new game

    caterpillar_speed = 2
    caterpillar_length = 3
    caterpillar.shapesize(1, caterpillar_length, 1)
    caterpillar.showturtle()
    caterpillar2.shapesize(1, caterpillar_length, 1)
    caterpillar2.setheading(180)
    caterpillar2.showturtle()
    display_score(score)
    place_leaf()  # Place the leaf at the start of the game

    while True:
        caterpillar.forward(caterpillar_speed)
        caterpillar2.forward(caterpillar_speed)
        if caterpillar.distance(leaf) < 70 or leaf.distance(caterpillar2) < 70:
            place_leaf()
            caterpillar_length += 1
            caterpillar.shapesize(1, caterpillar_length, 1)
            caterpillar2.shapesize(1, caterpillar_length, 1)
            caterpillar_speed += 1
            score += 100
            display_score(score)
        if outside_window(caterpillar) or outside_window(caterpillar2):
            game_over()
            break

def move_up():
    if caterpillar.heading() == 0 or caterpillar.heading() == 180:
        caterpillar.setheading(90)

def move_down():
    if caterpillar.heading() == 0 or caterpillar.heading() == 180:
        caterpillar.setheading(270)

def move_left():
    if caterpillar.heading() == 90 or caterpillar.heading() == 270:
        caterpillar.setheading(180)

def move_right():
    if caterpillar.heading() == 90 or caterpillar.heading() == 270:
        caterpillar.setheading(0)

def caterpillar2_up():
    if caterpillar2.heading() == 0 or caterpillar2.heading() == 180:
        caterpillar2.setheading(90)

def caterpillar2_down():
    if caterpillar2.heading() == 0 or caterpillar2.heading() == 180:
        caterpillar2.setheading(270)

def caterpillar2_left():
    if caterpillar2.heading() == 90 or caterpillar2.heading() == 270:
        caterpillar2.setheading(180)

def caterpillar2_right():
    if caterpillar2.heading() == 90 or caterpillar2.heading() == 270:
        caterpillar2.setheading(0)

t.onkey(caterpillar2_up, 'w')
t.onkey(caterpillar2_down, 's')
t.onkey(caterpillar2_left, 'a')
t.onkey(caterpillar2_right, 'd')

t.onkey(start_game, 'space')
t.onkey(move_up, 'Up')
t.onkey(move_down, 'Down')
t.onkey(move_left, 'Left')
t.onkey(move_right, 'Right')
t.onkey(reset_game, 'r')  # Bind the reset_game function to the "R" key
t.listen()
t.mainloop()