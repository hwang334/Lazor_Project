import os
import time
from LazorBoard import LazorBoard
from Classes import Board
from Solver import Solver
from LazorVisualizer import visualize_lazor_solution

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
