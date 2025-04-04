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

    def simulate_lasers(self):
        '''
        Simulates all lasers and checks if they hit the targets.
        
        Returns:
            bool: True if all targets are hit, False otherwise.
        '''
        for laser in self.lasers:
            x, y, vx, vy = laser
            while 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid):
                if self.grid[y][x] == 'x':
                    break  # Hit a wall, stop
                if (x, y) in self.targets:
                    self.targets.remove((x, y))
                    break
                if self.grid[y][x] in ['A', 'B', 'C']:
                    # Reflect, refract, or block the laser based on block type
                    if self.grid[y][x] == 'A':
                        vx, vy = -vx, -vy  # Reflect
                    elif self.grid[y][x] == 'B':
                        vx, vy = vy, vx  # Refract
                    # 'C' block type might just block the laser path (no direction change)
                x += vx
                y += vy
        return len(self.targets) == 0


class Solver:
    '''
    Solves the laser puzzle by testing different block placements and checking if all targets are hit.
    
    board: *Board*
        The game board containing grid, lasers, and target positions.
    '''
    def __init__(self, board):
        self.board = board

    def solve(self):
        '''
        Attempts to solve the puzzle by placing blocks and simulating the laser paths.
        '''
        # Iterate through the block types and positions to test placing blocks
        for block_type in self.board.blocks:
            for y in range(len(self.board.grid)):
                for x in range(len(self.board.grid[0])):
                    if self.board.place_block(x, y, block_type):
                        # After placing the block, simulate the lasers
                        if self.board.simulate_lasers():
                            # If the lasers hit all targets, return the solved board
                            return self.board.grid
                        else:
                            # Revert block placement if not successful
                            self.board.grid[y][x] = 'o'
                            self.board.blocks[block_type] += 1
        return None  # No solution found


class Laser:
    '''
    Simulates the behavior of a laser on the board, tracking its movement and interactions.
    
    x: *int*
        Initial x-coordinate of the laser.
    y: *int*
        Initial y-coordinate of the laser.
    vx: *int*
        Velocity in the x direction.
    vy: *int*
        Velocity in the y direction.
    '''
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        '''
        Moves the laser to the next position based on its velocity.
        '''
        self.x += self.vx
        self.y += self.vy

    def get_position(self):
        '''
        Returns the current position of the laser.
        
        Returns:
            tuple[int, int]: Current (x, y) coordinates of the laser.
        '''
        return self.x, self.y


class A_Block:
    '''
    Reflective block that changes the laser direction upon contact.

    *Parameters*
        position: *tuple*
            A tuple (x, y) representing the block's position on the grid.
    '''

    def __init__(self, position):
        '''
        Initialize a ReflectBlock object with its position.

        *Parameters*
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        # Initialize the block's position
        self.position = position

    def reflect(self, laser: 'Laser') -> 'Laser':
        '''
        Reflects the laser based on its impact on the block.

        *Parameters*
            laser: *Laser*
                An object representing the laser with position and velocity.

        *Returns*
            Laser: The laser object with updated position and velocity after reflection.
        '''
        # Calculate the relative position of the laser to the block
        relative_position = (laser.x - self.position[0],
                             laser.y - self.position[1])

        # Reflect the laser based on its relative position
        if (relative_position == (0, 1) or
                relative_position == (0, -1)):  # Vertical hit
            laser.vy = -laser.vy
        elif (relative_position == (1, 0) or
              relative_position == (-1, 0)):  # Horizontal hit
            laser.vx = -laser.vx

        # Update the laser's position
        laser.x += laser.vx
        laser.y += laser.vy

        return laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to reflect a laser.

        *Parameters*
            laser: *Laser*
                The laser object to be reflected.

        *Returns*
            Laser: The updated laser object.
        '''
        return self.reflect(laser)


class B_Block:
    '''
    Opaque block that stops the laser completely.

    *Parameters*
        position: *tuple*
            A tuple (x, y) representing the block's position on the grid.
    '''

    def __init__(self, position):
        '''
        Initialize an OpaqueBlock object with its position.

        *Parameters*
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        # Initialize the block's position
        self.position = position

    def opaque(self, laser):
        '''
        Stops the laser completely upon contact.

        *Parameters*
            laser: *Laser*
                An object representing the laser with position and velocity.

        *Returns*
            Laser: The laser object with updated position and stopped state.
        '''
        # Mark the laser as blocked
        laser.is_block = True
        return laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to block a laser.

        *Parameters*
            laser: *Laser*
                The laser object to be blocked.

        *Returns*
            Laser: The updated laser object.
        '''
        return self.opaque(laser)


class C_Block:
    '''
    Refractive block that allows part of the laser to pass while reflecting another part.

    *Parameters*
        position: *tuple*
            A tuple (x, y) representing the block's position on the grid.
    '''

    def __init__(self, position):
        '''
        Initialize a RefractBlock object with its position.

        *Parameters*
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        # Initialize the block's position
        self.x, self.y = position

    def refract(self, laser):
        '''
        Refracts the laser based on its impact on the block.

        *Parameters*
            laser: *Laser*
                An object representing the laser with position and velocity.

        *Returns*
            laser: *Laser*
                The original laser object.
            new_laser: *Laser*
                The laser object with updated position and velocity after refraction.
        '''
        # Calculate the relative position of the laser to the block
        laser_vx = laser.vx
        laser_vy = laser.vy
        # Laser comes from left or right
        if (self.x - 1, self.y) == (laser.x, laser.y) or \
                (self.x + 1, self.y) == (laser.x, laser.y):
            laser_vx = -laser.vx
        # Laser comes from up or down
        if (self.x, self.y - 1) == (laser.x, laser.y) or \
                (self.x, self.y + 1) == (laser.x, laser.y):
            laser_vy = -laser.vy
        # Create a new laser object with the updated velocity
        new_laser = Laser((laser.x, laser.y), (laser_vx, laser_vy))
        laser()
        return new_laser, laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to refract a laser.

        *Parameters*
            laser: *Laser*
                The laser object to be refracted.

        *Returns*
            laser: *Laser*
                The updated laser object.
        '''
        return self.refract(laser)
