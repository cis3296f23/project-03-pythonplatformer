# Python-Platformer
Python Platformer is a 2D platformer game that provides a classical, Super-Mario Bros. experience. The theme around this game is that of Temple University and its mascot, Hooter the Owl.  After clicking through the title screen, the user will be able to control a character’s movements as the character advances through a level. Like other Platformer games, there will be various obstacles and enemies scattered across the level that the player must avoid. There will also be a leaderboard presented to users to showcase the fastest or best scores.

<img width="801" alt="Screenshot 2023-11-10 at 9 46 14 AM" src="https://github.com/cis3296f23/project-03-pythonplatformer/assets/90412421/8e617e21-af45-4c4e-85c5-e7167fa2d6c1">
<img width="997" alt="Screenshot 2023-11-10 at 9 46 36 AM" src="https://github.com/cis3296f23/project-03-pythonplatformer/assets/90412421/fd3bebbb-aff8-4fd9-bfa6-0c1aaef8179f">

# UML Diagram
![image](https://github.com/cis3296f23/project-03-pythonplatformer/assets/111991851/a04a7858-54fe-41ad-ae9c-7931e1cd405e)

So far we have a Player Class, and an Object class which contains 2 objects: Fire and Block. The Player class includes methods for moving, jumping, taking damage, determining if head has hit something, determining if the player has landed, and drawing the player sprite, and animating the player sprite. It includes fields which keep track of actions the player performs. The Object class has methods for initializing and drawing objects. The Object class has fields for keeping track of dimensions (width and height), name of object, image to use for object, and how to draw object. Block is of type object and has a method to initialize the object and fields to mask the object. Fire is of type object and contains methods to initialize, animate, and turn the object on or off. Fire contains fields which keep track of dimensions and useful variables for animation.






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
