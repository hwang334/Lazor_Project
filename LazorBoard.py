
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
