import matplotlib.pyplot as plt

def visualize_lazor_solution(board, laser_paths, output_filename="lazor_solution.png"):

    rows = len(board.grid)
    cols = len(board.grid[0]) if rows > 0 else 0

    fig, ax = plt.subplots(figsize=(cols * 0.8, rows * 0.8))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.invert_yaxis()

    # Draw grid lines
    for x in range(cols + 1):
        ax.axvline(x, color='black', linewidth=0.5)
    for y in range(rows + 1):
        ax.axhline(y, color='black', linewidth=0.5)

    color_map = {
        'x': 'lightgrey',
        'o': 'white',
        'A': 'limegreen',
        'B': 'tomato',
        'C': 'royalblue'
    }

    # Draw each cell of the board
    for r in range(rows):
        for c in range(cols):
            cell = board.grid[r][c]
            facecolor = color_map.get(cell, 'white')
            rect = plt.Rectangle((c, r), 1, 1, facecolor=facecolor, edgecolor='none')
            ax.add_patch(rect)

    # Draw target points (convert half-grid coordinates to plotting coordinates)
    for (tx, ty) in board.targets:
        # Multiply half-grid coordinates by 0.5 to convert to plotting coordinates
        x = tx * 0.5
        y = ty * 0.5
        ax.plot(x, y, marker='*', markersize=15,
                color='gold', markeredgecolor='black', markeredgewidth=1)

    # Draw laser trajectories
    laser_colors = ['red', 'cyan', 'orange', 'magenta', 'blue', 'green']
    for i, path in enumerate(laser_paths):
        xs = [p[0] * 0.5 for p in path]
        ys = [p[1] * 0.5 for p in path]
        color = laser_colors[i % len(laser_colors)]
        ax.plot(xs, ys, color=color, linewidth=2, marker='o', markersize=3)

    ax.set_title("Lazor Puzzle Solution")
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"Visualization saved to: {output_filename}")
