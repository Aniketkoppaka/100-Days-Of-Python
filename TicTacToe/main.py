import random

def display_board(board):
    """
    Prints out a 3x3 Tic-Tac-Toe board.
    """
    print('\n' * 100)
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9] + ' ')
    print('___________')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6] + ' ')
    print('___________')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3] + ' ')

def player_input():
    """
    Asks the player to choose X or O.
    Returns a tuple with (Player 1 marker, Player 2 marker).
    """
    marker = ''
    while not (marker == 'X' or marker == 'O'):
        marker = input('Player 1, do you want to be X or O? ').upper()
    if marker == 'X':
        return 'X', 'O'
    else:
        return 'O', 'X'

def place_marker(board, marker, position):
    """
    Assigns the marker ('X' or 'O') to a specific position on the board.
    """
    board[position] = marker

def check_win(board, mark):
    """
    Checks all rows, columns, and diagonals for a win.
    Returns True if the player with the given 'mark' has won.
    """
    return ((board[7] == mark and board[8] == mark and board[9] == mark) or  #Checking rows
            (board[4] == mark and board[5] == mark and board[6] == mark) or
            (board[1] == mark and board[2] == mark and board[3] == mark) or
            (board[7] == mark and board[4] == mark and board[1] == mark) or  #Checking columns
            (board[8] == mark and board[5] == mark and board[2] == mark) or
            (board[9] == mark and board[6] == mark and board[3] == mark) or
            (board[7] == mark and board[5] == mark and board[3] == mark) or  #Checking diagonals
            (board[9] == mark and board[5] == mark and board[1] == mark))

def choose_first():
    """
    Randomly chooses which player goes first.
    """
    if random.randint(0,1) == 0:
        return 'Player 2'
    else:
        return 'Player 1'

def space_check(board, position):
    """
    Returns True if the position on the board is empty.
    """
    return board[position] == ' '

def check_full_board(board):
    """
    Checks if the board is full.
    Returns True if full, False otherwise.
    """
    for i in range(1, 10):
        if space_check(board, i):
            return False
    return True

def player_choice(board):
    """
    Gets the next players move
    """
    position = 0
    while position not in [1, 2, 3, 4, 5, 6, 7, 8, 9] or not space_check(board, position):
        try:
            position = int(input('Choose your next position: (1-9) '))
        except ValueError:
            print('Sorry, please enter a number.')
    return position

def replay():
    """
    Asks the player if they want to play again.
    """
    return input('Do you want to play again? Enter Yes or No. ').lower().startswith('y')

print('Welcome to Tic Tac Toe!')
while True:
    the_board = [' '] * 10
    player1_marker, player2_marker = player_input()
    turn = choose_first()
    print(turn + ' will go first.')

    game_is_on = True

    while game_is_on:
        if turn == 'Player 1':
            display_board(the_board)
            position = player_choice(the_board)
            place_marker(the_board, player1_marker, position)

            if check_win(the_board, player1_marker):
                display_board(the_board)
                print('Congratulations! You have won the game!')
                game_is_on = False
            else:
                if check_full_board(the_board):
                    display_board(the_board)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'Player 2'
        else:
            display_board(the_board)
            position = player_choice(the_board)
            place_marker(the_board, player2_marker, position)

            if check_win(the_board, player2_marker):
                display_board(the_board)
                print('Congratulations! Player 2 has won!')
                game_is_on = False
            else:
                if check_full_board(the_board):
                    display_board(the_board)
                    print('The game is a draw!')
                    break
                else:
                    turn = 'Player 1'

        if not replay():
            break