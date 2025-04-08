from LazorBoard import LazorBoard

# def test_place_block():
#     # Create a 5x5 empty grid
#     grid = [['o' for _ in range(5)] for _ in range(5)]
#     blocks = {'A': 3, 'B': 2, 'C': 1}
#     board = LazorBoard(grid, [], [], blocks)
    
#     # Try placing an 'A' block at position (1, 1)
#     print("Before placing block:")
#     print(board.grid)
    
#     result = board.place_block(1, 1, 'A')  # Should return True
#     print(f"Place block result: {result}")
    
#     # Check board state after placing the block
#     print("After placing block:")
#     print(board.grid)
    
#     # Check remaining block count
#     print("Remaining blocks:", board.blocks)
    
#     # Try placing a block at the same position again, it should return False because the spot is already occupied
#     result2 = board.place_block(1, 1, 'B')  # Should return False
#     print(f"Place block result at (1, 1) again: {result2}")
    
#     # Try placing a block at an invalid position (10, 10), it should return False
#     result3 = board.place_block(10, 10, 'C')  # Should return False
#     print(f"Place block result at (10, 10): {result3}")
    
# test_place_block()

if __name__ == '__main__':
    board = LazorBoard.from_file('bff_files/mad_1.bff') 
    print("Before placing block:")
    print(board.grid)
    result = board.place_block(1, 1, 'A')  
    print(f"Result of placing block: {result}")
    print("After placing block:")
    print(board.grid)
