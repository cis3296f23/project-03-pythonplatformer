# Python-Platformer
Python Platformer is a 2D platformer game that provides a classical, Super-Mario Bros. experience. The theme around this game is that of Temple University and its mascot, Hooter the Owl.  After clicking through the title screen, the user will be able to control a character’s movements as the character advances through a level. Like other Platformer games, there will be various obstacles and enemies scattered across the level that the player must avoid. There will also be a leaderboard presented to users to showcase the fastest or best scores.

<img width="801" alt="Screenshot 2023-11-10 at 9 46 14 AM" src="https://github.com/cis3296f23/project-03-pythonplatformer/assets/90412421/8e617e21-af45-4c4e-85c5-e7167fa2d6c1">
<img width="997" alt="Screenshot 2023-11-10 at 9 46 36 AM" src="https://github.com/cis3296f23/project-03-pythonplatformer/assets/90412421/fd3bebbb-aff8-4fd9-bfa6-0c1aaef8179f">

# UML Diagram
![Python Platformer drawio (2)](https://github.com/cis3296f23/project-03-pythonplatformer/assets/111991851/f95d3487-721a-4222-b719-976273abe95f)


We have a Player class, a Level class, and Enemy Class, and an Object class which contains 3 objects: Fire, Block, and Spike. The Player class includes methods for moving, jumping, taking damage, determining if head has hit something, determining if the player has landed, and drawing the player sprite, and animating the player sprite. It includes fields which keep track of actions the player performs. The Level class has methods for initializing the level, generating platforms, and generating spikes. It contains fields for the platforms. The Object class has methods for initializing and drawing objects. The Object class has fields for keeping track of dimensions (width and height), name of object, image to use for object, and how to draw object. Block is of type object and has a method to initialize the object and fields to mask the object. Fire is of type object and contains methods to initialize, animate, and turn the object on or off. Fire contains fields which keep track of dimensions and useful variables for animation. Spike is of type object and contains methods to initialize the object and to load the image for the spike, and fields to mask the object. The Enemy class has not yet been implemented, but has been added to the diagram for an idea of what will need to be implemented. It contains methods for making enemies move, jump, and updating/animating the sprites. It contains fields for sprite and to mask the object.

# Sequence Diagrams
![Python Platformer (5)](https://github.com/cis3296f23/project-03-pythonplatformer/assets/111991851/b81b9702-244c-44d7-b99c-578b6ff88bba)


This diagram displays the interaction between most of the objects in the game. When the game is running, the Game Manager gets the background for the level, then in main generates platforms and spikes for the level. Main then takes care of loading sprites for the player, drawing the player, and handling player movement. If the player collides with an object, it will return info about the object collided with. If it is fire, spikes, or an enemy, the player will be "hit".  If the player runs out of lives, the player will die and it will return to main that the game should quit. If the "P" key is pressed, the pause menu will show up and the game will be paused. The pause menu allows the player to exit the game by pressing quit, which will set run to false calling the quit method. When the game is quit, the window will close.

<img width="751" alt="Screenshot 2023-12-01 at 11 39 54 AM" src="https://github.com/cis3296f23/project-03-pythonplatformer/assets/90412421/caeb8c71-c56e-48c9-9432-9adde358dbc8">



# How to run
- Download the latest binary from the Release section on the right on GitHub.  
- On the command line uncompress using
```
tar -xzf  
```
- On the command line run with
```
./main
```
- You will see the Platformer window on your terminal and you can begin playing.

# How to contribute
Follow this project board to know the latest status of the project: [(https://github.com/orgs/cis3296f23/projects/121/views/1)]

### How to build
- Use this github repository: https://github.com/cis3296f23/project-03-pythonplatformer
- Fork a copy of the code or download the zip file.  
- Use PyCharm or VSCode to open 
- Check for main.py file as well as other images folders.
- Open main.py and run the code from the IDE to test the game.
- Make any necessary changes/improvements
- Add, commit, and push any modifications.
