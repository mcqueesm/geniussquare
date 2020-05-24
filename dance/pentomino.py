import matplotlib.cm
import matplotlib.pyplot
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages
import sys
import dance as dance
import json

class Piece(object):
    def __init__(self, letter, mask):
        self.letter = letter
        self.mask = mask.astype(np.bool)
        self.color = (1.0, 1.0, 1.0, 1.0)

    def unique_rotations(self):
        unique = [self.mask]

        for r in [0, 1, 2, 3]:
            for f in [0, 1]:
                rotated = self.rotation(r, f)

                is_new = True
                for u in unique:
                    if np.array_equal(u, rotated):
                        is_new = False
                        break

                if is_new:
                    unique.append(rotated)

        return unique

    def rotation(self, r, f):
        rotated = self.mask
        for i in range(r):
            rotated = np.rot90(rotated)

        if f:
            rotated = np.fliplr(rotated)
        return rotated

pieces = [Piece('P', np.array([[1, 1],
                               [1, 1]])),
          Piece('X', np.array([[0, 1],
                               [1, 1],
                               [0, 1]])),
          Piece('F', np.array([[0, 1],
                               [1, 1],
                               [1, 0]])),
          Piece('V', np.array([[1],
                               [1],
                               [1]])),
          Piece('W', np.array([[1],
                               [1]])),
          Piece('Z', np.array([[1]])),
          Piece('U', np.array([[1, 0],
                               [1, 1]])),
          Piece('N', np.array([[1, 1],
                               [0, 1],
                               [0, 1]])),
          Piece('I', np.array([[1],
                               [1],
                               [1],
                               [1]]))]

boards = {}
boards['hollow_chess_board'] = np.array([[1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1]],
                                       dtype=np.bool)

def is_valid_location(board, mask, location):
    i, j = location
    di, dj = mask.shape

    subboard = board[i:i+di, j:j+dj]
    if subboard.shape == mask.shape and np.array_equal(mask, mask & subboard):
        return True
    else:
        return False

def valid_locations(board, mask):
    locations = [(i,j) for i in range(board.shape[0]) for j in range(board.shape[1])]
    return filter(lambda loc: is_valid_location(board, mask, loc), locations)

def fill_in_row(row, piece_index, mask, location, column_map):
    i, j = location

    row[piece_index] = True
    for r, mr in enumerate(mask):
        for c, v in enumerate(mr):
            if v:
                row[column_map[i+r, j+c]] = True

def exact_cover_problem(board):
    n_piece_columns = len(pieces)
    n_space_columns = np.nonzero(board)[0].size

    n_columns = n_piece_columns + n_space_columns

    column_map = np.cumsum(board).reshape(board.shape) + n_piece_columns - 1

    rows = []
    row_labels = []
    for piece_index, piece in enumerate(pieces):
        for mask in piece.unique_rotations():
            for location in valid_locations(board, mask):
                row = np.zeros(n_columns, dtype=np.bool)
                fill_in_row(row, piece_index, mask, location, column_map)
                rows.append(row)

    return np.array(rows, dtype=np.bool)

def exact_cover_row_labels(board):
    labels = []
    for piece_index, piece in enumerate(pieces):
        for mask_index, mask in enumerate(piece.unique_rotations()):
            for location in valid_locations(board, mask):
                labels.append((piece.letter, piece_index, mask_index, location))

    return labels

def simplified_chess_board_problems():
    base = exact_cover_problem(boards['hollow_chess_board'])
    labels = exact_cover_row_labels(boards['hollow_chess_board'])
    n_columns = base.shape[1]

    # Generate the 'X at 23' problem
    mask = np.array([l[0] == 'X' and l[3] != (0,1) for l in labels], dtype=np.bool)
    base_0 = base.copy()
    base_0[mask, :] = 0

    # Generate the 'X at 24' problem
    mask = np.array([l[0] == 'X' and l[3] != (0,2) for l in labels], dtype=np.bool)
    base_1 = base.copy()
    base_1[mask, :] = 0

    # Generate the 'X at 33, P not flipped' problem
    xmask = np.array([l[0] == 'X' and l[3] != (1,1) for l in labels], dtype=np.bool)
    pmask = np.array([l[0] == 'P' and l[2] in [0,2,4,6] for l in labels], dtype=np.bool)
    base_2 = base.copy()
    base_2[xmask, :] = 0
    base_2[pmask, :] = 0

    return base_0, base_1, base_2

def load_solution(filename):
    solution = []
    with open(filename) as f:
        for line in f:
            solution.append(np.fromstring(line, dtype=np.int, sep=' '))

    return solution

def display_solution(board, solution, index, fig):
    print('in display solution ', index)
    colored = np.zeros((board.shape[0], board.shape[1], 4))
    labels = exact_cover_row_labels(board)

    for row in solution:
        l = labels[row]
        piece_index = l[1]
        mask_index = l[2]
        i, j = l[3]
        color = matplotlib.cm.rainbow(piece_index / float(len(pieces)))

        mask = pieces[piece_index].unique_rotations()[mask_index]
        for r, mr in enumerate(mask):
            for c, v in enumerate(mr):
                if v:
                    colored[i+r, j+c] = color

   
    matplotlib.pyplot.imshow(colored, interpolation='nearest')
    matplotlib.pyplot.axis('off')
    fig.savefig("catalog/static/solutions{0}.png".format(index))
   

dice = [[(1, 3), (3, 2), (2, 3), (2, 2), (3, 3), (4, 2)],
        [(5, 2), (0, 0), (4, 1), (3, 0), (2, 0), (3, 1)],
        [(3, 4), (4, 5), (4, 4), (4, 3), (5, 3), (5, 4)],
        [(1, 2), (0, 1), (2, 1), (1, 0), (1, 1), (0, 2)],
        [(0, 3), (2, 5), (2, 4), (1, 4), (3, 5), (5, 5)],
        [(5, 1), (0, 4), (1, 5), (4, 0)],
        [(5, 0), (0, 5)]]
def diceGen():
    roll = [(0, 0) for x in range(0, 7)]
    for a in range (0, 6):
        roll[0]=dice[0][a]
        for b in range (0, 6):
            roll[1]=dice[1][b]
            for c in range (0, 6):
                roll[2]=dice[2][c]
                for d in range (0, 6):
                    roll[3]=dice[3][d]
                    for e in range (0, 6):
                        roll[4]=dice[4][e]
                        for f in range (0, 4):
                            roll[5]=dice[5][f]
                            for g in range (0, 2):
                                roll[6]=dice[6][g]
                                yield roll

"""
if __name__ == '__main__':
    numDic = {
        'A': 0,
        'B': 1,
        'C': 2, 
        'D': 3,
        'E': 4,
        'F': 5
    }
    #gen = diceGen()
    
    inputstr = input('Enter dice values:')
    dlist = inputstr.split()
    for x in dlist:
        boards['hollow_chess_board'][int(numDic[x[0]]), int(x[1])-1] = 0
    
    allSolutions = {'solutions': []}
    

    for i, r in enumerate(gen):
   
        b = np.copy(boards['hollow_chess_board'])
        print("r is ", r)
        for d in list(r):
            print("d is ", d)
            b[d[0], d[1]] = 0
        
        print('Saving problem...')
        np.savetxt('sub_problem_1', exact_cover_problem(b).astype(np.int), fmt='%r')
        mat = np.loadtxt('sub_problem_1')
        dl = dance.DancingLinks(mat)
        snum = dl.generate_num_of_solutions(i)
        allSolutions['solutions'].append([snum, list(r)])
            
        
    with open('sols.json', 'w', encoding='utf-8') as f:
        json.dump(allSolutions, f, ensure_ascii=False, indent=4)

    
    print('Saving problem...')
    np.savetxt('sub_problem_1', exact_cover_problem(boards['hollow_chess_board']).astype(np.int), fmt='%r')
    print('Solving problem...')
    os.spawnl(os.P_WAIT, '/usr/bin/python', 'python', 'dance.py', 'sub_problem_1', 'solution_1')
    solution = load_solution('solution_1')
    cols = 5
    #rows = 20
    rows = (len(solution) // 5) + 1
    fig = matplotlib.pyplot.figure(figsize=(10, 40))
    fig.suptitle('Number of solutions for \n {s}: \n {t}'.format(s= inputstr, t=len(solution)), fontsize=40)
    for i in range(1, len(solution)+1):
        display_solution(boards['hollow_chess_board'], solution[i-1], fig, rows, cols, i)

    
    pdf = PdfPages('solutions.pdf')
    pdf.savefig()

    pdf.close()
    #matplotlib.pyplot.show()
    """