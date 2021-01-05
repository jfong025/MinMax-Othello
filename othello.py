import turtle
import functools
import random
from copy import deepcopy
import time

s = turtle.Screen()
t = turtle.Turtle()
s.bgcolor('forest green')
s.setup(600,600)
gameBoard = []
Turn = 'black'
gameOver = False



def drawBoard(n):
    s.tracer(0, 0)

    t.penup()
    t.goto(-200,200)
    t.setheading(0)
    for z in list(range(n+1)):
        for j in list(range(n)):
            t.pendown()
            t.forward(50)
        t.penup()
        t.goto(-200,200 - (50 * (z+1)))
    t.penup()
    t.goto(-200, 200)
    for i in list(range(n+1)):
        for b in list(range(n)):
            t.pendown()
            t.setheading(-90)
            t.forward(50)
        t.penup()
        t.goto(-200 + (50 * (i+1)),200)
    s.tracer(1, 0)

def whichRow(y):
   return (int((200-y)/50))

def whichColumn(x):
   return (int((200+x)/50))

def xFromColumn(column):
    return -175 + (column*50)

def yFromRow(row):
    return 175 - (row * 50)
def stampPlayer(row,column,player):
    s.tracer(0,0)
    t.penup()
    t.goto(xFromColumn(column),yFromRow(row))
    t.shape('circle')
    t.shapesize(2,2)
    t.color(player)
    t.stamp()
    s.tracer(1,0)

def updateBoard(board, player,row,col):
    board[row][col]= player
    return board
def updateScore(player):
    whiteScore =calculateScore(gameBoard,'black')
    blackScore =calculateScore(gameBoard, 'white')
def calculateScore(board, player):
    return functools.reduce(lambda x,y: x+y ,[len([v for v in row if v == player])for row in board])
def initialize():
    global gameBoard
    gameBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]]
    gameBoard[3][3] = 'white'
    gameBoard[3][4] = 'black'
    gameBoard[4][4] = 'white'
    gameBoard[4][3] = 'black'
    flatten = lambda l: [item for sublist in l for item in sublist]
    t.clear()
    t.clearstamps()
    drawBoard(8)
    stampPlayer(-1, 7, 'white')
    t.goto(xFromColumn(7), yFromRow(-1))
    t.color('black')
    t.write(len(list(filter(lambda x: x == 'white', flatten(gameBoard)))), False, align="center",
            font=("Arial", 25, "normal"))
    stampPlayer(-1, 0, 'black')
    t.goto(xFromColumn(0), yFromRow(-1))
    t.color('white')
    t.write(len(list(filter(lambda x: x == 'black', flatten(gameBoard)))), False, align="center",
            font=("Arial", 25, "normal"))
    for i in list(range(8)):
        for j in list(range(8)):
            if gameBoard[i][j] != 0:
                stampPlayer(i, j, gameBoard[i][j])

def allMoves(board,player):
    moves = []
    for i in range(0,8):
        for j in range (0,8):
            if validMove(board, player, i, j) and board[i][j] == 0:
                moves.append([i,j])
    return moves

def itemOf(board,row,column,player):
    if row > 7 or row < 0 or column < 0 or column > 7:
        return 'x'
    else:
        if board[row][column] == player:
            return True
        return False

def validMove(board,player,row,column):
    movecopy= [itemOf(board,row,column+1,player), itemOf(board,row,column-1,player),itemOf(board,row+1,column,player),
             itemOf(board,row-1,column,player),itemOf(board,row+1,column+1,player), itemOf(board,row-1,column-1,player),
             itemOf(board, row+1, column - 1,player), itemOf(board,row-1,column+1,player)]

    possiblemoves= [vector(board,[0,7],row,column,player), vector(board,[0,-7],row,column,player),vector(board,[7,0],row,column,player),
                    vector(board,[-7,0],row,column,player),vector(board,[7,7],row,column,player), vector(board,[-7,-7],row,column,player),
                    vector(board,[7,-7],row,column,player), vector(board,[-7,7],row,column,player)]
    results=[]
    for i in list(range(len(movecopy))):
        if movecopy[i] != True and movecopy[i] != 'x':
            results += [possiblemoves[i]]
    if True in results:
        return True
    else:
        return False

def vector(board,vect,row,col,player):
    row = round(row)
    col = round(col)
    if row > 7 or row < 0 or col < 0 or col > 7:
        return 'x'
    if board[row][col] == player:
        if 7 in vect or -7 in vect:
            return False
        return True
    if board[row][col] == 0:
        if 7 not in vect and -7 not in vect:
            return 'x'
    if vect == [0,0]:
        return False
    if vect[0] == 0:
        return vector(board, [vect[0],round(vect[1] + -1*(vect[1]/abs(vect[1])))],row,col+(vect[1]/abs(vect[1])),player)
    if vect[1]== 0:
        return vector(board, [round(vect[0] + -1 * (vect[0] / abs(vect[0]))), vect[1]], row + (vect[0] / abs(vect[0])), col,player)
    else:
        return vector(board,[round(vect[0] + -1 * (vect[0] / abs(vect[0]))),round(vect[1] + -1*(vect[1]/abs(vect[1])))],row+(vect[0]/abs(vect[0])),col+(vect[1]/abs(vect[1])),player)

def nextBoard(board,player,move):
    currentboard = deepcopy(board)


    possiblemoves = [[vector(board, [0,7],move[0],move[1], player),[0, 7]],[vector(board, [0, -7], move[0],move[1], player),[0, -7]],
                     [vector(board, [7, 0], move[0], move[1], player),[7, 0]],
                     [vector(board, [-7, 0], move[0], move[1], player),[-7, 0]], [vector(board, [7, 7], move[0],move[1], player),[7, 7]],
                     [vector(board, [-7, -7], move[0], move[1], player),[-7, -7]],
                     [vector(board, [7, -7], move[0], move[1], player),[7, -7]], [vector(board, [-7, 7], move[0],move[1], player),[-7, 7]]]
    moves = [x[1] for x in possiblemoves if x[0]==True]
    for i in list(range(len(moves))):
        currentboard = vectorChange(currentboard,moves[i],move[0],move[1],player)
    currentboard[move[0]][move[1]] = player
    return currentboard

def vectorChange(board,vect,row,col,player):
    row = round(row)
    col = round(col)
    if row > 7 or row < 0 or col < 0 or col > 7:
        return 'x'
    if board[row][col] == player:
        if 7 in vect or -7 in vect:
            return False
        return board
    if board[row][col] == 0:
        if 7 not in vect and -7 not in vect:
            return 'x'
    if board[row][col] != player and board[row][col] != 0:
        if player == 'white':
            board[row][col] = 'white'
        if player == 'black':
            board[row][col] = 'black'
    if vect == [0,0]:
        return False
    if vect[0] == 0:
        return vectorChange(board, [vect[0],round(vect[1] + -1*(vect[1]/abs(vect[1])))],row,col+(vect[1]/abs(vect[1])),player)
    if vect[1] == 0:
        return vectorChange(board, [round(vect[0] + -1 * (vect[0] / abs(vect[0]))), vect[1]], row + (vect[0] / abs(vect[0])), col,player)
    else:
        return vectorChange(board,[round(vect[0] + -1 * (vect[0] / abs(vect[0]))),round(vect[1] + -1*(vect[1]/abs(vect[1])))],row+(vect[0]/abs(vect[0])),col+(vect[1]/abs(vect[1])),player)

def startBGame(p1,p2):
    whitedepth=p1
    blackdepth=p2
    global gameBoard
    flatten = lambda l: [item for sublist in l for item in sublist]
    initialize()
    while gameOver == False:
        global Turn
        boardcheck = flatten(gameBoard)
        if 0 not in boardcheck or 'black' not in boardcheck or 'white' not in boardcheck:
            break
        if allMoves(gameBoard,Turn) != []:
            if gameOver == False:
                if Turn == 'white':
                    #s=time.time()
                    move = minimax(gameBoard,whitedepth,'white')
                    #print(time.time()-s)
                    makemove(move[0], move[1])
                else:
                    # randommove = allMoves(gameBoard, Turn)[random.randint(0, len(allMoves(gameBoard, Turn)) - 1)]
                    # makemove(randommove[0], randommove[1])
                    move = minimax(gameBoard,blackdepth,'black')
                    makemove(move[0], move[1])
        else:
            nextTurn = (lambda x: 'white' if x == 'black' else 'black')
            if allMoves(gameBoard, Turn) == [] and allMoves(gameBoard, nextTurn(Turn)) == []:
                break
        t.clear()
        t.clearstamps()
        drawBoard(8)
        stampPlayer(-1, 7, 'white')
        t.goto(xFromColumn(7), yFromRow(-1))
        t.color('black')
        t.write(len(list(filter(lambda x: x == 'white', flatten(gameBoard)))), False, align="center", font=("Arial", 25, "normal"))
        stampPlayer(-1, 0, 'black')
        t.goto(xFromColumn(0), yFromRow(-1))
        t.color('white')
        t.write(len(list(filter(lambda x: x == 'black', flatten(gameBoard)))), False, align="center", font=("Arial", 25, "normal"))
        for i in list(range(8)):
            for j in list(range(8)):
                if gameBoard[i][j] != 0:
                    stampPlayer(i, j, gameBoard[i][j])

def startPGame(cpuDepth):
    global gameBoard
    flatten = lambda l: [item for sublist in l for item in sublist]
    initialize()
    while gameOver == False:
        global Turn
        check = flatten(gameBoard)
        if 0 not in check or 'black' not in check or 'white' not in check:
            break
        if allMoves(gameBoard, Turn) != []:
            if gameOver == False:
                if Turn == 'white':
                    move = minimaxjustin(gameBoard, cpuDepth, 'white')
                    makemove(move[0], move[1])
                else:
                    move1 = input('Row?')
                    move2 = input('Col?')
                    makemove(move1, move2)
        else:
            nextTurn = (lambda x: 'white' if x == 'black' else 'black')
            if allMoves(gameBoard, Turn) == [] and allMoves(gameBoard, nextTurn(Turn)) == []:
                break
            Turn = nextTurn(Turn)
        t.clear()
        t.clearstamps()
        drawBoard(8)
        stampPlayer(-1, 7, 'white')
        t.goto(xFromColumn(7), yFromRow(-1))
        t.color('black')
        t.write(len(list(filter(lambda x: x == 'white', flatten(gameBoard)))), False, align="center",
                font=("Arial", 25, "normal"))
        stampPlayer(-1, 0, 'black')
        t.goto(xFromColumn(0), yFromRow(-1))
        t.color('white')
        t.write(len(list(filter(lambda x: x == 'black', flatten(gameBoard)))), False, align="center",
                font=("Arial", 25, "normal"))
        for i in list(range(8)):
            for j in list(range(8)):
                if gameBoard[i][j] != 0:
                    stampPlayer(i, j, gameBoard[i][j])


def printboard():
    flatten = lambda l: [item for sublist in l for item in sublist]
    t.clear()
    t.clearstamps()
    drawBoard(8)
    stampPlayer(-1, 7, 'white')
    t.goto(xFromColumn(7), yFromRow(-1)-10)
    t.color('black')
    t.write(len(list(filter(lambda x: x == 'white', flatten(gameBoard)))), False, align="center",
            font=("Arial", 25, "normal"))
    stampPlayer(-1, 0, 'black')
    t.goto(xFromColumn(0), yFromRow(-1)-10)
    t.color('white')
    t.write(len(list(filter(lambda x: x == 'black', flatten(gameBoard)))), False, align="center",
            font=("Arial", 25, "normal"))
    for i in list(range(8)):
        for j in list(range(8)):
            if gameBoard[i][j] != 0:
                stampPlayer(i, j, gameBoard[i][j])


def playerclick(x, y):
    t.onclick(playerclick)
    row = whichRow(y)
    col = whichColumn(x)
    if [whichRow(y),whichColumn(x)] in allMoves(gameBoard, Turn):
       makemove(row,col)

def main():
    mode = input("What mode would you like to play? (type 'b' for CPU VS. CPU or type 'p' for Player vs. CPU")
    if mode == 'b' or mode == 'p':
        if mode == 'b':
            p1 = int(input("How deep should player 1 go? (1-10)"))
            p2 = int(input("How deep should player 2 go? (1-10)"))
            startBGame(p1, p2)
        if mode == 'p':
            cpuDepth = input("How deep should the bot go? (1-10)")
            startPGame(cpuDepth)

def makemove(row,col):
    global gameBoard
    global Turn
    if [row,col] in allMoves(gameBoard, Turn):
        gameBoard = nextBoard(gameBoard, Turn,[row,col])
    printboard()
    nextTurn = (lambda x: 'white' if x == 'black' else 'black')
    Turn = nextTurn(Turn)

def eval_function(board,player):
    p_tiles = 0
    opp_tiles = 0
    scr = 0
    cor = 0

    #Disc Positioning and Frontier Disks

    for i in list(range(8)):
        for j in list(range(8)):
            if board[i][j] == player:
                p_tiles += 1
            if board[i][j] != player and board[i][j]!= 0:
                opp_tiles += 1

    if p_tiles != opp_tiles:
        scr = (100 * (p_tiles-opp_tiles))/(p_tiles+opp_tiles)
    if player == 'white':
        p_tiles = 0
        opp_tiles = 0
        if board[0][0] == player:
            p_tiles +=1
        if board[0][0] != player and board[0][0] != 0:
            opp_tiles += 1
        if board[0][7] == player:
            p_tiles+= 1
        if board[0][7] != player and board[0][7] != 0:
            opp_tiles+= 1
        if board[7][0] == player:
            p_tiles += 1
        if board[7][0] != player and board[7][0] != 0:
            opp_tiles += 1
        if board[7][7] == player:
            p_tiles+= 1
        if board[7][7] != player and board[7][7] != 0:
            opp_tiles+= 1
        cor = 5 * (p_tiles-opp_tiles)
    nextTurn = (lambda x: 'white' if x == 'black' else 'black')
    mob = 2 * len(allMoves(board,player))
    oppmob = -1 * len(allMoves(board,nextTurn(player)))
    flatten = lambda l: [item for sublist in l for item in sublist]

    if len([x for x in flatten(board) if x !=0]) > 53:
       score = (200.0 * cor) + (250 * scr) + (1200 * mob)
    else:
        score =  (500.5 * cor) + (15 * scr) + (5000 * mob)
    return score

def minimax(board,depth,player):
    nextMoves = allMoves(board, player)
    if len(nextMoves) == 1:
        return nextMoves[0]
    board = deepcopy(board)
    if depth == 0:
        return board
    alpha = -100000000000000000000
    beta = 100000000000000000000
    allBranches = [maxplayer(board, n, depth, player, alpha, beta) for n in nextMoves]
    maxvalue = max(allBranches)
    return nextMoves[allBranches.index(maxvalue)]


def maxplayer(board,move,depth,player,alpha,beta):
    nextTurn = (lambda x: 'white' if x == 'black' else 'black')
    newboard = deepcopy(nextBoard(board,player, move))
    if depth == 0 or allMoves(newboard, nextTurn(player)) == []:
        return eval_function(newboard, player)
    z = alpha
    for i in range(len(allMoves(newboard,nextTurn(player)))):
        x = minopp(newboard, allMoves(newboard, nextTurn(player))[i], depth-1, nextTurn(player), z, beta)
        if x > z: z = x
        if z > beta: return beta
    return z

def minopp(board, move, depth, player, alpha, beta):
    nextTurn = (lambda x: 'white' if x == 'black' else 'black')
    newboard = deepcopy(nextBoard(board, player, move))
    if depth == 0 or allMoves(newboard,nextTurn(player)) == []:
        return eval_function(board, player)
    z = beta
    for i in range(len(allMoves(newboard,nextTurn(player)))):
        x = maxplayer(newboard, allMoves(newboard, nextTurn(player))[i], depth-1, nextTurn(player), alpha, z)
        if x > z : z = x
        if z > alpha: return alpha
    return z
initialize()
main()