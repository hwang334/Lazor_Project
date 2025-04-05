from LazorBoard import LazorBoard

def test_dark_1():
    '''
    Loads and prints the board information from dark_1.bff for testing purposes.
    '''
    board = LazorBoard.from_file('bff_files/dark_1.bff')
    print('--- Lazor Board Info ---')
    print(board)

if __name__ == '__main__':
    test_dark_1()
