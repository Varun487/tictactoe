import numpy as np
import keras

# building the model from saved weights
# load YAML and create model
yaml_file = open('model/User_Computer_move_model_weights.yaml', 'r')
model_yaml = yaml_file.read()
yaml_file.close()
model = keras.models.model_from_yaml(model_yaml)

# load weights into new model
model.load_weights("model/User_Computer_move_model_weights.h5")
print("Loaded model from disk")

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# keeping track of user and computer's moves
user_moves = []
computer_moves = []

# Symbols
user_symbol = 'XO'
computer_symbol = 'OX'

# initial board state
board = [1,2,3,4,5,6,7,8,9]

# function to draw the board
def draw_board(board):
    print("{} | {} | {} \n--|---|---\n{} | {} | {} \n--|---|---\n{} | {} | {} \n".format(board[0], board[1], board[2], board[3], board[4], board[5], board[6], board[7], board[8]))

def inter_leaf_lists(user_moves, computer_moves):
    user_moves_len = len(user_moves)
    computer_moves_len = len(computer_moves)

    moves_history = []

    for i in range(max(user_moves_len, computer_moves_len)):
        if i < user_moves_len:
            moves_history.append(user_moves[i])
        if i < computer_moves_len:
            moves_history.append(computer_moves[i])

    return moves_history

def encode(user_moves, computer_moves):
    # interleave user and computer moves to a single list
    moves_history = inter_leaf_lists(user_moves, computer_moves)

    # make the array with all moves to be encoded
    while len(moves_history) < 7:
        moves_history.append(0)

    result = []

    for i in range(len(moves_history)):
        encoding = [0 for i in range(9)]
        if i == 0:
            encoding[moves_history[i] - 1] = 1
        elif i == 1:
            while len(encoding) > 3:
                encoding.remove(0)
            if moves_history[i] == 5:
                encoding[2] = 1
            else:
                encoding[moves_history[i]] = 1
        else:
            if moves_history[i] < 5:
                encoding[moves_history[i]] = 1
            else:
                encoding[moves_history[i] - 1] = 1
        result += encoding
        # print("encoding: ", encoding)

    # print(len(result))

    return result

def predict_next_move(encoded_input):
    # running for a single input (test)
    X = np.array([encoded_input])
    y = model.predict(X)
    y = list(map(lambda num: int(round(num)), y[0]))

    return y

def decode(prediction):
    for index,i in enumerate(prediction):
        if i == 1:
            return index + 1

# prompt to decide symbols for user and computer
print()
print()
while len(user_symbol) != 1 or len(computer_symbol) != 1:
    user_symbol = input("Enter the symbol (single character) you want to play tic tac toe with: ")
    computer_symbol = input("Enter the symbol (single character) you want the AI to play tic tac toe with: ")
    if len(user_symbol) != 1 or len(computer_symbol) != 1:
        print("Please ensure the symbols are single characters!")
print()
print()

def win_tie(board):
    if board[0] == board[1] == board[2]:
        return board[0]
    elif board[3] == board[4] == board[5]:
        return board[3]
    elif board[6] == board[7] == board[8]:
        return board[6]
    elif board[0] == board[3] == board[6]:
        return board[0]
    elif board[1] == board[4] == board[7]:
        return board[1]
    elif board[2] == board[5] == board[8]:
        return board[2]
    elif board[0] == board[4] == board[8]:
        return board[0]
    elif board[2] == board[4] == board[6]:
        return board[2]

    int_count = 0
    int_index = 0

    for index,i in enumerate(board):
        if isinstance(i,int):
            int_count += 1
            int_index = index

    if int_count == 1:
        board[int_index] = user_symbol
        return 'Tie'

    return None

continue_playing = 1

# main game loop
while continue_playing:
    # draw the current board
    draw_board(board)

    # taking the user input, taking care of invalid input
    user_inp = 0

    while user_inp not in board:
        print("Please enter a number from the board above")
        try:
            user_inp = int(input("Enter your move: "))
        except:
            print('Invalid input, please try again.')

    # change board
    board[user_inp - 1] = user_symbol

    # update user moves
    user_moves.append(user_inp)

    # get the computer input
    # encode the board for input to neural network
    comp_inp = decode(predict_next_move(encode(user_moves, computer_moves)))

    # change board
    board[comp_inp - 1] = computer_symbol

    # update computer moves
    computer_moves.append(comp_inp)

    result = win_tie(board)

    if result is not None:
        continue_playing = 0
        draw_board(board)

        if result == 'Tie':
            print("THE GAME HAS TIED.")

        elif result == user_symbol:
            print("Congratulations, YOU beat the AI and have won the game!")

        elif result == computer_symbol:
            print("The AI has won!")
