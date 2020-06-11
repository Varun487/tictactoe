import pandas as pd

# 4 (User_move, Computer_move) pairs - one for each move - along with one computer response
# 0 is the default used for no move is made by either in that move
template = "0 0 0 0 0 0 0 0 0"

def get_first_move_data():
    first_move = open('first_move.txt', 'r')
    first_move_data = first_move.readlines()
    first_move.close()

    first_move_data = [i.split() for i in first_move_data]
    first_move_data = [i[:-1] for i in first_move_data]

    for i in first_move_data:
        while len(i) < 9:
            i.insert(1, '0')

    return first_move_data

def get_second_move_data():
    second_move = open('second_move.txt', 'r')
    second_move_data = second_move.readlines()
    second_move.close()

    second_move_data = [i.split() for i in second_move_data]
    second_move_data = [i[:-1] for i in second_move_data]

    for i in second_move_data:
        if i[0] == '5':
            i.insert(1, '1')
        else:
            i.insert(1, '5')

    for i in second_move_data:
        if i[0] == i[2]:
            second_move_data.remove(i)

    second_move_data = list(filter(lambda x: len(set(x)) == len(x), second_move_data))

    for i in second_move_data:
        while len(i) < 9:
            i.insert(3, '0')

    return second_move_data

def get_third_move_data():
    third_move = open('third_move.txt', 'r')
    third_move_data = third_move.readlines()
    third_move.close()

    third_move_data = [i.split() for i in third_move_data]
    third_move_data = [i[:-1] for i in third_move_data]

    # third_move_data = list(filter(lambda x: len(set(x)) == len(x), third_move_data))

    for i in third_move_data:
        if i[0] == '5':
            i.insert(1,'1')
        else:
            i.insert(1, '5')

    second_move_data = get_second_move_data()
    # print(second_move_data)
    # print()

    for second_move in second_move_data:
        for third_move in third_move_data:
            if (third_move[:3] == second_move[:3]):
                #print(second_move[:3], "->", third_move)
                third_move.insert(3, second_move[-1])

    third_move_data = list(filter(lambda x: len(set(x)) == len(x), third_move_data))

    for i in third_move_data:
        while len(i) < 9:
            i.insert(5, '0')

    return third_move_data

def get_fourth_move_data():
    fourth_move = open('fourth_move.txt', 'r')
    fourth_move_data = fourth_move.readlines()
    fourth_move.close()

    fourth_move_data = [i.split() for i in fourth_move_data]
    fourth_move_data = [i[:-1] for i in fourth_move_data]

    for i in fourth_move_data:
        if i[0] == '5':
            i.insert(1, '1')
        else:
            i.insert(1, '5')

    second_move_data = get_second_move_data()

    for second_move in second_move_data:
        for fourth_move in fourth_move_data:
            if (fourth_move[:3] == second_move[:3]):
                #print(second_move[:3], "->", third_move)
                fourth_move.insert(3, second_move[-1])

    third_move_data = get_third_move_data()

    for third_move in third_move_data:
        for fourth_move in fourth_move_data:
            if (fourth_move[:5] == third_move[:5]):
                #print(third_move[:5], "->", fourth_move)
                fourth_move.insert(5, third_move[-1])

    fourth_move_data = list(filter(lambda x: len(set(x)) == len(x), fourth_move_data))

    for i in fourth_move_data:
        while len(i) < 9:
            i.insert(-1, '0')

    return fourth_move_data

# for data in (get_first_move_data() + get_second_move_data() + get_third_move_data() + get_fourth_move_data()):
#     print(data)
# print()
# print()
# for data in get_fourth_move_data():
#     print(data)

df = pd.DataFrame(get_first_move_data() + get_second_move_data() + get_third_move_data() + get_fourth_move_data(),
                  columns=["User Move 1", "Computer Move 1", "User Move 2", "Computer Move 2", "User Move 3",
                           "Computer Move 3", "User Move 4", "Computer Move 4", "Computer Response"]
)
df.to_csv('all_moves.csv')
