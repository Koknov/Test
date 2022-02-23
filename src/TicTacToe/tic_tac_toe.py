import random
import numpy as np


# Проверка вертикальных и горизонтальных линий в квадратном подполе,
# сторона которого равняется количеству символов для победы
def checkLanes(field, char):
    for i in range(field.shape[0]):
        winCols, winRows = True, True
        for j in range(field.shape[1]):
            winCols = winCols and (field[i][j] == char)
            winRows = winRows and (field[j][i] == char)
        if winCols or winRows:
            return True
    return False


# Проверка диагоналей в квадратном подполе,
# сторона которого равняется количеству символов для победы
def checkDiag(field, char, size):
    winToRight, winToLeft = True, True
    for i in range(field.shape[1]):
        winToRight = winToRight and (field[i][i] == char)
        winToLeft = winToLeft and (field[size - i - 1][i] == char)
    return winToRight or winToLeft


# Проверка поля на наличие выигрышных ситуаций
def checkWin(field, char, rows, cols, size):
    for i in range(rows - size + 1):
        for j in range(cols - size + 1):
            if checkLanes(field[i: i + size, j: j + size], char) \
                    or checkDiag(field[i: i + size, j: j + size], char, size):
                return True
    return False


# Отрисовка поля
def drawField(field):
    print("---------")
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            print("|" + str(field[i][j]) + "|", end="")
        print("")
    print("---------")


def computerMove(cols, rows, size):
    win = False
    firstPlayer = True
    field = [[" "] * cols for _ in range(rows)]
    field = np.array(field)
    moveHistory = [_ for _ in range(cols * rows)]
    while not win:
        try:
            move = random.choice(moveHistory)
        except IndexError:
            print("Ничья")
            return
        moveHistory.remove(move)
        field[move // col][move % col] = "X" if firstPlayer else "O"
        firstPlayer = not firstPlayer
        drawField(field)
        win = checkWin(field, field[move // col][move % col], rows, cols, size)
    print(field.tolist())
    out = "2" if firstPlayer else "1"
    print("Выиграл игрок " + out)


if __name__ == '__main__':
    col = 5  # Количество столбцов поля
    row = 4  # Количество строк поля
    sizeToWin = 4   # Количество подряд идущих крестиков/ноликов для победы

    # Если размеры поля и количество символов для победы должны задаваться из консоли
    # while True:
    #     try:
    #         col = int(input("Введите количество столбцов: "))
    #         row = int(input("Введите количество строк: "))
    #         sizeToWin = int(input("Введите количество подряд идущих крестиков/ноликов, необходимых для победы: "))
    #         if sizeToWin > col or sizeToWin > row:
    #             print("Количество подряд идущих крестиков/ноликов для победы не должно превышать "
    #                   "количество строк или стобцов")
    #             continue
    #         break
    #     except ValueError:
    #         print("Некорректный ввод. Введите число")
    #         continue

    computerMove(col, row, sizeToWin)
