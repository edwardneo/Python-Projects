import pygame

screenWidth = 800
screenHeight = 900
screenMargin = 10
gridWidth = (screenWidth-2*screenMargin)/3
upperBar = screenHeight-screenWidth
iconMargin = 5
lineWidth = 1
counter = 0
coordinates = []
XCoordinates = []
OCoordinates = []

pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False
color = (255, 255, 255)

for i in range(1, 4):
    for j in range(1, 4):
        coordinates.append((i, j))

def drawGrid():
    pygame.draw.line(screen, color, (gridWidth+screenMargin, upperBar+screenMargin), (gridWidth+screenMargin, screenHeight-screenMargin), lineWidth)
    pygame.draw.line(screen, color, (2*gridWidth+screenMargin, upperBar+screenMargin), (2*gridWidth+screenMargin, screenHeight-screenMargin), lineWidth)
    pygame.draw.line(screen, color, (screenMargin, upperBar+gridWidth+screenMargin), (screenWidth-screenMargin, upperBar+gridWidth+screenMargin), lineWidth)
    pygame.draw.line(screen, color, (screenMargin, upperBar+2*gridWidth+screenMargin), (screenWidth-screenMargin, upperBar+2*gridWidth+screenMargin), lineWidth)

def drawCross(row, column):
    posx = (column-1)*gridWidth+screenMargin+iconMargin
    posy = upperBar+(row-1)*gridWidth+screenMargin+iconMargin
    pygame.draw.line(screen, color, (posx, posy), (posx+gridWidth-2*iconMargin, posy+gridWidth-2*iconMargin), lineWidth)
    pygame.draw.line(screen, color, (posx+gridWidth-2*iconMargin, posy), (posx, posy+gridWidth-2*iconMargin), lineWidth)

def drawCircle(row, column):
    pygame.draw.circle(screen, color, (int((column-1)*gridWidth+screenMargin+gridWidth/2), int(upperBar+(row-1)*gridWidth+screenMargin+gridWidth/2)), int(gridWidth/2-screenMargin), lineWidth)

def hasWon(places):
    rows = [0, 0, 0]
    columns = [0, 0, 0]
    diagonals = [0, 0]
    for coordinate in places:
        rows[coordinate[0]-1] += 1
        columns[coordinate[1]-1] += 1
        if coordinate in [(1, 1), (2, 2), (3, 3)]:
            diagonals[0] += 1
        if coordinate in [(1, 3), (2, 2), (3, 1)]:
            diagonals[1] += 1
    if 3 in rows + columns + diagonals:
        return True
    else:
        return False

while not done:
    drawGrid()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                row = int((position[1]-upperBar)/gridWidth) + 1
                column = int(position[0]/gridWidth) + 1
                if (row, column) in coordinates:
                    if counter%2 == 0:
                        drawCross(row, column)
                        XCoordinates.append((row, column))
                        if hasWon(XCoordinates):
                            print("X has won.")
                            done = True
                    else:
                        drawCircle(row, column)
                        OCoordinates.append((row, column))
                        if hasWon(OCoordinates):
                            print("O has won.")
                            done = True
                    coordinates.remove((row, column))

                    counter += 1

    pygame.display.flip()
