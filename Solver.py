from itertools import permutations
from copy import deepcopy
from Blocks import A_Block, B_Block, C_Block, Laser
from LazorBoard import LazorBoard
from collections import Counter

class Solver:
    '''
    A class that encapsulates the Lazor puzzle solver logic.

    board : *LazorBoard*
        The board instance to solve.
    '''
    def __init__(self, board):
        '''
        Initialize the Solver with a LazorBoard instance.

        *board: LazorBoard*
            The puzzle board to solve.
        '''
        self.board = board
        # Get all possible positions for blocks (positions with 'o')
        self.all_PosBlock = self._get_all_possible_positions()
        # Initialize lasers from the board
        self.lasers = [Laser(l.x, l.y, l.vx, l.vy) for l in self.board.lasers]

    def _get_all_possible_positions(self):
        '''
        Get all possible positions where blocks can be placed (positions with 'o').
        
        **Returns**
            *list*: List of positions where blocks can be placed.
        '''
        positions = []
        for y in range(len(self.board.grid)):
            for x in range(len(self.board.grid[y])):
                if self.board.grid[y][x] == 'o':
                    # Using (x, y) format for consistency
                    positions.append((x, y))
        return positions

    def insert(self, block_position, grid):
        '''
        Adds blocks to the grid based on the provided positions.

        **Parameters**
            block_position: *list*
                List of (block_type, position) tuples.
            grid: *list*
                The grid to which blocks are added.

        **Returns**
            grid: *list*
                The grid after adding the blocks.
        '''
        # Add the blocks to the grid
        for block_type, position in block_position:
            x, y = position
            grid[y][x] = block_type
        return grid

    def position_available(self, laser):
        '''
        Checks if the next position of a laser is within the grid.

        **Parameters**
            laser: *Laser*
                The laser to check.

        **Returns**
            *bool*
        '''
        next_x = laser.x + laser.vx
        next_y = laser.y + laser.vy
        return 0 <= next_x < len(self.board.grid[0]) and 0 <= next_y < len(self.board.grid)

    def check_lasers(self, lasers, tmp_grid, targets):
        '''
        Checks the paths of lasers on the grid, considering block interactions.

        **Parameters**
            lasers: *list*
                List of lasers to check.
            tmp_grid: *list*
                The temporary grid to check lasers' paths.
            targets: *list*
                List of target points.

        **Returns**
            lasers: *list*
                List of lasers after checking paths.
            targets: *list*
                List of targets points after checking paths.
        '''
        for laser in lasers[:]:  # Use a copy to allow appending to original list
            # Add is_block attribute if not present
            if not hasattr(laser, 'is_block'):
                laser.is_block = False

            while self.position_available(laser) and not laser.is_block:
                # Move the laser
                laser.move()
                
                # Check if the laser hit a target
                if (laser.x, laser.y) in targets:
                    targets.remove((laser.x, laser.y))

                # Check if the laser hit a block
                if 0 <= laser.x < len(tmp_grid[0]) and 0 <= laser.y < len(tmp_grid):
                    block_type = tmp_grid[laser.y][laser.x]
                    
                    if block_type == 'A':
                        block = A_Block((laser.x, laser.y))
                        laser = block(laser)
                    elif block_type == 'B':
                        block = B_Block((laser.x, laser.y))
                        laser = block(laser)
                        break  # B blocks stop the laser
                    elif block_type == 'C':
                        block = C_Block((laser.x, laser.y))
                        try:
                            new_laser, laser = block(laser)
                            lasers.append(new_laser)
                        except Exception as e:
                            # Fix any implementation issues in C_Block
                            print(f"Error with C_Block: {e}")
                            break
                    elif block_type == 'x':
                        # Hit a wall, stop the laser
                        break

        return lasers, targets

    def unique_permutations(self, elements):
        """
        Generate all unique permutations of the input list in a sorted manner.
        
        Parameters:
            elements: list
                A list of elements to permute.
                
        Yields:
            tuple: A unique permutation of the elements list.
        """
        elements.sort()
        counter = Counter(elements)
        
        def permute(sequence):
            if not sequence:
                yield tuple()
            else:
                for element in counter:
                    if counter[element] > 0:
                        counter[element] -= 1
                        for sub_permute in permute(sequence[1:]):
                            yield (element,) + sub_permute
                        counter[element] += 1
                        
        return permute(elements)

    def solve(self):
        '''
        Attempts to solve the game by iterating through all possible block combinations and laser paths.

        **Returns**
            *LazorBoard*: A solved board if a solution is found, None otherwise.
        '''
        # Get all blocks we need to place
        block_list = (
            ['A'] * self.board.blocks['A'] +
            ['B'] * self.board.blocks['B'] +
            ['C'] * self.board.blocks['C']
        )
        
        print(f"Block list: {block_list}")
        print(f"All possible positions: {self.all_PosBlock}")
        
        # Fill remaining positions with 'o' (no block)
        empty_slots = ['o'] * (len(self.all_PosBlock) - len(block_list))
        
        # Get all possible combinations of block positions
        all_possible_combinations = self.unique_permutations(block_list + empty_slots)
        
        # Try each combination
        for block_position in all_possible_combinations:
            # Pair each block type with a position
            block_position = list(zip(block_position, self.all_PosBlock))
            
            # Create a temporary grid with the blocks placed
            tmp_grid = self.insert(block_position, deepcopy(self.board.grid))
            
            # Create temporary copies of lasers and targets
            lasers = [Laser(l.x, l.y, l.vx, l.vy) for l in self.board.lasers]
            targets = deepcopy(self.board.targets)
            
            # Check if this arrangement solves the puzzle
            lasers, targets = self.check_lasers(lasers, tmp_grid, targets)
            
            # If all targets are hit, we've found a solution
            if not targets:
                # Create a new board with the solution
                solved_board = deepcopy(self.board)
                solved_board.grid = tmp_grid
                return solved_board
                
        # No solution found
        return None
    
    def save_solution_to_txt(self, grid, filename):
        '''
        Saves the solution grid to a text file.
        
        **Parameters**
            grid: *list*
                The grid to save.
            filename: *str*
                The name of the file to save to.
        '''
        with open(filename, 'w') as f:
            for row in grid:
                f.write(' '.join(row) + '\n')
        print(f"Solution saved to {filename}")

        update
        