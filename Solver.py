from LazorBoard import LazorBoard
from Blocks import A_Block, B_Block, C_Block, Laser
import copy

def simulate_lasers(board):
    '''
    Simulates the lasers on the board and returns the set of hit target points.

    *board: LazorBoard*
        The board instance with lasers and targets.

    *return: set*
        Set of (x, y) target points hit by any laser.
    '''
    hit_targets = set()
    active_lasers = [Laser(x, y, vx, vy) for (x, y, vx, vy) in board.lasers]

    for laser in active_lasers:
        steps = 0
        while steps < 100:  # Limit to 100 steps to avoid infinite loops
            laser.move()
            pos = (laser.x, laser.y)

            if pos in board.targets:
                hit_targets.add(pos)

            if board.out_of_bounds(pos):  # Check if laser goes out of bounds
                break

            block = board.get_block_at(laser.x, laser.y)  # Get block at current position
            if block is not None:
                if isinstance(block, A_Block):  # Handle A_Block interaction
                    laser = block(laser)
                elif isinstance(block, B_Block):  # Handle B_Block interaction
                    laser = block(laser)
                    break  # Stop laser on B_Block
                elif isinstance(block, C_Block):  # Handle C_Block interaction
                    reflected, transmitted = block(laser)
                    active_lasers.append(reflected)  # Add reflected laser
                    laser = transmitted  # Continue with transmitted laser
            steps += 1

    return hit_targets

def solve_lazor(board):
    '''
    Tries to place blocks on the board, simulates lasers, and checks if all targets are hit.

    *board: LazorBoard*
        A LazorBoard instance with available blocks and empty slots.

    *return: LazorBoard or None*
        A solved LazorBoard if a solution exists, otherwise None.
    '''
    empty_slots = board.get_empty_slots()  # Get all empty slots on the board
    block_list = [B_Block for _ in range(board.blocks.get('B', 0))] + \
                 [A_Block for _ in range(board.blocks.get('A', 0))] + \
                 [C_Block for _ in range(board.blocks.get('C', 0))]

    # Try all combinations of blocks and place them on the board
    return backtrack(board, empty_slots, block_list, 0)

def backtrack(board, empty_slots, block_list, index):
    if index == len(block_list):
        # If all blocks have been placed, try to simulate the lasers and check if the targets are hit
        if board.simulate_lasers():
            return board
        return None

    x, y = empty_slots[index]
    block = block_list[index]

    # Use the block type string (e.g., 'A', 'B', or 'C') instead of the block class
    block_type = block.__name__[0]  # Get the first letter of the block class name ('A', 'B', 'C')
    
    # Try placing the block at the current position
    if board.place_block(x, y, block_type):
        result = backtrack(board, empty_slots, block_list, index + 1)
        if result:
            return result

        # If no solution is found, remove the block and try the next possibility
        board.grid[y][x] = 'o'
        board.blocks[block_type] += 1

    return None


def save_solution_to_txt(solution, filename):
    '''
    Save the solved grid with blocks to a .txt file.

    * solution: list[list[str]] 
        The grid with placed blocks (e.g. 'A', 'B', 'C').
    * filename: str
        Name of the output file, should end with .txt.
    '''
    with open(filename, 'w') as f:
        for row in solution:
            f.write('  '.join(row) + '\n')  # Save each row of the grid

if __name__ == '__main__':
    # Read the board from a .bff file
    board = LazorBoard.from_file('bff_files/dark_1.bff')
    solved = solve_lazor(board)  # Solve the puzzle

    if solved:
        print("Solution found:")
        for row in solved.grid:
            print(' '.join(row))  # Print the solved board

        # Save the solved grid to a file
        board_name = 'dark_1'  # You can dynamically extract the board name if needed
        save_solution_to_txt(solved.grid, f'{board_name}_solution.txt')
    else:
        print("No solution found.")
