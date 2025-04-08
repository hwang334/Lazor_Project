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

# Logic Behind the Code 
### 1. Initial Laser Path (No Block State)

Start from each laser's initial position and simulate laser movement in half-step units
until it reaches or crosses the board boundary.

During this process, track the cells the laser passes through by checking if
the two consecutive laser points share edge points with a grid cell.

These "laser-passed" cells form the initial candidate cell set.

### 2. Place Blocks in Candidate Cells and Update Path

Select a cell from the candidate set and place one of the available block types (A/B/C) into it.

Once a block is placed, the laser path may change:
- When a laser moves from (x, y) to (nx, ny), check for collisions with any placed block.
- If a collision occurs, modify the laser according to the block type:
  - A: Reflects the laser.
  - B: Blocks the laser.
  - C: Splits the laser—one beam reflects, one continues in the same direction.

The collision point becomes the new starting point for the laser (or multiple starting points for C),
and the simulation continues as if in a "no block" state.
Record all new cells the laser passes through; these form the new candidate set.

### 3. Recursion and Backtracking

For each new candidate cell, recursively attempt to place the remaining blocks.
Update laser paths and generate further candidate cells.

If at any point all target points are hit by lasers, a solution has been found.

If all placement combinations fail to hit all targets, backtrack:
Remove the last placed block and try another block or another location.

### 4. Edge Point Matching

To detect grid traversal and collisions:
- Maintain an edge point library for each grid cell: typically 4 midpoints of each edge.
- Similarly, blocks have their own edge point definitions.

During simulation:
- To detect cell traversal: if both points p1 and p2 in the laser path lie on a cell's edges, mark that cell as traversed.
- To detect collisions: if p1 and p2 lie on a block's edge, a collision occurs.
  Determine which edge was hit based on p1 → p2 direction, then apply reflection/block/split accordingly.

### 5. Post-Collision: Resume "No Block" Simulation

After hitting a block, call its specific handler:
- A: Reflect the beam, invert the appropriate directional component.
- B: Terminate the beam.
- C: Create two new beams—one reflected, one continuing.

For reflected beams: restart simulation from the collision point.
For transmitted beams (C): offset the origin slightly (by half-step) to prevent re-collision at the same point,
then continue "no block" simulation.

Each new segment may yield new candidate cells, which must be tracked and updated.

### 6. Target Hit Detection

If a laser at any point exactly matches the position of a target, mark that target as hit.

Once all targets are hit, a solution has been achieved, and the recursion ends.

Continue the loop: place block → simulate → gather new candidates → place again,
until all targets are covered or all paths fail and require backtracking.


# Overview of the three code files

### 1. **LazorBoard.py**

**Purpose**:  
This file contains the `LazorBoard` class, which handles the board layout, the placement of blocks, and simulates laser movements based on the configuration read from `.bff` files. It also checks whether lasers hit the targets and handles the grid setup for the game.

**Classes**:
- **LazorBoard**: Manages the board layout and contains methods for placing blocks, checking valid positions, and simulating laser movements.

**Functions**:
- **`__init__(self, grid, blocks, lasers, targets)`**: Initializes the LazorBoard with a grid, available blocks, lasers, and targets.
- **`from_file(cls, filename)`**: Class method that reads a `.bff` file, parses it, and initializes a LazorBoard instance.
- **`__str__(self)`**: Returns a string representation of the board layout, blocks, lasers, and targets.
- **`get_empty_slots(self)`**: Returns a list of coordinates where blocks can be placed (positions marked with 'o' in the grid).
- **`out_of_bounds(self, pos)`**: Checks if a position is outside the grid.
- **`is_valid_position(self, x, y)`**: Checks if a given position is valid for placing a block.
- **`place_block(self, x, y, block_type)`**: Places a block of the specified type on the board at the given position.
- **`get_block_at(self, x, y)`**: Returns the block type at a given position or 'o' if there is no block.
- **`simulate_lasers(self)`**: Simulates all lasers and checks if they hit the targets.

---

### 2. **Classes.py**

**Purpose**:  
This file defines the core blocks (`A_Block`, `B_Block`, `C_Block`) and the `Laser` class. The blocks interact with lasers in different ways: reflecting, refracting, or blocking them. The laser class represents the lasers' position and movement.

**Classes**:
- **Laser**: Represents a laser with its position and direction on the board.
- **A_Block**: Reflects the laser in the opposite direction.
- **B_Block**: Refracts the laser by swapping its x and y directions.
- **C_Block**: Blocks the laser and stops its movement.

**Functions**:
- **`Laser(x, y, vx, vy)`**: Initializes the laser with its position `(x, y)` and velocity `(vx, vy)`.
- **`A_Block(laser)`**: Reflects the laser by changing its velocity direction.
- **`B_Block(laser)`**: Refracts the laser by swapping its velocity components (`vx`, `vy`).
- **`C_Block(laser)`**: Blocks the laser, stopping its movement.

---

### 3. **Solver.py**

**Purpose**:  
This file contains the logic to solve the Lazor puzzle by placing blocks on the board. It tries different permutations of the available blocks and simulates laser movements to check if all targets are hit.

**Functions**:
- **`simulate_lasers(board)`**: Simulates the lasers on the given board and returns the set of hit target points.
- **`solve_lazor(board)`**: Attempts to solve the puzzle by trying all possible block placements and checking if all targets are hit.
- **`save_solution_to_txt(solution, filename)`**: Saves the solved board configuration to a `.txt` file.

**Helper Functions**:
- **`backtrack(board, empty_slots, block_list, idx)`**: A recursive helper function used by `solve_lazor` to place blocks on the board and backtrack if a solution is not found.
- **`get_empty_slots(board)`**: Returns the list of empty slots available for placing blocks on the board.

---

### **How to Run the Code**

1. **Prepare the `.bff` file**:  
   The `.bff` file should define the grid, blocks, lasers, and targets. It should be formatted as follows:
   - `GRID START` and `GRID STOP` to define the grid.
   - `B` followed by a number to specify how many blocks of type `B` are available.
   - `L` to define the lasers' positions and directions.
   - `P` to specify the target positions.

2. **Run the main file**:  
   In the terminal, run `main.py` to start the program. It will ask for the board name (e.g., `dark_1`), read the corresponding `.bff` file, and attempt to solve the puzzle. If a solution is found, it will output the result to a `.txt` file.

   Example:
   ```bash
   python main.py
   ```

   You will be prompted to enter the board name (e.g., `dark_1`).

3. **Solution File**:  
   If the puzzle is solved successfully, the program will output the solved board configuration to a `.txt` file named `<board_name>_solution.txt`.


# example:

