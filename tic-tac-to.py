import tkinter as tk
from tkinter import messagebox
import math

nSize = 4
playerElement = 'X'
board = [[None for _ in range(nSize)] for _ in range(nSize)]
buttons = []

def moveFunc(i, j):
    global playerElement
    if board[i][j] is None:
        board[i][j] = playerElement
        buttons[i][j].config(text=playerElement)
        if checkDraw():
            scores = calculateScore()
            winner = "X" if scores['X'] > scores['O'] else "O" if scores['O'] > scores['X'] else "مساوی"
            messagebox.showinfo("پایان بازی", f"برنده: {winner}\nامتیازات: X = {scores['X']}, O = {scores['O']}")
            restartGame()
        else:
            playerElement = 'O' if playerElement == 'X' else 'X'
            if playerElement == 'O':
                root.after(500, aiMoveFunc)

def aiMoveFunc():
    global playerElement
    bestScore = -math.inf
    bestMove = None
    for i in range(nSize):
        for j in range(nSize):
            if board[i][j] is None:
                board[i][j] = 'O'
                score = minimaxAlgFunc(False, 0)
                board[i][j] = None
                if score > bestScore:
                    bestScore = score
                    bestMove = (i, j)
    if bestMove:
        moveFunc(*bestMove)

def minimaxAlgFunc(checkMaximizing, depth):
    scores = calculateScore()
    if checkDraw():
        return scores['O'] - scores['X']
    if depth >= 3:
        return scores['O'] - scores['X']
    if checkMaximizing:
        bestScore = -math.inf
        for i in range(nSize):
            for j in range(nSize):
                if board[i][j] is None:
                    board[i][j] = 'O'
                    score = minimaxAlgFunc(False, depth + 1)
                    board[i][j] = None
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = math.inf
        for i in range(nSize):
            for j in range(nSize):
                if board[i][j] is None:
                    board[i][j] = 'X'
                    score = minimaxAlgFunc(True, depth + 1)
                    board[i][j] = None
                    bestScore = min(score, bestScore)
        return bestScore

def calculateScore():
    scores = {'X': 0, 'O': 0}
    for i in range(nSize):
        row = board[i]
        col = [board[j][i] for j in range(nSize)]
        for line in [row, col]:
            scores = newScores(line, scores)
    main_diag = [board[i][i] for i in range(nSize)]
    anti_diag = [board[i][nSize - i - 1] for i in range(nSize)]
    for diag in [main_diag, anti_diag]:
        scores = newScores(diag, scores)
    return scores

def newScores(line, scores):
    xNum = 0
    oNum = 0
    for item in line:
        if item == 'X':
            xNum += 1
            if oNum > 1:
                scores['O'] += oNum - 2
                if oNum > 3:
                    scores['O'] += oNum - 3
            oNum = 0
        elif item == 'O':
            oNum += 1
            if xNum > 1:
                scores['X'] += xNum - 2
                if xNum > 3:
                    scores['X'] += xNum - 3
            xNum = 0
        else:
            if xNum > 1:
                scores['X'] += xNum - 2
                if xNum > 3:
                    scores['X'] += xNum - 3
            if oNum > 1:
                scores['O'] += oNum - 2
                if oNum > 3:
                    scores['O'] += oNum - 3
            xNum = 0
            oNum = 0
    if xNum > 1:
        scores['X'] += xNum - 2
        if xNum > 3:
            scores['X'] += xNum - 3
    if oNum > 1:
        scores['O'] += oNum - 2
        if oNum > 3:
            scores['O'] += oNum - 3
    return scores

def checkDraw():
    for row in board:
        for item in row:
            if item is None:
                return False
    return True

def restartGame():
    global playerElement
    global board
    board = [[None for _ in range(nSize)] for _ in range(nSize)]
    for i in range(nSize):
        for j in range(nSize):
            buttons[i][j].config(text='')
    playerElement = 'X'

def createWidgets():
    global buttons
    root.title("Tic-Tac-To")
    buttons = []
    for i in range(nSize):
        row = []
        for j in range(nSize):
            button = tk.Button(root, text='', font=('Arial', 16), height=2, width=4, command=createCommand(i, j))
            button.grid(row=i, column=j)
            row.append(button)
        buttons.append(row)
    reset_button = tk.Button(root, text="شروع مجدد", command=restartGame)
    reset_button.grid(row=nSize, column=0, columnspan=nSize)

def createCommand(i, j):
    def buttonCommand():
        moveFunc(i, j)
    return buttonCommand

if __name__ == "__main__":
    root = tk.Tk()
    createWidgets()
    root.mainloop()