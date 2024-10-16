#from cProfile import label
from tkinter import *
import random

#Adding some constant values to begin
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100  #the lower the value, the faster the game will be
SPACE_SIZE = 50
BODY_PARTS = 3 #starting snake body size
SNAKE_COLOR = "#00FF00"  #green color for the snake
FOOD_COLOR = "#FF0000" #red color for the food
BACKGROUND_COLOR = "#000000" #black color for the background


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [] #List of coordinates
        self.squares = [] #List of square graphics

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates: #List of lists
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # Placing food object randomly
        # Viewing the game_board similarly to a chess board, (Therefore there are 700/50 possible spots in each axis)
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE #multiplying by space size to convert to pixels
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y] #Setting cordinates

        #Drawing food object in canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag = "food")



def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE #moving 1 space up

    elif direction == "down":
        y += SPACE_SIZE #moving 1 space down

    elif direction == "left":
        x -= SPACE_SIZE #moving 1 space left

    elif direction == "right":
        x += SPACE_SIZE #moving 1 space right


    snake.coordinates.insert(0, (x, y)) #updating the coordinates of the head of the snake
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR) #New graphic for the head of the snake
    snake.squares.insert(0, square) #updating snake's list of squares


    if x == food.coordinates[0] and y == food.coordinates[1]: #Means they are overlapping
        #Increasing the score
        global score
        score += 1

        label.config(text=f"Score: {score}")

        #Deleting food object and recreating it
        canvas.delete("food")
        food = Food()

    else:
        #Deleting the last body part of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    #Checking collisions
    if check_collisions(snake):
        game_over() #Calling gameover function if there is a collision
    else:
        window.after(SPEED, next_turn, snake, food) #Updating to the next turn if there is no collision


def change_direction(new_direction):
    global direction #Old direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0] #Unpacking the head of the snake

    if x<0 or x>= GAME_WIDTH: #Checking to see if snake has crossed the left or right border of the game
        #print("GAME OVER") #For testing
        return True
    elif y<0 or y>= GAME_HEIGHT: #Checking to see if snake has crossed the top or bottom border of the game
        # print("GAME OVER") #For testing
        return True

    for body_part in snake.coordinates[1:]: #If snake touches its body
        if x == body_part[0] and y == body_part[1]:
            #print("GAME OVER") #For testing
            return True

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score),font=("consolas", 40))
label.pack()

canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

#Window Sizing
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#Adjusting the position of window
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}") #This will load the window in the center

#Binding keys for controls
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()