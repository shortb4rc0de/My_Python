TicTacToe = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]   # Массив, который отвечает за положение крестиков и ноликов

print('Здравствуйте! Вы можете сыграть в игру крсетики-нолики.'
      'Ходить нужно по очереди, сначала ходит первый игрок,'
      'потом второй.\nКрестик - первый игрок, нолик - второй. '
      'Чтобы поставить символ в нужную вам клетку,'
      'Введите номер стобца [1 - 3] и строки [1 - 3]. Приятной игры!\n ')


def moves(string, col, mas, turn):  # Функция, меняющая значения в массиве, на основе ходов игрков
    string -= 1
    col -= 1
    if turn == 2:
        mas[string][col] = 'O'
    else:
        mas[string][col] = 'X'

    return mas


def win(mas):  # Функция, проверяющая, является ли нынешнее положение выигрышным
    if mas[0][0] == mas[0][1] == mas[0][2] and mas[0][0] != 0 and mas[0][1] != 0 and mas[0][2] != 0:
        return False
    if mas[1][0] == mas[1][1] == mas[1][2] and mas[1][0] != 0 and mas[1][1] != 0 and mas[1][2] != 0:
        return False
    if mas[2][0] == mas[2][1] == mas[2][2] and mas[2][0] != 0 and mas[2][1] != 0 and mas[2][2] != 0:
        return False
    if mas[0][0] == mas[1][0] == mas[2][0] and mas[0][0] != 0 and mas[1][0] != 0 and mas[2][0] != 0:
        return False
    if mas[0][1] == mas[1][1] == mas[2][1] and mas[0][1] != 0 and mas[1][1] != 0 and mas[2][1] != 0:
        return False
    if mas[0][2] == mas[1][2] == mas[2][2] and mas[0][2] != 0 and mas[1][2] != 0 and mas[2][2] != 0:
        return False
    if mas[0][0] == mas[1][1] == mas[2][2] and mas[0][0] != 0 and mas[1][1] != 0 and mas[2][2] != 0:
        return False
    if mas[0][2] == mas[1][1] == mas[2][0] and mas[0][2] != 0 and mas[1][1] != 0 and mas[2][0] != 0:
        return False
    return True


boo = True
player_control = 1
for i in range(3):
    print(*TicTacToe[i][:3])

while boo:  # Основное тело программы
    try:
        print(f'Игрок № {player_control}, введите номер строки: ')
        stroka = int(input())

        print(f'Игрок № {player_control}, введите номер столбца: ')
        stolbec = int(input())

        if 1 <= stroka <= 3 and 1 <= stolbec <= 3:
            if TicTacToe[stroka - 1][stolbec - 1] == 0:
                TicTacToe = moves(stroka, stolbec, TicTacToe, player_control)

                for i in range(3):
                    print(*TicTacToe[i][:3])

                boo = win(TicTacToe)

                if player_control % 2 == 1:
                    player_control += 1
                else:
                    player_control -= 1

                count_zero = 0
                for i in range(3):
                    for j in range(3):
                        if TicTacToe[i][j] == 0:
                            count_zero += 1
                if count_zero == 0:
                    boo = False
            else:
                print('Эта клетка занята!')
        else:
            print('Неправильный номер строки или столбца, проверьте данные')
    except ValueError:
        print('Введите число')


if __name__ == '__main__':
    if count_zero != 0 or win(TicTacToe) is False:
        print(f'Игрок № {player_control + 1 if player_control == 1 else player_control - 1} победил!')
    else:
        print('Ничья')
