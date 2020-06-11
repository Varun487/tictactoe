import pandas as pd

all_moves = pd.read_csv('all_moves.csv')

def encoding_User_Computer_Move(user_move, computer_move, user_num, computer_num):
    User_move_encoding = pd.get_dummies(user_move, prefix='User_Move_{}_encoding'.format(user_num))
    Computer_move_encoding = pd.get_dummies(computer_move, prefix='Computer_Move_{}_encoding'.format(computer_num))

    df = pd.concat([User_move_encoding, Computer_move_encoding], axis=1, sort=False)

    return df


def training_set_User_Computer_Move_Encoding():
    y = pd.DataFrame()

    for i in range(4):
        temp = encoding_User_Computer_Move(all_moves['User_Move_{}'.format(i+1)], all_moves['Computer_Move_{}'.format(i+1)], i+1, i+1)
        #print(temp)
        y = pd.concat([y, temp], axis=1, sort=False)

    y = y.drop('Computer_Move_4_encoding_0', axis=1)
    Computer_Response_encoding = pd.get_dummies(all_moves.Computer_Response, prefix='Computer_Response_encoding')
    y = pd.concat([y, Computer_Response_encoding], axis=1, sort=False)
    y.to_csv('Training_set_User_Computer_Move_encoding.csv')

def convert_to_board_state_encoding():
    df = pd.read_csv('all_moves.csv')
    df = df.drop(['Computer_Move_4'], axis = 1)
    rows = []

    for i,j in df.iterrows():
        rows.append([j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8]])

    for index,row in enumerate(rows):
        row = list(dict.fromkeys(row).keys())

        if 0 in row:
            row.remove(0)

        print(index, row[:-1])

# training_set_User_Computer_Move_Encoding()
convert_to_board_state_encoding()
