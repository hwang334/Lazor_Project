from Blocks import A_Block, B_Block, C_Block, Laser



class LazorBoard:
    '''
    Parses a .bff file to initialize the Lazor board setup.

    Attributes
    ----------
    grid : *list[list[str]]*
        The board layout with 'o' for valid positions and 'x' for invalid.
    blocks : *dict[str, int]*
        A dictionary with keys 'A', 'B', and 'C' representing block types and their available counts.
    lasers : *list[Laser]*
        List of Laser objects that represent lasers on the board.
    targets : *list[tuple[int, int]]*
        List of target coordinates that need to be hit.
    '''
    def __init__(self, grid, blocks, lasers, targets):
        self.grid = grid
        self.blocks = blocks
        self.lasers = [Laser(x, y, vx, vy) for x, y, vx, vy in lasers]  # Use Laser class instances
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
        print(f"Blocks after reading file: {blocks}") 
        return cls(grid, blocks, lasers, targets)

    def __str__(self):
        '''
        Returns a nicely formatted string representation of the Lazor board.
        '''
        grid_str = '\n'.join([' '.join(row) for row in self.grid])
        blocks_str = ', '.join([f'{k}: {v}' for k, v in self.blocks.items()])
        lasers_str = '\n'.join([f'  - ({x}, {y}) direction ({vx}, {vy})' for x, y, vx, vy in self.lasers])
        targets_str = '\n'.join([f'  - ({x}, {y})' for x, y in self.targets])

        return (
            f'=== Lazor Board ===\n'
            f'Grid:\n{grid_str}\n\n'
            f'Blocks: {blocks_str}\n\n'
            f'Lasers:\n{lasers_str}\n\n'
            f'Targets:\n{targets_str}\n'
        )

    def get_empty_slots(self):
        ''' Returns a list of empty slots (positions with 'o') on the grid. '''
        empty_slots = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 'o':
                    empty_slots.append((x, y))
        return empty_slots

    def out_of_bounds(self, pos):
        ''' Returns True if the position is outside the grid boundaries. '''
        x, y = pos
        return not (0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid))

    def is_valid_position(self, x, y):
        '''
        Checks if a given coordinate is a valid position for placing a block.
        
        x: *int*
            The x-coordinate on the board.
        y: *int*
            The y-coordinate on the board.
        '''
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid) and self.grid[y][x] == 'o'

    def place_block(self, x, y, block_type):
        '''
        Places a block of a given type on the board.
        
        x: *int*
            The x-coordinate where the block will be placed.
        y: *int*
            The y-coordinate where the block will be placed.
        block_type: *str*
            The type of block ('A', 'B', or 'C') to place.
        '''
        
        if self.is_valid_position(x, y) and self.blocks[block_type] > 0:
            self.grid[y][x] = block_type
            self.blocks[block_type] -= 1
            return True
        return False

    def get_block_at(self, x, y):
        '''
        Returns the block at the given position (x, y) on the grid.
        
        x: *int*
            The x-coordinate of the position.
        y: *int*
            The y-coordinate of the position.
        
        Returns:
            str: The type of block at the position, or 'o' if no block is present.
        '''
        if 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
            return self.grid[y][x]  # Return the type of block or 'o' if empty
        return 'o'

    def simulate_lasers(self):
        '''
        Simulates all lasers and checks if they hit the targets.
        
        Returns:
            bool: True if all targets are hit, False otherwise.
        '''
        for laser in self.lasers:
            while 0 <= laser.x < len(self.grid[0]) and 0 <= laser.y < len(self.grid):
                block = self.get_block_at(laser.x, laser.y)  # Get block at current position
                if block == 'x':
                    break  # Hit a wall, stop
                if (laser.x, laser.y) in self.targets:
                    self.targets.remove((laser.x, laser.y))
                    break
                if block in ['A', 'B', 'C']:
                    block_obj = A_Block((laser.x, laser.y)) if block == 'A' else \
                                B_Block((laser.x, laser.y)) if block == 'B' else \
                                C_Block((laser.x, laser.y))
                    laser = block_obj(laser)  # Use the block's __call__ method to interact with the laser
                laser.move()  # Move the laser using the Laser class's move method
        return len(self.targets) == 0

def __deepcopy__(self, memo):
    '''Support deep copy'''
    from copy import deepcopy
    result = LazorBoard(
        deepcopy(self.grid), 
        deepcopy(self.blocks), 
        [(l.x, l.y, l.vx, l.vy) for l in self.lasers], 
        deepcopy(self.targets)
    )
    return result

def print_solution(self, output_file=None):
    '''
    Print the solution and optionally save it to a file
    
    Parameters:
        output_file (str, optional): Path to the output file
    '''
    output = []
    for row in self.grid:
        output.append(' '.join(row))
    
    solution_str = '\n'.join(output)
    print(solution_str)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(solution_str)
        print(f'Solution saved to {output_file}')
