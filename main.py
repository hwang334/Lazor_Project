from LazorBoard import LazorBoard
from Solver import solve_lazor, save_solution_to_txt

if __name__ == '__main__':
    # Prompt the user to input the level name
    level_name = input("Enter the level name (e.g., dark_1): ")  # User inputs the level name

    # Read and parse the level file using the provided level name
    board = LazorBoard.from_file(f'bff_files/{level_name}.bff')

    # Solve the puzzle by finding the correct block placement
    solved_board = solve_lazor(board)

    if solved_board:
        # If a solution is found, print it and save to a file
        print(f"Solution found for {level_name}:")
        print(solved_board)

        # Save the solution grid to a .txt file
        save_solution_to_txt(solved_board.grid, f'{level_name}_solution.txt')
    else:
        # If no solution is found, inform the user
        print(f"No solution found for {level_name}.")
