# 2025 Software Lazor Project--Group 15

This is a team-based coding project focused on solving Lazor, a puzzle game where laser beams must hit specific targets by placing different types of blocks on a grid. Our goal is to develop a Python program that can automatically find valid solutions for any given Lazor level.

The program will read the puzzle setup from a .bff file, simulate how lasers move, including reflection, absorption, and refraction and search for the correct block placements to solve the puzzle efficiently. We will use fundamental programming concepts like data structures, class, loops, and functions, along with search algorithms to explore possible solutions. 

# Group members

Huakun Wang: hwang334@jh.edu  
Xiaoyu Wang: xwang442@jh.edu 
Zhixin (Mac) Zhang: zzhan336@jh.edu

# How is the solution generated?  

The game starts with an empty board, which contains a grid where lasers, blocks, and targets are placed and interact. The grid is represented as a matrix with different symbols:  
- `x` = No block allowed  
- `o` = Blocks allowed  
- `A` = Fixed reflect block  
- `B` = Fixed opaque block  
- `C` = Fixed refract block  

There are also three types of functional blocks that can be placed freely:  
- A_Block (Reflect Block): Bounces the laser at a 90-degree angle.  
- B_Block (Opaque Block): Blocks the laser completely.  
- C_Block (Refract Block): Splits the laser into two paths—one passing through and the other reflecting.  

The program begins by loading the level settings from a `.bff` file. It then constructs the grid and identifies where blocks can be placed. The `component.py` file defines the laser behavior and block types.  

To solve the puzzle, the program generates all possible block arrangements and simulates laser movement for each case. It verifies if the lasers successfully hit all targets.  

To run the solver, execute `version_final.py` and enter the board file name. If a solution is found, it will be saved as a `.txt` file, including the final board layout, placed blocks, and laser paths. If no solution exists, the screen will display "No answer".  

If the given board file is missing, the program will immediately print an error message without attempting to solve the puzzle.

# example:

