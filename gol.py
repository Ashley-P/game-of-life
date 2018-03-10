import tdl 
import time
import copy



### CONSTANTS ###
SCREEN_WIDTH = 150
SCREEN_HEIGHT = 80
INFO_HEIGHT = 1
PAUSED = True


def calculate_neighbours(x, y):
    neighbours = 0
 
    for i in (x-1, x, x+1):
        for j in (y-1, y, y+1): # Looping through all 9 surrounding squares
            if(i == x and j == y): # Don't count the middle square
                continue
            elif i < 0 or j < 0: # To prevent weird issues with wrapping
                continue
            else:
                try: # Preventing from searching out of bounds
                    neighbours += old_field[i][j]
                except IndexError:
                    pass

    return neighbours


def advance():
    global gen
    # Game Rules
    for x in range(len(new_field)):
        for xx in range(len(new_field[0])):
            neighbours = calculate_neighbours(x, xx)
             
            if (neighbours in (2, 3)) and (old_field[x][xx] == 1): # It's fine
                continue
            elif (neighbours == 3) and (old_field[x][xx] == 0): # Breeding
                new_field[x][xx] = 1
            elif (neighbours < 2) and (old_field[x][xx] == 1): # Underpopulation
                new_field[x][xx] = 0
            elif (neighbours > 3) and (old_field[x][xx] == 1): # Overpopulation
                new_field[x][xx] = 0
    gen += 1


if __name__ == "__main__":
    ### Initialisation ###
    tdl.set_font('Tocky_square_10x10.png', altLayout=False)
    root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Conway's Game of Life", fullscreen=False)
    main = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT - INFO_HEIGHT)
    info = tdl.Console(SCREEN_WIDTH, INFO_HEIGHT)

    t1 = time.time() # Setting up FPS counter
    t2 = 0.

    gen = 0 # Generation counter

    old_field = [[0 for x in range(SCREEN_HEIGHT - INFO_HEIGHT)] for xx in range(SCREEN_WIDTH)]
    new_field = [[0 for x in range(SCREEN_HEIGHT - INFO_HEIGHT)] for xx in range(SCREEN_WIDTH)]


    ### MAIN LOOP ###
    while not tdl.event.is_window_closed():

        # Drawing on the info panel
        info.draw_str(0, 0, "{:8.5f}".format(1 /  (t1 - t2)), bg=0x0) # Drawing the FPS
        info.draw_str(10, 0, "Generation : {}".format(gen))
        if PAUSED:
            info.draw_str(-6, 0, "PAUSED")

        # Drawing new_field to the main console
        for x in range(len(new_field)):
            for xx in range(len(new_field[0])):
                if new_field[x][xx] == 0:
                    main.draw_char(x, xx, ' ', fg=0xFFFFFF, bg=0x0)
                elif new_field[x][xx] == 1:
                    main.draw_char(x, xx, ' ', fg=0x0, bg=0xFFFFFF)

        # Rules happen in this function
        if not PAUSED:
            advance()

        # Handling input
        for event in tdl.event.get():
            if event.type == 'MOUSEDOWN':
                c = event.cell
                if event.button == 'LEFT': # Makes the selected cell alive
                    try:
                        new_field[c[0]][c[1]] = 1
                    except IndexError:
                        pass
                elif event.button == 'RIGHT': # Makes the selected cell dead
                    try:
                        new_field[c[0]][c[1]] = 0
                    except IndexError:
                        pass

            elif event.type == 'MOUSEMOTION':
                # TODO: Implement Clicking and dragging
                pass
                
            elif event.type == 'KEYDOWN':
                if event.keychar == 'ESCAPE': # Resets the field
                    new_field = [[0 for x in range(SCREEN_HEIGHT - INFO_HEIGHT)] for xx in range(SCREEN_WIDTH)]
                    gen = 0
                elif event.keychar == 'SPACE': # Pauses and unpauses the game
                    PAUSED = not PAUSED
                elif event.keychar == '.': # Advances by 1 generation when the game is paused
                    if PAUSED:
                        advance()

        # Blitting to the root window
        root.blit(main)
        root.blit(info, x=0, y=SCREEN_HEIGHT - INFO_HEIGHT)
        tdl.flush()

        main.clear()
        info.clear()

        old_field = copy.deepcopy(new_field)

        # Calculating FPS
        t2 = t1
        t1 = time.time()
