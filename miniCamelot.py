"""
Jakub Nowak
Mini_Camelot
v 1.0.0
"""
import pygame

pygame.init()

square_width = 25
square_height = 25
square_margin = 5

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
player1Color = (0,191,255) #blue
player1SelectedColor = (135,206,235) #lighter blue
player2Color = red
goalColor = (255,223,0)
green = (173,255,47)


display_width = square_width * 8
display_height = square_height * 14

#initiate whosTurn to player 1. after eachTUrn, change players.
whosTurn = 1

#create board
board = []

for row in range(14):
    # For each row, create a list that will
    # represent an entire row
    board.append([])
    # Loop for each column
    for column in range(8):
        # Add a the number zero to the current row
        board[row].append(0)

#persist last selected player value, set first to one of the player pieces
lastSelected = (8,3)

#initiate list of squares player can move to. this will be a list of touples
moveableSquare = []

########Setup board
#if array has number 0, signify that board is open
#if array has number 3, signify that board is blocked
#if array has number 1, signify that board is occupied by player 1
#if array has number 2, signify that board is occupied by player 2 (AI)
#if array has number 4, signify that square is selected by player 1
#if array has number 5, signify that square is goal area
#if array has number 6, signify that square can be moved to

#goal areas
board[0][3] = 5
board[0][4] = 5

board[13][3] = 5
board[13][4] = 5

#unplayable area
board[0][0] = 3
board[0][1] = 3
board[0][2] = 3
board[0][5] = 3
board[0][6] = 3
board[0][7] = 3
board[1][0] = 3
board[1][1] = 3
board[1][6] = 3
board[1][7] = 3
board[2][0] = 3
board[2][7] = 3

board[13][0] = 3
board[13][1] = 3
board[13][2] = 3
board[13][5] = 3
board[13][6] = 3
board[13][7] = 3
board[12][0] = 3
board[12][1] = 3
board[12][6] = 3
board[12][7] = 3
board[11][0] = 3
board[11][7] = 3


#players
board [4][2] = 2
board [4][3] = 2
board [4][4] = 2
board [4][5] = 2
board [5][3] = 2
board [5][4] = 2

board [9][2] = 1
board [9][3] = 1
board [9][4] = 1
board [9][5] = 1
board [8][3] = 1
board [8][4] = 1


##############################
gameDisplay= pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Mini-Camelot')
clock = pygame.time.Clock()


isWinner = False

##############################
#functions

def drawFromBoard(grid):
    rowIndex = 0
    for row in grid:
        columnIndex = 0
        
        for box in row:
            #3 = unplayable region
            if(box == 3):
                pygame.draw.rect(gameDisplay,black,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            #0 = playable region
            if(box == 0):
                pygame.draw.rect(gameDisplay,white,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            #1 = occupied by player 1
            if(box == 1):
                pygame.draw.rect(gameDisplay,player1Color,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            #2 = occupied by player 2
            if(box == 2):
                pygame.draw.rect(gameDisplay,player2Color,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            if(box == 4):
                pygame.draw.rect(gameDisplay,player1SelectedColor,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            if(box == 5):
                pygame.draw.rect(gameDisplay,goalColor,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))
            if(box == 6):
                pygame.draw.rect(gameDisplay,green,(columnIndex*square_height,rowIndex* square_width,square_width,square_height))

            columnIndex += 1
        
        rowIndex += 1


def whichSquareWasClicked(coordinates):
    #do nothing
    # arrayIndex = [][]
    index_x = coordinates[0]/square_width
    index_y = coordinates[1]/square_height
    return (index_x, index_y)

#arrayIndex passed in as (x,y)
def changeSquareToColor(arrayIndex, targetValue, oldBoard):
    newBoard = oldBoard
    newBoard[arrayIndex[1]][arrayIndex[0]] = targetValue
    return newBoard

#array coordinates passed in as (y,x)
def findMoveableSquares(selectedSquare, passedBoard, turn):
    capturedPieces = []
    openMoves = []
    capturedPiecesDict = {}
    player = turn
    enemy = None
    if(player == 1):
        enemy = 2
    else:
        enemy = 1
    
    #Check all possible Moves, add possible moves to openMoves List

    #check adjacent moves
    #check up
    
    if (selectedSquare[0] >= 1 and (passedBoard[selectedSquare[0]-1][selectedSquare[1]] == 0 or passedBoard[selectedSquare[0]-1][selectedSquare[1]] == 5)):
        openMoves.append([selectedSquare[0]-1,selectedSquare[1]])
    #check down
    if (selectedSquare[0] <= 12 and (passedBoard[selectedSquare[0]+1][selectedSquare[1]] == 0 or passedBoard[selectedSquare[0]+1][selectedSquare[1]] == 5)):
        openMoves.append([selectedSquare[0]+1,selectedSquare[1]])
    #check left
    if (selectedSquare[1] >= 1 and (passedBoard[selectedSquare[0]][selectedSquare[1]-1] == 0 or passedBoard[selectedSquare[0]][selectedSquare[1]-1] == 5)):
        openMoves.append([selectedSquare[0],selectedSquare[1]-1])
    #check right
    if (selectedSquare[1] <= 6 and (passedBoard[selectedSquare[0]][selectedSquare[1]+1] == 0 or passedBoard[selectedSquare[0]][selectedSquare[1]+1] == 5)):
        openMoves.append([selectedSquare[0],selectedSquare[1]+1])
    #check up/left
    if(selectedSquare[0] >= 1 and selectedSquare[1]-1 >= 1 and (passedBoard[selectedSquare[0]-1][selectedSquare[1]-1] == 0 or passedBoard[selectedSquare[0]-1][selectedSquare[1]-1] == 5)):
        openMoves.append([selectedSquare[0]-1,selectedSquare[1]-1])
    #check up/right
    if(selectedSquare[0] >= 1 and selectedSquare[1]+1 <= 6 and (passedBoard[selectedSquare[0]-1][selectedSquare[1]+1] == 0 or passedBoard[selectedSquare[0]-1][selectedSquare[1]+1] == 5)):
        openMoves.append([selectedSquare[0]-1,selectedSquare[1]+1])
    #check down/left
    if(selectedSquare[0] <= 12 and selectedSquare[1]-1 >= 1 and (passedBoard[selectedSquare[0]+1][selectedSquare[1]-1] == 0 or passedBoard[selectedSquare[0]+1][selectedSquare[1]-1] == 5)):
        openMoves.append([selectedSquare[0]+1,selectedSquare[1]-1])
    #check down/right
    if(selectedSquare[0] <= 12 and selectedSquare[1]+1 <= 6 and (passedBoard[selectedSquare[0]+1][selectedSquare[1]+1] == 0 or passedBoard[selectedSquare[0]+1][selectedSquare[1]+1] == 5)):
        openMoves.append([selectedSquare[0]+1,selectedSquare[1]+1])

    #check jumps. If jump, add 'in between piece' to list of 'capturedPieces'

    #check up jump
    if (selectedSquare[0] >= 2 and (passedBoard[selectedSquare[0]-2][selectedSquare[1]] == 0 or passedBoard[selectedSquare[0]-2][selectedSquare[1]] == 5) and (passedBoard[selectedSquare[0]-1][selectedSquare[1]] == 2 or passedBoard[selectedSquare[0]-1][selectedSquare[1]] == 1)):
        openMoves.append([selectedSquare[0]-2,selectedSquare[1]])
        if(passedBoard[selectedSquare[0]-1][selectedSquare[1]] == enemy):
            capturedPiecesDict[str([selectedSquare[0]-1,selectedSquare[1]])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]-1,selectedSquare[1]])
    #check down jump
    if (selectedSquare[0] <= 11 and (passedBoard[selectedSquare[0]+2][selectedSquare[1]] == 0 or passedBoard[selectedSquare[0]+2][selectedSquare[1]] == 5) and (passedBoard[selectedSquare[0]+1][selectedSquare[1]] == 2 or passedBoard[selectedSquare[0]+1][selectedSquare[1]] == 1)):
        openMoves.append([selectedSquare[0]+2,selectedSquare[1]])
        if(passedBoard[selectedSquare[0]+1][selectedSquare[1]] == enemy):
            capturedPiecesDict[str([selectedSquare[0]+1,selectedSquare[1]])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]+1,selectedSquare[1]])
    #check left jump
    if (selectedSquare[1] >= 2 and (passedBoard[selectedSquare[0]][selectedSquare[1]-2] == 0 or passedBoard[selectedSquare[0]][selectedSquare[1]-2] == 5) and (passedBoard[selectedSquare[0]][selectedSquare[1]-1] == 2 or passedBoard[selectedSquare[0]][selectedSquare[1]-1] == 1)):
        openMoves.append([selectedSquare[0],selectedSquare[1]-2])
        if(passedBoard[selectedSquare[0]][selectedSquare[1]-1] == enemy):
            capturedPiecesDict[str([selectedSquare[0],selectedSquare[1]-1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0],selectedSquare[1]-1])
    #check right jump
    if (selectedSquare[1] <= 5 and (passedBoard[selectedSquare[0]][selectedSquare[1]+2] == 0 or passedBoard[selectedSquare[0]][selectedSquare[1]+2] == 5) and (passedBoard[selectedSquare[0]][selectedSquare[1]+1] == 2 or passedBoard[selectedSquare[0]][selectedSquare[1]+1] == 1)):
        openMoves.append([selectedSquare[0],selectedSquare[1]+2])
        if(passedBoard[selectedSquare[0]][selectedSquare[1]+1] == enemy):
            capturedPiecesDict[str([selectedSquare[0],selectedSquare[1]+1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0],selectedSquare[1]+1])
    #check up/left jump
    if(selectedSquare[0] >= 2 and selectedSquare[1]-1 >= 2 and (passedBoard[selectedSquare[0]-2][selectedSquare[1]-2] == 0 or passedBoard[selectedSquare[0]-2][selectedSquare[1]-2] == 5) and (passedBoard[selectedSquare[0]-1][selectedSquare[1]-1] == 2 or passedBoard[selectedSquare[0]-1][selectedSquare[1]-1] == 1)):
        openMoves.append([selectedSquare[0]-2,selectedSquare[1]-2])
        if(passedBoard[selectedSquare[0]-1][selectedSquare[1]-1] == enemy):
            capturedPiecesDict[str([selectedSquare[0]-1,selectedSquare[1]-1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]-1,selectedSquare[1]-1])
    #check up/right jump
    if(selectedSquare[0] >= 2 and selectedSquare[1]+1 <= 5 and (passedBoard[selectedSquare[0]-2][selectedSquare[1]+2] == 0 or passedBoard[selectedSquare[0]-2][selectedSquare[1]+2] == 5) and (passedBoard[selectedSquare[0]-1][selectedSquare[1]+1] == 2 or passedBoard[selectedSquare[0]-1][selectedSquare[1]+1] == 1)):
        openMoves.append([selectedSquare[0]-2,selectedSquare[1]+2])
        if(passedBoard[selectedSquare[0]-1][selectedSquare[1]+1] == enemy):
            capturedPiecesDict[str([selectedSquare[0]-1,selectedSquare[1]+1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]-1,selectedSquare[1]+1])
    #check down/left jump
    if(selectedSquare[0] <= 11 and selectedSquare[1]-1 >= 2 and (passedBoard[selectedSquare[0]+2][selectedSquare[1]-2] == 0 or passedBoard[selectedSquare[0]+2][selectedSquare[1]-2] == 5) and (passedBoard[selectedSquare[0]+1][selectedSquare[1]-1] == 2 or passedBoard[selectedSquare[0]+1][selectedSquare[1]-1] == 1)):
        openMoves.append([selectedSquare[0]+2,selectedSquare[1]-2])
        if(passedBoard[selectedSquare[0]+1][selectedSquare[1]-1] == enemy):
            capturedPiecesDict[str([selectedSquare[0]+1,selectedSquare[1]-1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]+1,selectedSquare[1]-1])
    #check down/right jump
    if(selectedSquare[0] <= 11 and selectedSquare[1]+1 <= 5 and (passedBoard[selectedSquare[0]+2][selectedSquare[1]+2] == 0 or passedBoard[selectedSquare[0]+2][selectedSquare[1]+2] == 5) and (passedBoard[selectedSquare[0]+1][selectedSquare[1]+1] == 2 or passedBoard[selectedSquare[0]+1][selectedSquare[1]+1] == 1)):
        openMoves.append([selectedSquare[0]+2,selectedSquare[1]+2])
        if(passedBoard[selectedSquare[0]+1][selectedSquare[1]+1] == enemy):
            capturedPiecesDict[str([selectedSquare[0]+1,selectedSquare[1]+1])] = len(openMoves) -1
            capturedPieces.append([selectedSquare[0]+1,selectedSquare[1]+1])


    #if there are capturePieces, force player to use those
    print 'capturePieces'
    print capturedPieces

    print 'dictionary'
    print capturedPiecesDict
    
    print 'moves'
    print openMoves
    #if the capturedPieces are enemy pieces, purge openMoves list of any moves that do NOT capture those enemy pieces
    forcedMoves = []
    for key in capturedPiecesDict:
        forcedMoves.append(openMoves[capturedPiecesDict[key]])

    if (len(forcedMoves) > 0):
        return (forcedMoves, capturedPieces)
    else:
        return (openMoves, capturedPieces)
    # return (openMoves, capturedPieces)

def cleanBoard(board):
    rowIndex = 0
    newBoard = board
    for row in board:
        columnIndex = 0
        
        for box in row:
            #3 = unplayable region
            if(box == 6):
                newBoard = changeSquareToColor([columnIndex,rowIndex],0, board)
            
            columnIndex += 1
        
        rowIndex += 1

def findAIPieces(board, player):
    pieces = []
    
    rowIndex = 0
    for row in board:
        columnIndex = 0
        
        for box in row:
            if box == player:
                pieces.append([rowIndex, columnIndex])
            
            columnIndex += 1
        
        rowIndex += 1
    return pieces

#take in old board, return new board. piece and targetMove are both coordinates passed in as (y,x)
def createNewBoard(currentBoard, piece, targetMove, turn, capturedPiece):

    newBoard = currentBoard
    if capturedPiece == None:
        #color targetMove as turn
        newBoard = changeSquareToColor((targetMove[1],targetMove[0]), turn, currentBoard)
        #color piece as white
        newBoard = changeSquareToColor((piece[1],piece[0]), 0, currentBoard)


        print targetMove

    else:
        #color targetMove as turn
        newBoard = changeSquareToColor((targetMove[1],targetMove[0]), turn, currentBoard)
        #color capturedPiece white
        newBoard = changeSquareToColor((capturedPiece[1],capturedPiece[0]), 0, currentBoard)
        #color piece as white
        newBoard = changeSquareToColor((piece[1],piece[0]), 0, currentBoard)


    return newBoard
    

def winCheck(board, currentPlayer):
    winBoxes = []
    
    #set boxes for Castle capture win condition
    if(currentPlayer == 1):
        winBoxes = [[0,3],[0,4]]
    
    else:
        winBoxes == [[13,3],[13,4]]
    
    #check to see if enemy castle istaken
    pieces = findAIPieces(board, currentPlayer)
    for piece in pieces:
        if (piece in winBoxes):
            return True
    
    #check if board is empty of enemy player pieces
    enemy = None
    if(currentPlayer == 1):
        enemy = 2
    else:
        enemy = 1
    
    if len(findAIPieces(board, enemy)) == 0:
        return True 
    
    
    #if no return before this, return false
    return False

def scoreBoard(board, player):
    print 'scoreBoard'
    
    enemy = ''
    if enemy == '1':
        nextTurn = 2
    else:
        enemy = 1

    playerNum = len(findAIPieces(board, player))
    enemyNum = len(findAIPieces(board, enemy))

    #find score for board here.



def miniMax(board, nodeLevel, myTurn, alpha, beta):
    nextTurn = ''
    if myTurn == '1':
        nextTurn = 2
    else:
        nextTurn = 1

    
    if myTurn == 1:

        aIPieces = findAIPieces(board, myTurn)
        print 'All Ai Pieces'
        print aIPieces

        for piece in aIPieces:
                print piece
                # allMoves.append(findMoveableSquares(piece, board))
                pieceMoves = findMoveableSquares(piece, board, myTurn)
                print 'All PieceMoves:'
                print pieceMoves

                for move in range(len(pieceMoves[0])):
                    newBoard = createNewBoard(board, piece, pieceMoves[0][move], myTurn)
                    nodeLevel = nodeLevel + 1
                    miniMax(newBoard, nodeLevel, nextTurn, alpha, beta)
    else:
        #Player 2 Turn
        aIPieces = findAIPieces(board, myTurn)
        print 'All Ai Pieces'
        print aIPieces

        for piece in aIPieces:
                print piece
                # allMoves.append(findMoveableSquares(piece, board))
                pieceMoves = findMoveableSquares(piece, board, myTurn)
                print 'All PieceMoves:'
                print pieceMoves

                for move in range(len(pieceMoves[0])):
                    newBoard = createNewBoard(board, piece, pieceMoves[0][move], myTurn)
                    nodeLevel = nodeLevel + 1
                    miniMax(newBoard, nodeLevel, nextTurn, alpha, beta)




#######################################################################################
while not isWinner:
    if(whosTurn == 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isWinner = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #check which square the mouseclick is in
                    arrayIndex = whichSquareWasClicked(event.pos)
                    squareStatus = board[arrayIndex[1]][arrayIndex[0]]
                    moveableSquare = []
                    capturedPieces = []
                    print'Array Index:--------------------------------------------------'
                    print arrayIndex
                    
                    #user selects their own piece
                    if squareStatus == 1:
                        #change selected square to selectedPlayer1
                        board[lastSelected[0]][lastSelected[1]] = 1
                        board = changeSquareToColor(arrayIndex, 4, board)
                        #loop through board, check every square that is green, and color it white
                        cleanBoard(board)
                        lastSelected = (arrayIndex[1],arrayIndex[0])
                        #find squares to move to. recolor them
                        response = findMoveableSquares((arrayIndex[1],arrayIndex[0]), board, whosTurn)
                        print 'moveable squares: ';
                        print response;
                        moveableSquare = response[0]
                        capturedPieces = response[1]
                        #response[0] = openMoves
                        #response[1] = capturedPieces
                        #color all openMoves green. 
                        for square in response[0]:
                            flippedAxisIndex = [square[1],square[0]]
                            board = changeSquareToColor(flippedAxisIndex, 6, board)
                    #user selects space to move to
                    if squareStatus == 6:
                        #move lastSelected to new square, paint lastSelected to white, 
                        board = changeSquareToColor(arrayIndex, 1, board)
                        board = changeSquareToColor([lastSelected[1],lastSelected[0]], 0, board)
                        
                        #if there was a jump, paint captured piece to white
                        xMovement = abs(lastSelected[1] - arrayIndex[0])
                        yMovement = abs(lastSelected[0] - arrayIndex[1])
                        if(xMovement == 2 or yMovement == 2):
                            #a jump was made, if jumped over enemy piece, paint enemy piece white
                            #figure out which piece was jumped over
                            middlePieceXIndex = arrayIndex[0]
                            middlePieceYIndex = arrayIndex[1]

                            if(xMovement == 2):
                                if(arrayIndex[0] > lastSelected[1]):
                                    middlePieceXIndex = arrayIndex[0]-1
                                else:
                                    middlePieceXIndex = arrayIndex[0]+1
                            if(yMovement == 2):
                                if(arrayIndex[1] < lastSelected[0]):
                                    middlePieceYIndex = arrayIndex[1]+1
                                else:
                                    middlePieceYIndex = arrayIndex[1]-1
                            #check to see if piece jumped over is enemy piece
                            if(board[middlePieceYIndex][middlePieceXIndex] == 2):
                                board = changeSquareToColor([middlePieceXIndex,middlePieceYIndex],0, board)

                        #cleanup after move
                        lastSelected= (arrayIndex[1],arrayIndex[0])
                        cleanBoard(board)
                        if winCheck(board, whosTurn):
                            isWinner = true
                        else:
                            whosTurn = 2
    elif whosTurn == 2:
        #run AI
        #find how many AI pieces there are on the board.
        nodeLevel = 0
        # miniMax(board,nodeLevel, whosTurn)
        

        myTurn = whosTurn
        #win condition check
        
        aIPieces = findAIPieces(board, myTurn)
        print 'All Ai Pieces'
        print aIPieces

        for piece in aIPieces:
            print piece
            # allMoves.append(findMoveableSquares(piece, board))
            pieceMoves = findMoveableSquares(piece, board, myTurn)
            print 'All PieceMoves:'
            print pieceMoves

            if len(pieceMoves[1]) == 0:
                #No forced moves, and no captured Pieces
                for move in range(len(pieceMoves[0])):
                    newBoard = createNewBoard(board, piece, pieceMoves[0][move], myTurn, None)
            else:
                #has forced jump moves, so use captured pieces
                for move in range(len(pieceMoves[0])):
                    newBoard = createNewBoard(board, piece, pieceMoves[0][move], myTurn, pieceMoves[1][move])
                



        print 'Turn Ended'
        whosTurn = 1



##########################
    
    gameDisplay.fill(white)

    drawFromBoard(board)

##########################
    pygame.display.update()
    clock.tick(30)

pygame.quit()
