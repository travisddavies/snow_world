# Snow World - The Game
This program was created by Travis Davies. 
<br/>
Video URL: https://youtu.be/Ll6rVcqolbY
<br/><br/>
## About
Snow world is a platformer video game created with the Pygame library, inspired by classic games such as Super Mario. The game is set in the Snowy Mountains, Australia. The player has to make it to the end of the map without being killed by the snowmen or falling off a cliff.
<br/><br/>
## How to Play
To play, you must progress further right through the map until you reach the Australian Flag. The obstacle of the game are the snowmen and the cliffs. You must jump from one platform to another without falling off the cliff, and you must not get hit by the snowmen more than three times. You can either kill the snowmen by jumping on them, or you can dodge them.
<br/><br/>
## Controls
To control the game, you simple need to use the 'a' key or the left key to move left, the 'd' key or the right key to move right and the space bar to jump. 
<br/><br/>
## Files Included
Files included in this program are the main game file, called 'project.py', the map file, called 'map.txt', and a folder of images, sounds and theme music. The images include the background image, the start screen image, the sprites for the player, the sprites for the snowmen and the Australian flag. The sounds include jumping sounds, destroying snowmen, getting hit by snowmen, game over and game won. The song included in the game is used as the theme song of the game, which is called 'Firecracker', by the legendary band Yellow Magic Orchestra.
<br/><br/>
## Details of the Game
### The Player:
The player consists of a set dictionary, where his coordinates, direction facing and number of lives are stored. Inside this dictionary is another dictionary for the surfaces (i.e. the images that are displayed on the screen to represent the player) used, as well as an index which will change to a new surface when prompted. 
<br/><br/>
When moving the player left or right, the x-coordinate of the player in the dictionary will change by a certain velocity per frame. As the sprite moves left or right, the index in the dictionary will keep looping through the surfaces used to represent different frames of running. 
<br/><br/>
Another important feature of the game is the camera that follows the player. As the player progresses further right, the window of the game follows the player, like a camera filming a movie, unvealing more of the map. This is done by recording a camera coordinate that increments at the same right that the player moves to the right. If the player moves to the left, the camera will not move left and will prevent the player from moving past the left-hand side of the window.
<br/><br/>
When the player is jumping, the y-coordinate of the player in the dictionary will change by a certain acceleration that mimicks a real jump. As the sprite jumps, a sound effect is played to mimick video game jumping. As the sprite is jumping, the surface is frozen to a single surface that represents jumping. When the player jumps on snowmen, he will also make a small bounce, along with a sound being played that sounds like a point was scored.
<br/><br/>
When the player falls off a platform, the y-coordinate of the player in its dictionary will change by a certain acceleration that mimicks gravity. If he lands onto lower ground, he will land on the platform to continue playing, if he falls to a section with now lower ground, he will fall past the window and will trigger a 'Game Over' screen.
<br/><br/>
When the player collides with a snowman that is not between the top of the snowman and the bottom of the player, one life will be taken off from the player's dictionary. The player will then enter 'invulnerable mode' for 2 seconds, where the surface will flash and no collisions with snowmen will be registered in the game.
<br/><br/>
The lives of the player can be found in the top-right-hand side of the screen, where miniature versions of the player's sprite can be found, each sprite represents a life that the player has remaining. The are three sprites in total, (i.e. three lives) dsiplayed on the screen. If all sprites are now longer displaying, it will trigger the 'Game Over' screen.
<br/><br/>
### The Snowmen:
The snowmen are a series of sprites scattered across the map, that oscillate back and forth on a certain platform. The snowmen detect when there is a wall in front of them, or if there is a lower platform or cliff in front of them and move in the opposite direction. 
<br/><br/>
These snowmen are essentially a list of dictionaries containing characteristics of each snowman, such as their position on the map, their dimensions, their velocity and a Boolean value for if they have been recorded as 'destroyed' or not. The dictionary also contains another dictionary which contains the surfaces used for the snowmen, along with an index to change the surface shown when prompted.
<br/><br/>
When a collision occurs between the top of a snowman and the bottom of the player, the snowman's surface will change to represent a snowman that has been destroyed, it will become stationary, its 'destroyed' Boolean will be turned to 'True' and its dimensions and position will be changed to display it properly on the screen.
<br/><br/>
A count of all the snowmen present on the map are displayed on the top-right-hand side of the screen, underneath the lives of the player. Each time a snowman is destroyed, the snowman count is reduced.
<br/><br/>
To improve the speed of the game, the snowmen are only displayed when the program indicates that the player is within two window-widths of the snowmen.  
<br/><br/>
### The Map:
The map of the game is provided in a file called 'map.txt'. This map contains a series of 0's, #'s, S's and an F, which all represent different things and their location on the map.
Each symbol is represented as follows:
- '#' = snow tile, which builds the platform
- S = snowman, the sprites scattered across the map.
- F = flag, the Australian flag at the end that ends the game
- 0 = open space

<br/>
In the game, the main game file reads this map file and organises it into a list of columns, each column representing a column of the map. This is used to gather information on the snowmen in the game, the location of the finishline flag, the terrain of the map, etc. 
<br/><br/>
For loops through the map of the game are used to find where the snowmen and player are in relation to the map and allows the game to act out functions such as actions for when sprites hit walls, when the player falls off a cliff, or even if the player of hanging on an edge.
<br/><br/>
The final flag is displayed at the end of the map. When a collision between the player and the flag occurs, the 'Winner' screen is triggered.
<br/><br/>
To improve the speed of the game, the map tiles are only displayed when certain tiles are within two window-widths of the player.