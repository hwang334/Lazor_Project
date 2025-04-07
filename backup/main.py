from LazorBoard import LazorBoard
from Solver import Solver
import os



if __name__ == '__main__':
    # Prompt the user to input the level name
    level_name = input("Enter the level name (e.g., dark_1): ")  # User inputs the level name
    
    # Make sure the bff_files directory exists
    bff_dir = 'bff_files'
    if not os.path.exists(bff_dir):
        print(f"Warning: Directory '{bff_dir}' not found. Creating directory...")
        os.makedirs(bff_dir)
    
    # Get the full path to the file
    file_path = f'{bff_dir}/{level_name}.bff'
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist. Please check the file name and path.")
        exit(1)

    # Read and parse the level file using the provided level name
    try:
        board = LazorBoard.from_file(file_path)
        print(f"Board loaded successfully:")
        print(board)
    except Exception as e:
        print(f"Error loading board: {e}")
        exit(1)

    # Create a Solver instance with the board
    solver = Solver(board)

    # Attempt to solve the puzzle
    print("Solving puzzle...")
    solved_board = solver.solve()

    if solved_board:
        # If a solution is found, print it and save to a file
        print(f"Solution found for {level_name}:")
        for row in solved_board.grid:
            print(' '.join(row))

        # Create a solution directory if it doesn't exist
        solution_dir = 'solutions'
        if not os.path.exists(solution_dir):
            os.makedirs(solution_dir)
            
        # Save the solution grid to a .txt file
        solution_file = f'{solution_dir}/{level_name}_solution.txt'
        solver.save_solution_to_txt(solved_board.grid, solution_file)
        print(f"Solution saved to {solution_file}")
    else:
        # If no solution is found, inform the user
        print(f"No solution found for {level_name}.")
