# ===== FILE: Classes.py =====

# Classes.py

class Board:
    '''
    Represents the game board, defining the grid, laser positions, and valid block placements.

    grid: *list[list[str]]*
        The board layout with markers for allowed and disallowed block placements.
    lasers: *list[tuple[int, int, int, int]]*
        List of laser positions and directions, represented as (x, y, vx, vy).
    targets: *list[tuple[int, int]]*
        Coordinates of target points that lasers must intersect.
    blocks: *dict[str, int]*
        Dictionary storing available block counts {'A': int, 'B': int, 'C': int}.
    '''
    def __init__(self, grid, lasers, targets, blocks):
        self.grid = grid
        self.lasers = lasers
        self.targets = targets
        self.blocks = blocks

    def is_valid_position(self, r, c):
        R = len(self.grid)
        C = len(self.grid[0]) if R > 0 else 0
        return 0 <= r < R and 0 <= c < C and self.grid[r][c] == 'o'

    def place_block(self, r, c, block_type):
        """Place a block of type block_type (A/B/C) on the board at (r, c). If placement is possible, update and return True; otherwise, return False."""
        if self.is_valid_position(r, c) and self.blocks[block_type] > 0:
            self.grid[r][c] = block_type
            self.blocks[block_type] -= 1
            return True
        return False

class Laser:
  
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.is_block = False  # Set to True if the laser is blocked

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def get_position(self):
        return (self.x, self.y)

class A_Block:
  
    def __init__(self, position):
        self.position = position

    def reflect(self, laser, edge_type):
        if edge_type == 'vertical':
            laser.vx = -laser.vx
        elif edge_type == 'horizontal':
            laser.vy = -laser.vy
        return laser

    def __call__(self, laser, edge_type):
        return self.reflect(laser, edge_type)

class B_Block:
   
    def __init__(self, position):
        self.position = position

    def __call__(self, laser):
        laser.is_block = True
        return laser

class C_Block:
   
    def __init__(self, position):
        self.position = position

    def __call__(self, laser, edge_type):
        from copy import deepcopy
        new_laser = deepcopy(laser)
        reflected_laser = A_Block(self.position)(new_laser, edge_type)
        return reflected_laser, laser


# ===== FILE: LazorBoard.py =====

# LazorBoard.py

class LazorBoard:
    '''
    Parses a .bff file to initialize the Lazor board setup.

    Attributes
    ----------
    grid : *list[list[str]]*
        The board layout with 'o' for valid positions and 'x' for invalid.
    blocks : *dict[str, int]*
        A dictionary with keys 'A', 'B', and 'C' representing block types and their available counts.
    lasers : *list[tuple[int, int, int, int]]*
        List of lasers defined as (x, y, vx, vy).
    targets : *list[tuple[int, int]]*
        List of target coordinates that need to be hit.
    ''' 
    def __init__(self, grid, blocks, lasers, targets):
        self.grid = grid
        self.blocks = blocks
        self.lasers = lasers
        self.targets = targets

    @classmethod
    def from_file(cls, filename):
        '''
        Reads a .bff file and creates a LazorBoard instance.

        *filename: str*
            Path to the .bff file.

        *returns: LazorBoard*
            A LazorBoard instance with parsed data.
        '''
        grid = []
        blocks = {'A': 0, 'B': 0, 'C': 0}
        lasers = []
        targets = []
        reading_grid = False

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line == 'GRID START':
                    reading_grid = True
                    continue
                elif line == 'GRID STOP':
                    reading_grid = False
                    continue

                if reading_grid:
                    row = line.split()
                    grid.append(row)
                elif line[0] in {'A', 'B', 'C'}:
                    parts = line.split()
                    block_type = parts[0]
                    count = int(parts[1])
                    blocks[block_type] = count
                elif line.startswith('L'):
                    parts = line.split()
                    x, y, vx, vy = map(int, parts[1:])
                    lasers.append((x, y, vx, vy))
                elif line.startswith('P'):
                    parts = line.split()
                    x, y = map(int, parts[1:])
                    targets.append((x, y))

        return cls(grid, blocks, lasers, targets)

    def __str__(self):
        '''
        Returns a nicely formatted string representation of the Lazor board.
        '''
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows>0 else 0
        
        grid_str = "\n".join([" ".join(row) for row in self.grid])
        block_str = ", ".join([f"{k}: {v}" for k,v in self.blocks.items()])
        laser_str = "\n".join([f"  - ({x},{y}) dir=({vx},{vy})" for (x,y,vx,vy) in self.lasers])
        target_str = "\n".join([f"  - ({x},{y})" for (x,y) in self.targets])
        return (f"=== Lazor Board ===\n"
                f"Grid size: {rows} x {cols}\n"
                f"{grid_str}\n\n"
                f"Blocks: {block_str}\n\n"
                f"Lasers:\n{laser_str}\n\n"
                f"Targets:\n{target_str}\n")


# ===== FILE: LazorVisualizer.py =====

# LazorVisualizer.py
import matplotlib.pyplot as plt

def visualize_lazor_solution(board, laser_paths, output_filename="lazor_solution.png"):

    rows = len(board.grid)
    cols = len(board.grid[0]) if rows > 0 else 0

    fig, ax = plt.subplots(figsize=(cols * 0.8, rows * 0.8))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Draw grid lines
    for x in range(cols + 1):
        ax.axvline(x, color='black', linewidth=0.5)
    for y in range(rows + 1):
        ax.axhline(y, color='black', linewidth=0.5)

    color_map = {
        'x': 'lightgrey',
        'o': 'white',
        'A': 'limegreen',
        'B': 'tomato',
        'C': 'royalblue'
    }

    # Draw each cell of the board
    for r in range(rows):
        for c in range(cols):
            cell = board.grid[r][c]
            facecolor = color_map.get(cell, 'white')
            rect = plt.Rectangle((c, r), 1, 1, facecolor=facecolor, edgecolor='none')
            ax.add_patch(rect)

    # Draw target points (convert half-grid coordinates to plotting coordinates)
    for (tx, ty) in board.targets:
        # Multiply half-grid coordinates by 0.5 to convert to plotting coordinates
        x = tx * 0.5
        y = ty * 0.5
        ax.plot(x, y, marker='*', markersize=15,
                color='gold', markeredgecolor='black', markeredgewidth=1)

    # Draw laser trajectories
    laser_colors = ['red', 'cyan', 'orange', 'magenta', 'blue', 'green']
    for i, path in enumerate(laser_paths):
        xs = [p[0] * 0.5 for p in path]
        ys = [p[1] * 0.5 for p in path]
        color = laser_colors[i % len(laser_colors)]
        ax.plot(xs, ys, color=color, linewidth=2, marker='o', markersize=3)

    ax.set_title("Lazor Puzzle Solution")
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"Visualization saved to: {output_filename}")


# ===== FILE: Solver.py =====

# Solver.py
import copy

def get_cell_edge_points(r, c):
    """
    Return the 4 midpoints of the edges of the cell (r, c) in half-grid coordinates.
    Used in simulate_single_laser() to determine if the laser passes through this cell.
    """
    return {
        (2*c+1, 2*r),     # Top edge midpoint (odd, even)
        (2*c+2, 2*r+1),   # Right edge midpoint (even, odd)
        (2*c+1, 2*r+2),   # Bottom edge midpoint (odd, even)
        (2*c,   2*r+1)    # Left edge midpoint (even, odd)
    }

class Solver:
    def __init__(self, board, debug=False):
        """
        :param board: Board object containing grid/blocks/lasers/targets
        :param debug: If True, detailed debug information will be printed to the console
        """
        # Save initial state
        self.original_grid = copy.deepcopy(board.grid)
        self.original_blocks = copy.deepcopy(board.blocks)
        self.original_targets = copy.deepcopy(board.targets)

        self.board = board       # Current board object
        self.debug = debug       # Debug flag
        self.placed_blocks = {}  # Placed blocks, mapping (r, c) -> 'A','B','C'
        self.final_paths = []    # Final laser trajectory paths

    def debug_print(self, *args):
        """Prints only when debug is True."""
        if self.debug:
            print(*args)

    def solve(self):
        """
        External entry point: Executes the solving process.
          1. Reset the board to its initial state
          2. Simulate lasers in a block-free state to obtain initial candidate cells
          3. Backtrack to place blocks; return True if all targets are hit, otherwise False
        """
        # Reset
        self.board.grid = copy.deepcopy(self.original_grid)
        self.board.blocks = copy.deepcopy(self.original_blocks)
        self.board.targets = copy.deepcopy(self.original_targets)
        self.placed_blocks.clear()
        self.final_paths.clear()

        # (1) Collect initial candidate cells in block-free state
        initial_candidates = self.simulate_no_blocks_initial()
        self.debug_print("[solve] Initial candidate cells =", initial_candidates)

        # (2) Backtracking
        success = self.backtrack(initial_candidates)
        if success:
            self.debug_print("[solve] Solution found!")
        else:
            self.debug_print("[solve] No solution.")
        return success

    def simulate_no_blocks_initial(self):
        """
        In a block-free state, for each laser, move in half steps, record the cells it passes through,
        and return the set of candidate cells.
        """
        candidate_cells = set()

        for (lx, ly, vx, vy) in self.board.lasers:
            path = []
            laser = Laser(lx, ly, vx, vy)

            steps = 0
            while steps < 2000:
                path.append((laser.x, laser.y))
                # Move a half step
                nx = laser.x + laser.vx
                ny = laser.y + laser.vy
                # Exit if out of bounds
                if nx < 0 or ny < 0 or nx > 2*len(self.board.grid[0]) or ny > 2*len(self.board.grid):
                    path.append((nx, ny))
                    break
                laser.x, laser.y = nx, ny
                steps += 1

            # Analyze consecutive points in the path; if (p1, p2) both fall on the midpoints of opposite edges of an 'o' cell, add that cell to candidates
            for i in range(len(path)-1):
                p1, p2 = path[i], path[i+1]
                for r in range(len(self.board.grid)):
                    for c in range(len(self.board.grid[0])):
                        if self.board.grid[r][c] == 'o':
                            edges = get_cell_edge_points(r, c)
                            if p1 in edges and p2 in edges:
                                candidate_cells.add((r,c))

        return candidate_cells

    def backtrack(self, candidates):
        """
        Main backtracking function:
          1) First use simulate_with_blocks() to check if all targets are hit
          2) If not all targets are hit, then try placing A/B/C blocks in new_candidates
          3) Return True if successful, otherwise backtrack
        """
        # Simulate lasers with the current placed blocks
        solved, new_candidates = self.simulate_with_blocks()
        if solved:
            self.debug_print("[backtrack] All targets hit, returning success")
            return True

        if not new_candidates:
            self.debug_print("[backtrack] No new candidate cells available, cannot place additional blocks, backtracking")
            return False

        # Try placing blocks in new_candidates
        for (r, c) in new_candidates:
            # If the cell is not 'o', it means a block is already placed
            if self.board.grid[r][c] != 'o':
                continue

            for block_type in ['A','B','C']:
                # If there are no remaining blocks of this type, skip
                if self.board.blocks.get(block_type, 0) < 1:
                    continue

                self.debug_print(f"[backtrack] Placing {block_type} block at ({r},{c})")
                self.board.grid[r][c] = block_type
                self.placed_blocks[(r,c)] = block_type
                self.board.blocks[block_type] -= 1

                if self.backtrack(new_candidates):
                    return True

                # Backtracking: remove the block from (r, c)
                self.debug_print(f"[backtrack] Backtracking: Removing {block_type} block from ({r},{c})")
                self.board.grid[r][c] = 'o'
                del self.placed_blocks[(r,c)]
                self.board.blocks[block_type] += 1

        return False

    def simulate_with_blocks(self):
        """
        Simulate all lasers with the current placed blocks:
          - For each laser, move in half steps, detect collisions, and if a collision occurs, process it (A reflection / B blocking / C splitting)
          - After each collision, immediately move the laser a half step away from the collision point to avoid infinite collisions
          - For C blocks, if splitting occurs, generate new lasers to simulate as well
        Returns: (whether all targets are hit, new_candidates)
        """
        remaining_targets = set(self.board.targets)
        all_paths = []
        new_candidates = set()

        # Collect all lasers to simulate (including any new ones generated by C block splitting)
        lasers_to_sim = [(lx, ly, vx, vy) for (lx, ly, vx, vy) in self.board.lasers]
        idx = 0

        while idx < len(lasers_to_sim):
            (lx, ly, vx, vy) = lasers_to_sim[idx]
            idx += 1

            if self.debug:
                print(f"[simulate_with_blocks] Laser #{idx} starting at ({lx},{ly}), direction=({vx},{vy})")

            laser_path, new_cand_part, new_lasers, remaining_targets = \
                self.simulate_single_laser(lx, ly, vx, vy, remaining_targets)

            all_paths.append(laser_path)
            new_candidates |= new_cand_part
            # If a C block produces a new beam, add it to the queue
            for nl in new_lasers:
                lasers_to_sim.append(nl)

        self.final_paths = all_paths
        solved = (len(remaining_targets) == 0)
        return solved, new_candidates

    def simulate_single_laser(self, lx, ly, vx, vy, remaining_targets):
        """
        Simulate a single laser with the current placed blocks:
          - Move in half steps
          - If it collides with an A/B/C block, perform the appropriate operation; after collision, immediately move the laser a half step away from the collision point to avoid infinite collisions
          - A C block will generate a new beam, which should be returned as new_lasers
        Also records the points the laser passes through for visualization; any 'o' cells passed are added to new_candidates.
        If a target is hit, remove it from remaining_targets.
        Returns: (laser_path, new_candidates, new_lasers, remaining_targets)
        """
        laser_path = []
        new_candidates = set()
        generated_lasers = []

        laser = Laser(lx, ly, vx, vy)
        steps = 0
        max_steps = 3000

        # Record the count of repeated collisions for the same collision to avoid infinite loops
        collision_count = {}

        while steps < max_steps and not laser.is_block:
            curr_pos = (laser.x, laser.y)
            laser_path.append(curr_pos)

            # If a target point is hit, remove it
            if curr_pos in remaining_targets:
                remaining_targets.remove(curr_pos)

            nx = laser.x + laser.vx
            ny = laser.y + laser.vy

            # Check for out-of-bounds
            if nx < 0 or ny < 0 or nx > 2*len(self.board.grid[0]) or ny > 2*len(self.board.grid):
                laser_path.append((nx, ny))
                break

            block_type, block_cell, edge_type = self.check_collision((laser.x, laser.y), (nx, ny))
            if block_type is not None:
                # Collision occurred
                collision_key = ((laser.x, laser.y), (laser.vx, laser.vy), block_type, edge_type)
                collision_count[collision_key] = collision_count.get(collision_key, 0) + 1

                # If the same collision condition occurs more than 3 times, force-stopping this laser to avoid infinite loop
                if collision_count[collision_key] > 3:
                    self.debug_print(f"[WARN] Repeated collision {collision_key} detected, force-stopping this laser")
                    laser.is_block = True
                    break

                self.debug_print(f"  - Collision: {curr_pos} -> ({nx},{ny}) at cell {block_cell}, block type = {block_type}, edge = {edge_type}")

                collision_x, collision_y = laser.x, laser.y

                if block_type == 'B':
                    # Block type B => Blocking
                    B_Block(block_cell)(laser)
                    # After being blocked, exit immediately
                    break

                elif block_type == 'A':
                    # Block type A => Reflection
                    A_Block(block_cell)(laser, edge_type)
                    # After collision, move the laser a half step away from the collision point
                    laser.x += laser.vx
                    laser.y += laser.vy

                elif block_type == 'C':
                    # Block type C => Splitting (one beam reflected + one transmitted)
                    from copy import deepcopy
                    main_laser = deepcopy(laser)
                    reflected_laser = A_Block(block_cell)(main_laser, edge_type)
                    # Reflected beam moves a half step away from the collision point
                    reflected_laser.x += reflected_laser.vx
                    reflected_laser.y += reflected_laser.vy

                    # Transmitted beam continues in the original direction, also moves a half step away from the collision point
                    transmit_laser = deepcopy(laser)
                    transmit_laser.x = collision_x + transmit_laser.vx
                    transmit_laser.y = collision_y + transmit_laser.vy

                    # The current laser is replaced by the reflected beam
                    laser.x, laser.y = reflected_laser.x, reflected_laser.y
                    laser.vx, laser.vy = reflected_laser.vx, reflected_laser.vy

                    # The transmitted beam is added to generated_lasers
                    generated_lasers.append((transmit_laser.x, transmit_laser.y, transmit_laser.vx, transmit_laser.vy))

            else:
                # No collision => move normally, and check if it passes through an 'o' cell
                for r in range(len(self.board.grid)):
                    for c in range(len(self.board.grid[0])):
                        if self.board.grid[r][c] == 'o':
                            ep = get_cell_edge_points(r, c)
                            if (laser.x, laser.y) in ep and (nx, ny) in ep:
                                new_candidates.add((r, c))

                laser.x, laser.y = nx, ny

            steps += 1

        return laser_path, new_candidates, generated_lasers, remaining_targets

    def check_collision(self, p1, p2):
        """
        Check if there is a collision with any placed block when moving from (p1) to (p2).
        If a collision occurs, return (block type, (r,c), edge_type); otherwise, return (None, None, None).

        Key change: Use the parity of p1 (or p2) to determine whether the edge is horizontal or vertical:
          - (odd, even)  => horizontal => invert vy
          - (even, odd)  => vertical   => invert vx
          - (even, even) => Corner (collision point at a corner, which usually does not occur), treat as no collision
        """
        for (r,c), btype in self.placed_blocks.items():
            edges = get_cell_edge_points(r,c)
            if p1 in edges and p2 in edges:
                # Indicates the laser has passed through the same edge of the block
                x, y = p1
                # Determine the collision edge based on the parity of (x, y)
                if (x % 2 == 1) and (y % 2 == 0):
                    edge_type = 'horizontal'  # invert vy
                elif (x % 2 == 0) and (y % 2 == 1):
                    edge_type = 'vertical'    # invert vx
                else:
                    # Other cases (e.g., (even, even) corner), do not process or treat as no collision
                    return None, None, None

                return btype, (r,c), edge_type

        return None, None, None


# ===== FILE: test_solver.py =====
import os
import time

def solve_all_bff_files(debug=False):
    bff_folder = os.path.join(os.path.dirname(__file__), "bff_files")
    bff_files = [f for f in os.listdir(bff_folder) if f.endswith(".bff")]
    
    print(f"[INFO] Found {len(bff_files)} .bff files in '{bff_folder}'")

    for bff_file in bff_files:
        bff_name = os.path.splitext(bff_file)[0]
        print(f"\n=== Solving: {bff_file} ===")
        
        path = os.path.join(bff_folder, bff_file)
        lazor_data = LazorBoard.from_file(path)
        
        board = Board(
            grid=lazor_data.grid,
            lasers=lazor_data.lasers,
            targets=lazor_data.targets,
            blocks=lazor_data.blocks
        )

        solver = Solver(board, debug=debug)
        
        start_time = time.time()
        success = solver.solve()
        elapsed_time = time.time() - start_time

        if success:
            print(f"[RESULT] Solution found for {bff_file} in {elapsed_time:.3f} seconds.")
            visualize_lazor_solution(board, solver.final_paths, f"{bff_name}_lazor_solution.png")
        else:
            print(f"[RESULT] No solution found for {bff_file}. (Took {elapsed_time:.3f} seconds)")

if __name__ == "__main__":
    solve_all_bff_files(debug=False)

