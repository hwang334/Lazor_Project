from LazorBoard import LazorBoard

def test(filename):
    '''
    Loads and prints the board information from a given .bff file.

    *filename: str*
        The name of the .bff file (without extension) located in bff_files/.
    '''
    board = LazorBoard.from_file(f'bff_files/{filename}.bff')
    print('--- Lazor Board Info ---')
    print(board)

if __name__ == '__main__':
    test('mad_1')

