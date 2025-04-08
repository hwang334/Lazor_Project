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
