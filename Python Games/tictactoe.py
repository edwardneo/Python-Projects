import pygame
import math

def shaded(color):
    shadeFactor = 0.3
    return (color[0]*(1-shadeFactor), color[1]*(1-shadeFactor), color[2]*(1-shadeFactor))

class Button():
    def __init__(self, centerX, centerY, width, height, buttonColor, text, font, fontSize, textColor):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.buttonColor = buttonColor

        self.XBounds = (self.centerX-self.width//2, self.centerX+self.width//2)
        self.YBounds = (self.centerY-self.height//2, self.centerY+self.height//2)

        self.text = text
        self.font = font
        self.fontSize = fontSize
        self.textColor = textColor

        self.drawButton()

    def drawButton(self, color=None):
        if color == None:
            color = self.buttonColor

        pygame.draw.rect(pygame.display.get_surface(), color, pygame.Rect(self.XBounds[0], self.YBounds[0], self.width, self.height))

        text = pygame.font.SysFont(self.font, self.fontSize).render(self.text, True, self.textColor)
        pygame.display.get_surface().blit(text, (self.centerX-text.get_width()//2, self.centerY-text.get_height()//2))

    def withinBounds(self, coordinates):
        return self.XBounds[0] <= coordinates[0] and coordinates[0] <= self.XBounds[1] and self.YBounds[0] <= coordinates[1] and coordinates[1] <= self.YBounds[1]
    def holdDown(self):
        self.drawButton(shaded(self.buttonColor))

class Interface:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 900

        self.text = "Tic-Tac-Toe"
        self.font = "comicsansms"
        self.fontSize = 128
        self.textColor = (0, 255, 0)
        self.textX = self.screenWidth//2
        self.textY = self.screenHeight//3

        self.buttonMargin = 20

        self.onePlayerX = self.screenWidth//4
        self.onePlayerY = 2*self.screenHeight//3
        self.onePlayerColor = (0, 255, 255)
        self.onePlayerText = "One Player"
        self.onePlayerTextColor = (0, 0, 0)

        self.twoPlayerX = 3*self.screenWidth//4
        self.twoPlayerY = 2*self.screenHeight//3
        self.twoPlayerColor = (0, 255, 255)
        self.twoPlayerText = "Two Player"
        self.twoPlayerTextColor = (0, 0, 0)

        self.buttonWidth = self.screenWidth//2-2*self.buttonMargin
        self.buttonHeight = self.screenHeight//3
        self.buttonFont = "helvetica"
        self.buttonFontSize = 80

    def createText(self):
        text = pygame.font.SysFont(self.font, self.fontSize).render(self.text, True, self.textColor)
        self.screen.blit(text, (self.textX-text.get_width()//2, self.textY-text.get_height()//2))
    def createButtons(self):
        self.onePlayerButton = Button(self.onePlayerX, self.onePlayerY, self.buttonWidth, self.buttonHeight, self.onePlayerColor, self.onePlayerText, self.buttonFont, self.buttonFontSize, self.onePlayerTextColor)

        self.twoPlayerButton = Button(self.twoPlayerX, self.twoPlayerY, self.buttonWidth, self.buttonHeight, self.twoPlayerColor, self.twoPlayerText, self.buttonFont, self.buttonFontSize, self.twoPlayerTextColor)
    def run(self):
        pygame.init()
        pygame.display.set_caption('Tic-Tac-Toe')
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen.fill((255, 255, 255))

        self.createText()
        self.createButtons()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.onePlayerButton.withinBounds(event.pos):
                        self.onePlayerButton.holdDown()
                    elif self.twoPlayerButton.withinBounds(event.pos):
                        self.twoPlayerButton.holdDown()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.onePlayerButton.withinBounds(event.pos):
                        self.onePlayerButton.drawButton()

                        self.onePlayer = OnePlayerTTT()
                        self.onePlayer.run()

                        done = self.onePlayer.exit
                    elif self.twoPlayerButton.withinBounds(event.pos):
                        self.twoPlayerButton.drawButton()

                        self.twoPlayer = TwoPlayerTTT()
                        self.twoPlayer.run()

                        done = self.twoPlayer.exit

            pygame.display.flip()

class OnePlayerTTT:
    def __init__(self):
        self.exit = False
        pass
    def run(self):
        pass

class TwoPlayerTTT:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screenWidth = self.screen.get_width()
        self.screenHeight = self.screen.get_height()

        self.screenMargin = 10
        self.textMargin = 30
        self.iconMargin = 5
        self.gridWidth = int((self.screenWidth-2*self.screenMargin)/3)
        self.upperBar = self.screenHeight - self.screenWidth

        self.buttonXbounds = [(self.screenWidth-self.screenWidth//4)//2, (self.screenWidth+self.screenWidth//4)//2]
        self.buttonYbounds = [3 * self.upperBar // 4 - self.upperBar // 8, 3 * self.upperBar // 4 + self.upperBar // 8]

        self.scores = {"X": 0,
                       "O": 0,
                       "Tie": 0
                       }

        self.turnX = True
        self.winner = None
        self.buttonDrawn = False
        self.exit = False

        self.XPositions = []
        self.OPositions = []
        self.positionsStatic = ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3))
        self.positions = list(self.positionsStatic)

        self.color = {'background': (255, 255, 255),
                      'text': (0, 0, 0),
                      'line':(0, 0, 0),
                      'X': (255, 0, 0),
                      'O': (0, 0, 255),
                      'button': (0, 255, 0),
                      'winner': (255, 217, 15)
                      }

        self.shadeFactor = 0.3

    def drawTitle(self):
        text = pygame.font.SysFont("comicsansms", 56).render("Two Player Tic-Tac-Toe", True, self.color['text'])
        self.screen.blit(text, ((self.screenWidth - text.get_width()) // 2, self.upperBar // 3 - text.get_height() // 2))

    def drawScores(self):
        XWinnerText = pygame.font.SysFont("comicsansms", 36).render("X: " + str(self.scores["X"]), True, self.color['X'])
        OWinnerText = pygame.font.SysFont("comicsansms", 36).render("O: " + str(self.scores["O"]), True, self.color['O'])

        pygame.draw.rect(self.screen, self.color['background'], pygame.Rect(self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 - XWinnerText.get_height() // 2, XWinnerText.get_width(), XWinnerText.get_height()))
        pygame.draw.rect(self.screen, self.color['background'], pygame.Rect(self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 - OWinnerText.get_height() // 2, OWinnerText.get_width(), OWinnerText.get_height()))

        if self.winner:
            if self.winner == "X":
                pygame.draw.rect(self.screen, self.color['winner'], pygame.Rect(self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 - XWinnerText.get_height() // 2, XWinnerText.get_width(), XWinnerText.get_height()))
            elif self.winner == "O":
                pygame.draw.rect(self.screen, self.color['winner'], pygame.Rect(self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 - OWinnerText.get_height() // 2, OWinnerText.get_width(), OWinnerText.get_height()))
        else:
            if self.turnX:
                pygame.draw.line(self.screen, self.color['line'], (self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 + XWinnerText.get_height() // 2), (self.textMargin + XWinnerText.get_width() // 2, 2 * self.upperBar // 3 + XWinnerText.get_height() // 2))
            else:
                pygame.draw.line(self.screen, self.color['line'], (self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 + OWinnerText.get_height() // 2), (self.screenWidth-self.textMargin + OWinnerText.get_width() // 2, 2 * self.upperBar // 3 + OWinnerText.get_height() // 2))

        self.screen.blit(XWinnerText, (self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 - XWinnerText.get_height() // 2))
        self.screen.blit(OWinnerText, (self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 - OWinnerText.get_height() // 2))

    def drawButton(self, rgb):
        self.buttonDrawn = True

        pygame.draw.rect(self.screen, rgb, pygame.Rect(self.buttonXbounds[0], self.buttonYbounds[0], self.buttonXbounds[1] - self.buttonXbounds[0], self.buttonYbounds[1] - self.buttonYbounds[0]))

        text = pygame.font.SysFont("comicsansms", 24).render("New game", True, self.color['text'])
        self.screen.blit(text, ((self.screenWidth-text.get_width())//2, 3 * self.upperBar // 4 - text.get_height() // 2))


    def drawGrid(self):
        pygame.draw.line(self.screen, self.color['line'], (self.gridWidth+self.screenMargin, self.upperBar+self.screenMargin), (self.gridWidth+self.screenMargin, self.screenHeight-self.screenMargin))
        pygame.draw.line(self.screen, self.color['line'], (2*self.gridWidth+self.screenMargin, self.upperBar+self.screenMargin), (2*self.gridWidth+self.screenMargin, self.screenHeight-self.screenMargin))
        pygame.draw.line(self.screen, self.color['line'], (self.screenMargin, self.upperBar+self.gridWidth+self.screenMargin), (self.screenWidth-self.screenMargin, self.upperBar+self.gridWidth+self.screenMargin))
        pygame.draw.line(self.screen, self.color['line'], (self.screenMargin, self.upperBar+2*self.gridWidth+self.screenMargin), (self.screenWidth-self.screenMargin, self.upperBar+2*self.gridWidth+self.screenMargin))

    def setup(self):
        self.screen.fill(self.color['background'])
        self.drawTitle()
        self.drawScores()
        self.drawGrid()

    def drawCross(self, position):
        posx = (position[1]-1)*self.gridWidth+self.screenMargin+self.iconMargin
        posy = self.upperBar+(position[0]-1)*self.gridWidth+self.screenMargin+self.iconMargin

        pygame.draw.line(self.screen, self.color['X'], (posx, posy), (posx+self.gridWidth-2*self.iconMargin, posy+self.gridWidth-2*self.iconMargin))
        pygame.draw.line(self.screen, self.color['X'], (posx+self.gridWidth-2*self.iconMargin, posy), (posx, posy+self.gridWidth-2*self.iconMargin))

    def drawCircle(self, position):
        pygame.draw.circle(self.screen, self.color['O'], (int((position[1]-1)*self.gridWidth+self.screenMargin+self.gridWidth/2), int(self.upperBar+(position[0]-1)*self.gridWidth+self.screenMargin+self.gridWidth/2)), int(self.gridWidth/2-self.screenMargin), 1)

    def drawIcon(self, position):
        pygame.draw.rect(self.screen, self.color['background'], pygame.Rect(self.screenMargin+self.iconMargin+(position[1]-1)*self.gridWidth, self.upperBar+self.screenMargin+self.iconMargin+(position[0]-1)*self.gridWidth, self.gridWidth-2*self.iconMargin, self.gridWidth-2*self.iconMargin))

        if self.turnX:
            self.drawCross(position)

            self.XPositions.append(position)
            if self.hasWon(self.XPositions):
                self.winner = "X"
        else:
            self.drawCircle(position)

            self.OPositions.append(position)
            if self.hasWon(self.OPositions):
                self.winner = "O"

    def hasWon(self, places):
        rows = [0, 0, 0]
        columns = [0, 0, 0]
        diagonals = [0, 0]
        for place in places:
            rows[place[0]-1] += 1
            columns[place[1]-1] += 1
            if place in [(1, 1), (2, 2), (3, 3)]:
                diagonals[0] += 1
            if place in [(1, 3), (2, 2), (3, 1)]:
                diagonals[1] += 1
        if 3 in rows + columns + diagonals:
            return True
        else:
            return False

    def darkerShade(self, rgb):
        return (rgb[0]*(1-self.shadeFactor), rgb[1]*(1-self.shadeFactor), rgb[2]*(1-self.shadeFactor))

    def highlight(self, event):
        if self.buttonDrawn and self.buttonXbounds[0] <= event.pos[0] and event.pos[0] <= self.buttonXbounds[1] and self.buttonYbounds[0] <= event.pos[1] and event.pos[1] <= self.buttonYbounds[1]:
            self.drawButton(self.darkerShade(self.color['button']))
        elif not self.buttonDrawn:
            position = (math.floor((event.pos[1]-self.upperBar)/self.gridWidth)+1, math.floor(event.pos[0]/self.gridWidth)+1)

            if position in self.positions:
                pygame.draw.rect(self.screen, self.darkerShade(self.color['background']), pygame.Rect(self.screenMargin+self.iconMargin+(position[1]-1)*self.gridWidth, self.upperBar+self.screenMargin+self.iconMargin+(position[0]-1)*self.gridWidth, self.gridWidth-2*self.iconMargin, self.gridWidth-2*self.iconMargin))

    def buttonClicked(self):
        self.turnX = True
        self.buttonDrawn = False

        self.XPositions = []
        self.OPositions = []
        self.positions = list(self.positionsStatic)

        self.setup()

    def mouseClick(self, event):
        if self.buttonDrawn and self.buttonXbounds[0] <= event.pos[0] and event.pos[0] <= self.buttonXbounds[1] and self.buttonYbounds[0] <= event.pos[1] and event.pos[1] <= self.buttonYbounds[1]:
            self.buttonClicked()

        elif not self.buttonDrawn:
            position = (math.floor((event.pos[1]-self.upperBar)/self.gridWidth)+1, math.floor(event.pos[0]/self.gridWidth)+1)

            if position in self.positions:
                self.positions.remove(position)
                self.drawIcon(position)
                if self.positions == [] and not self.winner:
                    self.winner = "Tie"
                self.turnX = not self.turnX
                self.drawScores()

    def redrawBoard(self):
        self.screen.fill(self.color['background'])
        self.setup()
        for position in self.XPositions:
            self.drawCross(position)
        for position in self.OPositions:
            self.drawCircle(position)

    def run(self):
        self.setup()
        clock = pygame.time.Clock()

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.highlight(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseClick(event)
                if not self.winner == None:
                    self.scores[self.winner] += 1
                    self.redrawBoard()
                    self.drawButton(self.color['button'])
                    self.winner = None

            pygame.display.flip()
            clock.tick(60)

def main():
    interface = Interface()
    interface.run()

if __name__ == "__main__":
    main()
