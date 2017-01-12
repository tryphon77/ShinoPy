# ShinoPy
This is a port of the 1987 Sega Arcade Game Shinobi.
It uses a small python lib called GenePy, based upon Pygame, whose purpose is to mimic some aspects of the Megadrive hardware, in order to make a port to the Megadrive easier. The goal of this project is to design a proper game engne, before working on the Megadrive version (which will use SGDK).

For this reason, the engine is volontarily not optimized.

The project is in very early alpha, as the GenePy library.

## Structure

res : ressources (tiles, sprites, ...)

tools : python scripts for generating ressources from ripped files (not included). They rely on MDTools, a set of python scripts for generating ressources in MD format (not included, but will be on github sooner or later)
	map_tools.py : generate patterns, tilesets and tilemaps
	sprite_tools.py : generate patterns, frame descriptions, animations descriptions, ...

. : main directory
run_stage.py : main loop when ingame, in a stage
tsprite.py : definitions and handling of TSprites (graphical animated object, that can be made of several hardware sprites). The T is for avoiding confusion with the Sprite struct in SGDK
tilemap.py
