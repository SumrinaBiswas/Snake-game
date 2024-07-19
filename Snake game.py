import turtle as t
import random

w = 700  # Width of box
h = 700  # Height of box
food_size = 15  # Size of food
delay = 70  # in milliseconds

# Values by which the snake will move in direction when given direction
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}

global SCORE
SCORE = 0

# Default position of game scene
def reset():
    global snake, snake_dir, food_position, pen, score_pen
    snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
    snake_dir = "up"  # Default snake direction
    food_position = get_random_food_position()
    food.goto(food_position)  # Render food on scene
    SCORE = 0
    update_score()
    move_snake()

def move_snake():
    global snake_dir, SCORE
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_dir][0]
    new_head[1] = snake[-1][1] + offsets[snake_dir][1]
    
    if new_head in snake[:-1]:
        game_over()
    else:
        snake.append(new_head)
        if not food_collision():
            snake.pop(0)
        if snake[-1][0] > w / 2:
            snake[-1][0] -= w
        elif snake[-1][0] < -w / 2:
            snake[-1][0] += w
        elif snake[-1][1] > h / 2:
            snake[-1][1] -= h
        elif snake[-1][1] < -h / 2:
            snake[-1][1] += h

        pen.clearstamps()
        for index, segment in enumerate(snake):
            pen.goto(segment[0], segment[1])
            # Gradually decrease the size of the segments towards the tail
            size = 1 - (index / len(snake)) * 0.5  # Adjust this value for tail size
            if index == len(snake) - 1:
                size = 0.8  # Adjust the head size here
            pen.shapesize(size)
            # Apply a gradient color effect
            r = int(255 * (1 - index / len(snake)))
            g = int(255 * (index / len(snake)))
            b = 0
            pen.color(r / 255, g / 255, b / 255)
            pen.stamp()
        
        update_score()  # Update the score display
        screen.update()
        t.ontimer(move_snake, delay)

# If snake collides with food
def food_collision():
    global food_position, SCORE
    if get_distance(snake[-1], food_position) < 20:
        SCORE += 10
        food_position = get_random_food_position()
        food.goto(food_position)
        return True
    return False

# Random position for food
def get_random_food_position():
    x = random.randint(-w / 2 + food_size, w / 2 - food_size)
    y = random.randint(-h / 2 + food_size, h / 2 - food_size)
    return (x, y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

# Control
def go_up():
    global snake_dir
    if snake_dir != "down":
        snake_dir = "up"

def go_down():
    global snake_dir
    if snake_dir != "up":
        snake_dir = "down"

def go_left():
    global snake_dir
    if snake_dir != "right":
        snake_dir = "left"

def go_right():
    global snake_dir
    if snake_dir != "left":
        snake_dir = "right"

def game_over():
    global SCORE
    pen.clearstamps()
    pen.goto(0, 0)
    reset()
    pen.write(f"Game Over!Previous Score: {SCORE}", align="center", font=("Arial", 24, "bold"))
    SCORE = 0
    update_score()
    screen.update()

def update_score():
    score_pen.clear()
    score_pen.goto(-w / 2 + 50, h / 2 - 50)
    score_pen.write(f"Score: {SCORE}", align="left", font=("Arial", 20, "normal"))

# Define screen setup
screen = t.Screen()
screen.setup(w, h)
screen.title("Sumrina's Snake Game")
screen.bgcolor("light green")
screen.tracer(0)

# Define snake setup
pen = t.Turtle("circle")
pen.color("blue")
pen.penup()

# Define food setup
food = t.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(food_size / 20)
food.penup()

# Score setup
score_pen = t.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("black")

# Define control setup
screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")

reset()
t.done()