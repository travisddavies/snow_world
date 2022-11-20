import random, sys, os, pygame, time
from pygame.locals import *

FPS = 30 # frames per second to update the screen
WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 600 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2) # half the width of the window, in pixels
HALF_WINHEIGHT = int(WINHEIGHT / 2) # half the height of the window, in pixels
CAMERASLACK = 50 # the slack that is given for the camera following the character

TILEHEIGHT = 50 # height of the tiles
TILEWIDTH = 80 # width of the tiles
AMIGO_SIZE = 50 # the size of the player's sprite
SNOWMAN_WIDTH = 60 # the width of the snowmen
SNOWMAN_HEIGHT = 60 # the height of the snowmen
SQUASHED_SNOWMAN_WIDTH = 60 # the width of the squashed snowmen
SQUASHED_SNOWMAN_HEIGHT = 40 # the height of the squasehd snowmen
FLAG_HEIGHT = 200 # height of the flag
FLAG_WIDTH = 100 # width of the flag

# COLOURS     R    G    B
WHITE =      (255, 255, 255) 
LIGHTBLUE =  (214, 255, 255)
NAVYBLUE =    (60,  60, 100)
CYAN =         (0, 255, 255)
ELTRC_BLUE = (125, 249, 255)
BGCOLOR = ELTRC_BLUE # colour of the game's background
TEXTCOLOR = WHITE # colour of the game's text

VELOCITY = 10 # speed of the player's sprite
GRAVITY = 1 # acceleration of gravity
JUMPFORCE = 15 # initial speed of the jump in pixels

SNOWMAN_MAX_VELOCITY = 15 # max speed of the enemy sprites
SNOWMAN_MIN_VELOCITY = 5 # min speed of the enemy sprites

# syntactic sugar for the direction of the player's sprite
LEFT = 'left' 
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

JUMPSPEED = 20 # how fast the player's sprite can jump
JUMPHEIGHT = 100 # how high the player's sprite can jump

FLOOR = HALF_WINHEIGHT # the y-coordinate of the floor of the game

COLLISION_TOLERANCE = 20 # the tolerance allowed for collisions between sprites

INVULNTIME = 2 # how long the player is invulnerable after being hit in seconds

def main():
    """
    This is the main program.
    """
    # turn various variables in the main function that will be used in different functions into global variables
    global FPSCLOCK, DISPLAYSURF, TILEMAPPING, SNOWMEN, R_AMIGOS, L_AMIGOS, START_SCREEN, BASICFONT, LIFE, SOUNDS, BACKGROUND_IMAGE, FLAG
    # initialising the pygame library
    pygame.init()

    # the window and clock for the game
    FPSCLOCK = pygame.time.Clock() # clock for the game to control how fast the game updates
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) # setting the dimensions of the game's window 
    pygame.display.set_caption('Snow World') # setting the caption seen on the top of the window

    BASICFONT = pygame.font.Font('freesansbold.ttf', 25) # the font for the text used in the game

    START_SCREEN = pygame.image.load('data/snow_world.png') # loading the start screen image for the game
    START_SCREEN = pygame.transform.scale(START_SCREEN, (WINWIDTH, WINHEIGHT)) # scaling the start screen image to fit the entire window

    BACKGROUND_IMAGE = pygame.image.load('data/background.png') # loading the background image for the game
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINWIDTH, WINHEIGHT)) # scaling the background image to fit the entire window

    # loading all sprites of the player used in the game (right facing)
    R_AMIGO1 = pygame.image.load('data/character1.png')
    R_AMIGO2 = pygame.image.load('data/character2.png') 
    R_AMIGO3 = pygame.image.load('data/character3.png')
    R_JUMP_AMIGO = pygame.image.load('data/character_jump.png')

    # making copies of all loaded sprites and flipping them to face left
    L_AMIGO1 = pygame.transform.flip(R_AMIGO1, True, False) 
    L_AMIGO2 = pygame.transform.flip(R_AMIGO2, True, False) 
    L_AMIGO3 = pygame.transform.flip(R_AMIGO3, True, False) 
    L_JUMP_AMIGO = pygame.transform.flip(R_JUMP_AMIGO, True, False)

    LIFE = pygame.transform.scale(R_AMIGO1, (20, 20)) # scaling R_AMIGO1 to a smaller size to represent the lives of the player

    SNOW = pygame.image.load('data/snow.png') # loading the snow tile that will be used as the platform for the game
    SNOWMAN = pygame.image.load('data/snowman.png') # loading the snowman sprite which is the enemy of the game
    SQUASHED_SNOWMAN = pygame.image.load('data/squashed_snowman.png') # loading the squashed snowman which is the sprite after it has died

    # adding all right-facing sprites to one dictionary, the keys will act as an index for the 'run_position' 
    # to easily reference each different sprite in the game loop
    R_AMIGOS = {0: pygame.transform.scale(R_AMIGO1, (AMIGO_SIZE, AMIGO_SIZE)), 
                1: pygame.transform.scale(R_AMIGO2, (AMIGO_SIZE, AMIGO_SIZE)), 
                2: pygame.transform.scale(R_AMIGO3, (AMIGO_SIZE, AMIGO_SIZE)),
                3: pygame.transform.scale(R_JUMP_AMIGO, (AMIGO_SIZE, AMIGO_SIZE))}

    # adding all left-facing sprites to one dictionary, using the keys as an index much like the dictionary above
    L_AMIGOS = {0: pygame.transform.scale(L_AMIGO1, (AMIGO_SIZE, AMIGO_SIZE)), 
                1: pygame.transform.scale(L_AMIGO2, (AMIGO_SIZE, AMIGO_SIZE)), 
                2: pygame.transform.scale(L_AMIGO3, (AMIGO_SIZE, AMIGO_SIZE)),
                3: pygame.transform.scale(L_JUMP_AMIGO, (AMIGO_SIZE, AMIGO_SIZE))}
    
    # loading the snow tile into a dictionary
    TILE_DICT = {'snow': pygame.transform.scale(SNOW, (TILEWIDTH, TILEHEIGHT))}

    TILEMAPPING = {'#': TILE_DICT['snow']}

    # loading the snowman sprites into a dictionary
    SNOWMEN = {0: pygame.transform.scale(SNOWMAN, (SNOWMAN_WIDTH, SNOWMAN_HEIGHT)),
               1: pygame.transform.scale(SQUASHED_SNOWMAN, (SQUASHED_SNOWMAN_WIDTH, SQUASHED_SNOWMAN_HEIGHT)),
               2: pygame.transform.scale(SNOWMAN, (20, 22))}

    # loading the finishline flag into the game and scaling it to size
    FLAG = pygame.image.load('data/flag.png')
    FLAG = pygame.transform.scale(FLAG, (FLAG_WIDTH, FLAG_HEIGHT))

    # loading all the sounds that will be used throughout the game into a dictionary
    SOUNDS = {'coin': pygame.mixer.Sound(file='data/coin.wav'),
              'jump': pygame.mixer.Sound(file='data/jump.wav'),
              'gameover': pygame.mixer.Sound(file='data/gameover.wav'),
              'hit': pygame.mixer.Sound(file='data/hit.wav'),
              'goal': pygame.mixer.Sound(file='data/goal.wav')}
    
    # shows the start screen of the game
    showStartScreen()

    # the loop that runs back and forth from game over and the game loop
    while True:
        runGame()
        if gameOverMode:
            showGameOverScreen()


def runGame():
    """The function where the game is run"""
    
    # declaring the gameOverMode boolean variable so it can be called in the main function
    global gameOverMode

    # the text used for when the player wins the game
    winnerFont = pygame.font.Font('freesansbold.ttf', 150) # font of the text
    winnerSurf = winnerFont.render('Winner!', True, TEXTCOLOR) # rendering the text to be shown on the screen and its colour
    # producing a rectangle for the text and positioning it to the centre of the screen
    winnerRect = winnerSurf.get_rect()
    winnerRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    pressKeySurf = BASICFONT.render("Press any key to restart!", True, TEXTCOLOR) # rendering the 'press any key' text to be shown on the screen
    # producing a rectangle for the text and positioning it to the centre of the screen
    pressKeyRect = pressKeySurf.get_rect() 
    pressKeyRect.centerx = HALF_WINWIDTH
    pressKeyRect.centery = HALF_WINHEIGHT + 75

    # initially turning off all Boolean switches for controlling the player's sprite
    moveLeft = False
    moveRight = False
    Jumping = False
    Falling = False
    invulnerableMode = False
    flashIsOn = False
    gameOverMode = False 
    winMode = False

    # initially setting the invulnerable start time variable to 0.
    invulnerableStartTime = 0    
    
    # intially setting the camera coordinates to (0, 0)
    camerax = 0
    cameray = 0    
    
    # creating acceleration for the gravity
    gravity_acc = GRAVITY
    jumpmotion = JUMPFORCE    
    
    # load tile map
    map_dict = readMapFile('map.txt')

    snowmenObj = map_dict['gamestate']['snowmen'] # the dictionary for the snowmen
    playerObj = map_dict['gamestate']['player'] # the dictionary for the player
    flagObj = map_dict['gamestate']['flag'] # the dictionary for the flag
    mapObj = map_dict['mapObj'] # the map of the game

    snowmen_left = len(snowmenObj) # the amount of snowmen that haven't been killed

    # loading the theme music into the game
    pygame.mixer.music.load(filename='data/Firecracker.wav')
    pygame.mixer.music.play(-1, 0.0)    
    
    # game loop
    while True:
        # Check if we should turn off invulnerability
        if invulnerableMode and time.time() - invulnerableStartTime > INVULNTIME:
            invulnerableMode = False

        # set background colour of the game
        DISPLAYSURF.fill(BGCOLOR)
 
        # finds the coordinates of the center of the sprite for the camera to follow.
        playerCenterx = playerObj['x'] + int(AMIGO_SIZE / 2)

        # find where the floor is in relation to the player
        floor = findFloor(mapObj, playerObj, AMIGO_SIZE)

        # map width and height
        mapWidth = len(mapObj) * TILEWIDTH
        mapHeight = (len(mapObj[0])) *  TILEHEIGHT

        # turning on/off Boolean switch when character is supposed to fall
        if not isGround(mapObj, playerObj, AMIGO_SIZE, AMIGO_SIZE) and not Jumping: 
            Falling = True
        else:
            Falling = False
            gravity_acc = GRAVITY

        # moving the snowmen left.
        for snowman in snowmenObj:
            if snowman['velocity'] > 0:
                snowman['direction'] = RIGHT
            elif snowman['velocity'] < 0:
                snowman['direction'] = LEFT             

        # event handling loop
        for event in pygame.event.get(): 
            # handling quit events
            if event.type == QUIT: 
                terminate()

            # handling keydown events
            elif event.type == KEYDOWN:
                # turning on Boolean swtch for horizontal movements when appropriate key is pressed down.
                if event.key in (K_a, K_LEFT):
                    moveLeft = True
                    moveRight = False
                if event.key in (K_d, K_RIGHT):
                    moveRight = True
                    moveLeft = False
                    
                # turning on Boolean switch for jumping when space bar button pressed down
                if event.key == K_SPACE:
                    if Jumping == False:
                        SOUNDS['jump'].play()
                        Jumping = True

            # handling keyup events
            elif event.type == KEYUP:
                # quitting program when a escape button keyup event occurs
                if event.key == K_ESCAPE:
                    terminate()

                # turning off Boolean switch for horizontal movements
                elif event.key in (K_a, K_LEFT):
                    moveLeft = False
                    playerObj['run_position'] = 0
                elif event.key in (K_d, K_RIGHT):
                    moveRight = False
                    playerObj['run_position'] = 0

        # moving the snowmen back and forth.
        # when they find a drop or a wall, they move in the other direction
        for snowman in snowmenObj:
            if snowman['direction'] == LEFT:
                if isGround(mapObj, snowman, snowman['velocity'], SNOWMAN_HEIGHT) and not isWall(mapObj, snowman, snowman['velocity'], SNOWMAN_HEIGHT):
                    snowman['x'] += snowman['velocity']
                else:
                    snowman['velocity'] = -snowman['velocity']
            elif snowman['direction'] == RIGHT:
                if isGround(mapObj, snowman, SNOWMAN_WIDTH + snowman['velocity'], SNOWMAN_HEIGHT) and not isWall(mapObj, snowman, SNOWMAN_WIDTH + snowman['velocity'], SNOWMAN_HEIGHT):
                    snowman['x'] += snowman['velocity']
                else:
                    snowman['velocity'] = -snowman['velocity']

        # simulate falling when there is no floor under the player
        if Falling:
            # prevent the player from jumping past the ground by reducing the distance that he jumps for the last iteration.
            if isGround(mapObj, playerObj, 0, gravity_acc + AMIGO_SIZE):
                gravity_acc = (floor * TILEHEIGHT - (playerObj['y'] + AMIGO_SIZE))
                playerObj['y'] += gravity_acc
                Falling = False
            else:
                playerObj['y'] += gravity_acc
                gravity_acc += GRAVITY
                Jumping = False  
     
        # executing the jump when Boolean swtch turned on
        if Jumping:
            # changing the player's sprite to the jumping sprite
            playerObj['run_position'] = 3
            # stopping the jump if the full form of the jump has been made
            if jumpmotion < 0:
                # prevent the player from jumping past the ground by reducing the distance that he jumps for the last iteration.
                if isGround(mapObj, playerObj, AMIGO_SIZE, -jumpmotion + AMIGO_SIZE):
                    jumpmotion = (floor * TILEHEIGHT - (playerObj['y'] + AMIGO_SIZE))
                    playerObj['y'] += jumpmotion
                    Jumping = False
                    jumpmotion = JUMPFORCE
                    playerObj['run_position'] = 0                
                else:
                    playerObj['y'] -= jumpmotion
                    jumpmotion -= GRAVITY                   
            else:
                # making the jump
                playerObj['y'] -= jumpmotion
                jumpmotion -= GRAVITY
 
        # executing left movements when the Boolean switch is turned on
        if moveLeft:
            # changing the sprites to face left
            playerObj['facing'] = LEFT
            playerObj['surfaces'] = L_AMIGOS

            # moving the sprite, while making sure that the player's sprite can't go further back than the camera.
            if playerObj['x'] > camerax - 5 and not isWall(mapObj, playerObj, -VELOCITY, AMIGO_SIZE):
                playerObj['x'] -= VELOCITY

            # running through the first 3 sprites in the dictionary when moving left and not jumping
            if not Jumping:
                playerObj['run_position'] = ((playerObj['run_position'] + 1) % (len(playerObj['surfaces']) -1))

        # executing right movements when the Boolean switch is turned on
        elif moveRight:
            # changing the sprites to face right
            playerObj['facing'] = RIGHT
            playerObj['surfaces'] = R_AMIGOS
            # moving the sprite rightwards
            if not isWall(mapObj, playerObj, AMIGO_SIZE + VELOCITY, AMIGO_SIZE):
                playerObj['x'] += VELOCITY
            # making sure that the camera follows the sprite as it moves to the right
            if playerCenterx > (camerax + HALF_WINWIDTH + CAMERASLACK):
                camerax += VELOCITY
            # running through the first 3 sprites in the dictionary when moving left and not jumping
            if not Jumping:
                playerObj['run_position'] = ((playerObj['run_position'] + 1) % (len(playerObj['surfaces']) - 1))

        # set to game over if the player falls down beyond the window
        if playerObj['y'] > WINHEIGHT:
            gameOverMode = True

        # checking for collisions between the snowmen and the player
        for snowman in snowmenObj:
            # this conditional is to accommodate for the fact that the 'rect' is created later in the game loop
            if 'rect' in snowman:
                # check for a collision while checking that the snowman is not already destroyed and the player is not in invulnerable mode
                if snowman['rect'].colliderect(playerObj['rect']) and not snowman['destroyed'] and not invulnerableMode:
                    # check for if the collision was from the player jumping on the snowman
                    if abs(snowman['rect'].top - playerObj['rect'].bottom) < COLLISION_TOLERANCE:
                        snowman['surface_index'] = 1 # change the snowman surface to the destroyed snowman
                        snowman['velocity'] = 0 # stop the snowman moving
                        # adjust the snowman to the appropriate coordinates and dimensions
                        snowman['height'] = SQUASHED_SNOWMAN_HEIGHT
                        snowman['width'] = SQUASHED_SNOWMAN_WIDTH
                        snowman['y'] += 20

                        snowman['destroyed'] = True # make sure the game knows this snowman is destroyed

                        # make the player do a little bounce
                        jumpmotion = 10
                        Jumping = True

                        SOUNDS['coin'].play() # make a noise to show the snowman was destroyed
                        snowmen_left -= 1 # reduce the amount of snowmen left
                    # conditional for if the player was hit by the snowman and is not in invulnerable mode
                    elif not invulnerableMode:
                        SOUNDS['hit'].play() # play the sound for being hit by the snowman
                        invulnerableMode = True # turn on invulnerable mode
                        invulnerableStartTime = time.time() # set the invulnerable mode start time
                        playerObj['health'] -= 1 # reduce the player's lives

                        # if the player's health is now 0, set to game over
                        if playerObj['health'] == 0:
                            gameOverMode = True

        # checking for collisions with the player and the finishline flag, and setting to win mode if there is one                   
        flagRect = pygame.Rect(flagObj['x'] - camerax, flagObj['y'] - cameray, FLAG_WIDTH, FLAG_HEIGHT)
        if 'rect' in playerObj:
            if flagRect.colliderect(playerObj['rect']):
                winMode = True
                SOUNDS['goal'].play()
    
        # if game over mode is on, the theme music will be turned off and the game will be moved to the game over screen
        if gameOverMode:
            pygame.mixer.music.stop()
            return 

        # blitting all images to the screen

        # blitting the background image to the screen
        backgroundRect = BACKGROUND_IMAGE.get_rect()
        backgroundRect.centery = HALF_WINHEIGHT
        backgroundRect.centerx = HALF_WINWIDTH
        DISPLAYSURF.blit(BACKGROUND_IMAGE, backgroundRect)

        # blitting the snow tiles to the screen
        for x in range(len(mapObj)):
            for y in range(len(mapObj[x])):
                spaceRect = pygame.Rect((x * TILEWIDTH - camerax, y * TILEHEIGHT - cameray, TILEWIDTH, TILEHEIGHT))
                if mapObj[x][y] in TILEMAPPING:
                    baseTile = TILEMAPPING[mapObj[x][y]]
                    # only blit the tiles that are near the game window
                    if (x * TILEWIDTH) > (camerax - WINWIDTH) and (x * TILEWIDTH) < (camerax + 2 * WINWIDTH):
                        DISPLAYSURF.blit(baseTile, spaceRect)

        # blitting the snowmen to the screen
        for snowman in snowmenObj:
            # only blit the snowmen that are near the game window
            if snowman['x'] > camerax - HALF_WINWIDTH and snowman['x'] < camerax + WINWIDTH:
                snowman['rect'] = pygame.Rect(snowman['x'] - camerax, snowman['y'] - cameray, snowman['width'], snowman['height'])
                DISPLAYSURF.blit(snowman['surfaces'][snowman['surface_index']], snowman['rect'])

        # blitting the flag
        flagSurface = flagObj['surfaces']
        DISPLAYSURF.blit(flagSurface, flagRect)

        # making an oscillating Boolean switch that will make the character flash if invulnerable mode is on.
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        # blitting the player sprite
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            # creating a rectangle for the sprite, with it's position relative to the camera to ensure it's always on the screen
            playerObj['rect'] = pygame.Rect(playerObj['x'] - camerax, playerObj['y'] - cameray, AMIGO_SIZE, AMIGO_SIZE)

            # blitting the sprite to the screen
            DISPLAYSURF.blit(playerObj['surfaces'][playerObj['run_position']], playerObj['rect'])
        
        # blitting the player's lives left
        for i in range(playerObj['health']):
            lifeRect = pygame.Rect(700 + i * 30, 10, 20, 20)
            DISPLAYSURF.blit(LIFE, lifeRect)
        
        # blitting the alive snowmen left as a number
        snowmen_leftSurf = BASICFONT.render(str(snowmen_left), 1, TEXTCOLOR)
        snowmen_leftRect = snowmen_leftSurf.get_rect()
        snowmen_leftRect.bottomleft = (700, 70)
        DISPLAYSURF.blit(snowmen_leftSurf, snowmen_leftRect)

        # blitting a little snowman next to the snowmen left number
        snowmen_icon = SNOWMEN[2]
        snowmen_iconRect = snowmen_icon.get_rect()
        snowmen_iconRect.bottomleft = (730, 68)
        DISPLAYSURF.blit(snowmen_icon, snowmen_iconRect)

        # show win screen if the player has won
        if winMode:
            pygame.mixer.music.stop()
            DISPLAYSURF.blit(winnerSurf, winnerRect)
            pygame.display.update()
            pygame.time.wait(6000)
            DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
            pygame.display.update()
            
            while True: # Main loop for the win screen.
                for event in pygame.event.get():
                    # check for quit
                    if event.type == QUIT:
                        terminate()
                    # check for any key down event
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            terminate()
                        return # user has pressed a key, so return.

        # updating the screen
        pygame.display.update()
        # controlling the update speed to ensure that changes don't happen to quickly
        FPSCLOCK.tick(FPS)

    

def terminate():
    # terminates the game when called.
    pygame.quit()
    sys.exit()


def readMapFile(filename):
    """
    retrieve information from the txt file for the map and organise it into a list of 
    columns containing information on the map tile layout.
    """
    assert os.path.exists(filename), 'Cannot find the level file: %s' % (filename)
    mapFile = open(filename, 'r')
    # Each level must end with a blank line
    content = mapFile.readlines() + ['\r\n']
    mapFile.close()

    mapTextLines = []
    mapObj = []
    snowmen = []
    flag = {}

    flag['surfaces'] = FLAG # add flag surface to the dictionary

    # characteristics for the player
    playerObj = {'surfaces': R_AMIGOS,
                 'facing': LEFT,    
                 'run_position': 0,
                 'x': HALF_WINWIDTH - AMIGO_SIZE / 2,
                 'y': FLOOR - AMIGO_SIZE,
                 'health': 3}


    for i in range(len(content)):
        line = content[i].rstrip('\r\n')

        if ';' in line:
            # Ignore the ; lines, they're comments in the level file.
            line = line[:line.find(';')]

        if line != '':
            # This line is part of the map.
            mapTextLines.append(line)

        elif line == '' and len(mapTextLines) > 0:
            # A blank line indicates the end of a level's map in the file.
            # Convert the text in mapTextLines into a level object.

            # Find the longest row in the map.
            maxWidth = -1
            for i in range(len(mapTextLines)):
                if len(mapTextLines[i]) > maxWidth:
                    maxWidth = len(mapTextLines[i])
            # Add spaces to the ends of the shorter rows. This
            # ensures the map will be rectangular.
            for i in range(len(mapTextLines)):
                mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i]))

            # Convert mapTextLines to a map object.
            for x in range(len(mapTextLines[0])):
                mapObj.append([])
            for y in range(len(mapTextLines)):
                for x in range(maxWidth):
                    mapObj[x].append(mapTextLines[y][x])

            
            for x in range(len(mapObj)):
                for y in range(len(mapObj[x])):
                    snowmenObj = {}
                    # add all snowmen and their characteristics as a dictionary, then all added into a list
                    if mapObj[x][y] == "S":
                        snowmenObj['x'] = x * TILEWIDTH
                        snowmenObj['y'] = y * TILEHEIGHT + TILEHEIGHT - SNOWMAN_HEIGHT
                        snowmenObj['height'] = SNOWMAN_HEIGHT
                        snowmenObj['width'] = SNOWMAN_WIDTH
                        snowmenObj['surface_index'] = 0
                        snowmenObj['surfaces'] = SNOWMEN
                        snowmenObj['velocity'] = getRandomVelocity()
                        snowmenObj['destroyed'] = False
                        snowmen.append(snowmenObj)
                        mapObj[x][y] = 0
                    # add the flag and its coordinates to the dictionary
                    if mapObj[x][y] == "F":
                        flag['x'] = x * TILEWIDTH
                        flag['y'] = y * TILEHEIGHT - FLAG_HEIGHT + TILEHEIGHT
                        

            # Loop through the spaces in the map and find the #
            # characters for the starting game state.
            gameObj = {'player': playerObj,
                       'snowmen': snowmen,
                       'flag': flag}
            levelObj = {'gamestate': gameObj,
                        'width': maxWidth,
                        'height': len(mapObj[0]),
                        'mapObj': mapObj}
    return levelObj



def isGround(mapObj, gameObj, x_offset=0, y_offset=0):
    """ Checks to see if there is ground under the player."""
    # finding the side and bottom of the sprite, and the grid coordinates of the floor for the sprite.
    gameObjBottom = gameObj['y'] + y_offset # bottom of the character
    gameObjSide = gameObj['x'] + x_offset   # side of the character
    floor_coord = findFloor(mapObj, gameObj, x_offset, y_offset)# grid coordinates of the floor
    mapLength = len(mapObj) * TILEWIDTH     # length of the map
    mapHeight = len(mapObj[0]) * TILEHEIGHT # height of the map

    # check if the player is outside of the map
    if gameObjSide < -5 or gameObj['y'] < 5 or gameObjSide > mapLength or gameObjBottom > mapHeight:
        return False
    # check if the player is on the floor.
    if floor_coord == None:
        return False
    floor = (floor_coord) * TILEHEIGHT
    if gameObjBottom >= floor:
        return True
    return False


def convertToGridCoords(x, y):
    """Converts pixels to tile grid"""
    grid_x = int(x / TILEWIDTH)
    grid_y = int(y / TILEHEIGHT)
    return grid_x, grid_y


def findFloor(mapObj, gameObj, x_offset=0, y_offset=0):
    """Finds the floor underneath the user"""
    gameObjSide = gameObj['x'] + x_offset - 5 # side of the object
    gameObjBottom = gameObj['y'] + y_offset
    mapLength = len(mapObj) * TILEWIDTH # width of the map
    mapHeight = len(mapObj[0] * TILEHEIGHT) # height of the map

    # checks to find if the object is outside of the map.
    if gameObj['x'] > mapLength or gameObjBottom > mapHeight:
        return None
    # distinguishing the player's behaviour on the map differently to enemies on the map, as they will recognise the floor at different points
    # i.e. the player should be able to run on edges on the cliff, while enemies should turn around when near a cliff.
    if 'run_position' in gameObj:
        # grid coordinates of the player
        x, y = convertToGridCoords(gameObj['x'], gameObj['y'])
        # finds the row in the map in the column that the object is on that is the floor.
        for row in range(len(mapObj[x])):
            if mapObj[x][row] == '#':
                # this checks to see if half of the object is on a step, as the game will get confused which step is considered the floor
                # in this case, we make the game pick the higher step if it is half on a step.
                if gameObjSide > len(mapObj[0:x + 1]) * TILEWIDTH and gameObjSide < len(mapObj) * TILEWIDTH:
                    for nextcolumnrow in range(len(mapObj[x + 1])):
                        if mapObj[x + 1][nextcolumnrow] == '#':
                            if nextcolumnrow < row:
                                return nextcolumnrow 
                return row
            # if there is no floor found in the column that the player is in, we check to see if the player is partially in the next column
            # if so, we change the column to the next one.
            elif row == len(mapObj[x]) - 1:
                if gameObjSide > len(mapObj[0:x + 1]) * TILEWIDTH:
                    for nextcolumnrow in range(len(mapObj[x + 1])):
                        if mapObj[x + 1][nextcolumnrow] == '#':
                            return nextcolumnrow               
        return None
    else:
        # grid coordinates of the enemy plus its x offsets
        x, y = convertToGridCoords(gameObj['x'] + x_offset, gameObj['y'])
        for row in range(len(mapObj[x])):
            if mapObj[x][row] == '#':        
                return row
        return None          


def findWall(mapObj, gameObj, x_offset=0, y_offset=0):
    """Finds the floor underneath the user"""
    gameObjSide = gameObj['x'] + x_offset # side of the object
    gameObjBottom = gameObj['y'] + y_offset # bottom of the object
    x, y = convertToGridCoords(gameObjSide, gameObjBottom) # x and y coordinates of object in terms of the map array
    mapLength = len(mapObj) * TILEWIDTH # width of the map
    mapHeight = len(mapObj[0] * TILEHEIGHT) # height of the map

    # checks to find if the player is outside of the map.
    if gameObj['x'] < 0 or gameObjSide > mapLength or gameObjBottom > mapHeight:
        return None
    # finds the row in the map in the column that the player is on that is the floor.
    for row in range(len(mapObj[x])):
        if mapObj[x][row] == '#':
            return row
        # if there is no floor found in the column that the player is in, we check to see if the player is partially in the next column
        # if so, we change the column to the next one.
        elif row == len(mapObj[x]) - 1:
            if gameObj['x'] + AMIGO_SIZE - 5 > len(mapObj[0:x + 1]) * TILEWIDTH:
                for nextcolumnrow in range(len(mapObj[x + 1])):
                    if mapObj[x + 1][nextcolumnrow] == '#':
                        return nextcolumnrow               
    return None


def isWall(mapObj, gameObj, x_offset=0, y_offset=0):
    """Checks if there is a wall in front of the object"""
    gameObjSide = gameObj['x'] + x_offset # side of the object
    gameObjBottom = gameObj['y'] + y_offset # bottom of the object
    wall_grid = findWall(mapObj, gameObj, x_offset, y_offset) # the y coordinate from the map array of year the floor is ahead of the object

    # checks to see if a floor was present in front of the object
    if wall_grid == None:
        return False
    floor_ahead = wall_grid * TILEHEIGHT # convert y-coordinate of the floor to pixels
    if floor_ahead < gameObjBottom:
        return True
    return False


def getRandomVelocity():
    """Provides a random velocity for each snowman"""
    speed = random.randint(SNOWMAN_MIN_VELOCITY, SNOWMAN_MAX_VELOCITY)
    if random.randint(0, 1) == 0:
        return speed
    else:
        return -speed    


def showStartScreen():
    """shows the start screen of the game"""
    # blit the start screen image to the screen
    titleRect = START_SCREEN.get_rect()
    titleRect.centery = HALF_WINHEIGHT
    titleRect.centerx = HALF_WINWIDTH
    DISPLAYSURF.blit(START_SCREEN, titleRect)

    # blit "Press any key to start! underneath the titlle of the game"
    press_key_text = "Press any key to start!"
    pressKeySurf = BASICFONT.render(press_key_text, 1, TEXTCOLOR)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.centerx = HALF_WINWIDTH
    pressKeyRect.centery = 3 * WINHEIGHT / 4 + 50
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()


def showGameOverScreen():
    # play game over sound
    SOUNDS['gameover'].play()

    # render a 'Game Over' text to show on the screen, generate a rectangle for the text and set position on the screen
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINWIDTH / 2, 10)
    overRect.midtop = (WINWIDTH / 2, gameRect.height + 10 + 25)

    # render "press any key to start!" text to go under the "game over" text, generate a rectangle for the text and set a position on the screen
    pressKeySurf = BASICFONT.render("Press any key to start!", True, TEXTCOLOR)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.centerx = HALF_WINWIDTH
    pressKeyRect.centery = 3 * WINHEIGHT / 4 + 50

    # blit the "Game Over" text to the screen
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    # update the screen to show the text, then wait for seconds for the sound to finish
    pygame.display.update()
    pygame.time.wait(4000)

    # blit the "press any key to start!" text
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    pygame.display.update()

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            # check for quit event
            if event.type == QUIT:
                terminate()
            # check for keydown event
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.
     


if __name__ == '__main__':
    main()