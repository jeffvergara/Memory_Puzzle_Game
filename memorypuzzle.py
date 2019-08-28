# memory puzzle

import random
import pygame, sys
from pygame.locals import *


FPS = 30  # frames per second, the general speed of the program
#WINDOWWIDTH = 640  # size of window width
#WINDOWHEIGHT = 480  # size of window height
WINDOWWIDTH = 1300
WINDOWHEIGHT = 700
REVEALSPEED = 10  # Speed boxes to reveal and cover
BOXSIZE = 150  # width and height of the box
GAPSIZE = 20  # gap between boxes pixels
BOARDWIDTH = 6 # number of column of icons
BOARDHEIGHT = 4  # number of rows of icon

assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, "BOARD NEEDS TO HAVE AN EVEN number of boxes for pairs of matches."  # Assertions are simply boolean expressions that
# checks if the conditions return true or not.
# If it is true, the program does nothing and
# move to the next line of code. However, if it's
# false, the program stops and throws an error.

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

# color of RGB

GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamonds"
LINES = "lines"
OVAL = "oval"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)

assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is to big for the number of shapes/colors defined"


def main():
    global FPSCLOCK, DISPLAYSURF

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0  # used to store x coordinate of mouse event
    mousey = 0  # used to store y coordinate of mouse event
    pygame.display.set_caption("Jumble Memory Game")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None  # stores the (x,y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:  # game main loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)  # drawing the window
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():  # event handling loop

            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):

                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        if boxx != None and boxy != None:
            # the mouse is currently over a box.

            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)

            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # set the box as "reveal"

                if firstSelection == None:  # the current box was the first box clicked
                    firstSelection = (boxx, boxy)

                else:  # the current box was the second box clicked
                       # check if there is a match between the two icons. 

                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
# sapcing can also caused: ==UnboundLocalError: local variable 'x' referenced before assignment==
                    if icon1shape != icon2shape or icon1color != icon2color:

                    #print("error")
                    # icon don't match. Re-cover up both selections.
                        pygame.time.wait(1000)  # 1000 milisecond = 1 sec
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                        #continue
                    
                    elif hasWon(revealedBoxes):  # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                    # reset the board

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                    # show the fully unreealed board for a second.
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                    # replay the start game animation.
                        startGameAnimation(mainBoard)
                    firstSelection = None  # reset firstSelection variable

        # Redraw the screen and wait a clock tick.
    pygame.display.update()

    pygame.mixer.music.load("mi3.wav")
    pygame.mixer.music.play(-1 , 0, 0)
    FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []

    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)

    return revealedBoxes


def getRandomizedBoard():
    # get a list of every possible shape in every possible color.

    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape, color))

    random.shuffle(icons)  # randomize the order of the icon list
    numIconUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # calculate how many icons are needed

    icons = icons[:numIconUsed] * 2  # make two icons each
    random.shuffle(icons)

    # create the board data stracture, with randomly placed icons.

    board = []

    for x in range(BOARDWIDTH):
        column = []

        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]  # remove the icons as we assign them

        board.append(column)

    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.

    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])

    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Converting board coordiantes to pixel coordinates

    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN

    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN

    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)

            if boxRect.collidepoint(x, y):
                return (boxx, boxy)

    return (None, None)


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)  # syntactic sugar
    half = int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy)  # get pixel coords to board coords

    # draw the shape

    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)

    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))

    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half),
                                                 (left + half, top + BOXSIZE - 1), (left, top + half)))

    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):

            pygame.draw.line(DISPLAYSURF, color,(left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color,(left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + 1))

    elif shape == OVAL:

        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    # shape value for x,y spot stored in board [x] [y] [0]

    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCover(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.

    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))

        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])

        if coverage > 0:  # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))

    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "boxreavel" animation.

    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, - REVEALSPEED):
        drawBoxCover(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCover(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # draw all of the boxes in their covered or revealed state:

    for boxx in range(BOARDWIDTH):

        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)

            if not revealed[boxx][boxy]:
                # draw a covered box
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))

            else:
                # draw the (revealed) icon.
                shape,color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape,color,boxx,boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # randomly reveal the boxes 8 at a time
    coverBoxes = generateRevealedBoxesData(False)
    boxes = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))

    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coverBoxes)

    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won

    coveredBoxes = generateRevealedBoxesData(True)

    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1  # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)

        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealBoxes):
    # Return True if all the boxes have been revealed, otherwise False
    for i in revealBoxes:

        if False in i:
            return False  # return False if any boxes are covered.

    return True


if __name__ == '__main__':
    main()
