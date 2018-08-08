import random
import curses

# Initialize the screen
screen = curses.initscr()
# Hide the cursor
curses.curs_set(0)

# Get the width and the height from the max
screenh, screenw = screen.getmaxyx()
# Create the new window
window = curses.newwin(screenh, screenw, 0, 0)

window.keypad(1)
window.timeout(100)

# Now for the snake spawn logic
snake_x = screenw/4
snake_y = screenh/2
# Snake starting body
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x-1],
    [snake_y, snake_x-2]
]

# Give the snake something to eat in the middle of the screen
food = [screenh/2, screenw/2]
window.addch(int(food[0]), int(food[1]), curses.ACS_PI)

# Tell the snake where he starts going initially
key = curses.KEY_RIGHT

# While the game is going
while True:
    next_key = window.getch()
    # Gives us either nothing or the next key
    key = key if next_key == -1 else next_key

    # Loss conditions:
    # If the y pos is at the bottom or height of the screen or the x pos is at the left or width of the screen or if the snake is inside itself
    if snake[0][0] in [0, screenh] or snake[0][1] in [0, screenw] or snake[0] in snake[1:]:
        # Kill the window and game
        curses.endwin()
        quit()
    
    # Control the snake
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    
    snake.insert(0, new_head)

    if snake[0] == food:
        food = None
        # If there's no food
        while food is None:
            nf = [
                # Random y between 1 and the the height -1
                random.randint(1, screenh-1),
                # Random x between 1 and the width -1
                random.randint(1, screenw-1)
            ]
            food = nf if nf not in snake else None
        # Add the food to the window
        window.addch(food[0], food[1], curses.ACS_PI)
    else:
        tail = snake.pop()
        # Add a space where the tail used to be
        window.addch(int(tail[0]), int(tail[1]), ' ')
    
    # Head of the snake
    window.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
