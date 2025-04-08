from LazorBoard import LazorBoard
from Classes import Board
from LazorVisualizer import visualize_lazor_solution
from Solver import Solver  # Assuming your solver file is named Solver.py and defines MySolver

def test_solver(bff_name: str, debug=False):
    """
    :param bff_name: bff file name without extension, e.g., "mad_4"
    :param debug: If True, a large amount of debug information will be printed to the console
    """
    # Parse the .bff file
    path = f"bff_files/{bff_name}.bff"  # Adjust according to the path of the .bff file in your project
    lazor_data = LazorBoard.from_file(path)
    print(f"[TEST] Successfully parsed {bff_name}.bff:")
    print(lazor_data)

    # Construct the Board object
    board = Board(
        grid=lazor_data.grid,
        lasers=lazor_data.lasers,
        targets=lazor_data.targets,
        blocks=lazor_data.blocks
    )

    # Create the solver and run the solution
    solver = Solver(board, debug=debug)
    success = solver.solve()

    # If a solution is found, visualize and save it
    if success:
        print("[TEST] Solution found! Visualizing...")
        visualize_lazor_solution(board, solver.final_paths, "lazor_solution.png")
        print("[TEST] Visualization saved as lazor_solution.png")
    else:
        print("[TEST] No solution found.")

if __name__ == "__main__":
    
    test_solver("numbered_6", debug=False)
