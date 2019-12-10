import pygame

class TwoPlayerTTT:
    def __init__(self):
        self.screenWidth = 800
        self.screenHeight = 900

        self.screenMargin = 10
        self.textMargin = 30
        self.iconMargin = 5
        self.gridWidth = int((self.screenWidth-2*self.screenMargin)/3)
        self.upperBar = self.screenHeight - self.screenWidth

        self.buttonXbounds = [(self.screenWidth-self.screenWidth//4)//2, (self.screenWidth+self.screenWidth//4)//2]
        self.buttonYbounds = [3 * self.upperBar // 4 - self.upperBar // 8, 3 * self.upperBar // 4 + self.upperBar // 8]

        self.scores = {"X": 0, "O": 0}
        self.turnX = True
        self.winner = None
        self.buttonDrawn = False

        self.XPositions = []
        self.OPositions = []
        self.positionsStatic = ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3))
        self.positions = list(self.positionsStatic)

        self.backgroundColor = (255, 255, 255)
        self.textColor = (0, 0, 0)
        self.lineColor = (0, 0, 0)
        self.XColor = (255, 0, 0)
        self.OColor = (0, 0, 255)
        self.buttonColor = (0, 255, 0)
        self.winnerBackgroundColor = (255, 217, 15)

    def drawTitle(self):
        text = pygame.font.SysFont("comicsansms", 56).render("Two Player Tic-Tac-Toe", True, self.textColor)
        self.screen.blit(text, ((self.screenWidth - text.get_width()) // 2, self.upperBar // 3 - text.get_height() // 2))

    def drawScores(self, drawBackground=False):
        XWinnerText = pygame.font.SysFont("comicsansms", 36).render("X: " + str(self.scores["X"]), True, self.XColor)
        OWinnerText = pygame.font.SysFont("comicsansms", 36).render("O: " + str(self.scores["O"]), True, self.OColor)

        if drawBackground:
            if self.winner == "X":
                pygame.draw.rect(self.screen, self.winnerBackgroundColor, pygame.Rect(self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 - XWinnerText.get_height() // 2, XWinnerText.get_width(), XWinnerText.get_height()))
            else:
                pygame.draw.rect(self.screen, self.winnerBackgroundColor, pygame.Rect(self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 - OWinnerText.get_height() // 2, OWinnerText.get_width(), OWinnerText.get_height()))

        self.screen.blit(XWinnerText, (self.textMargin - XWinnerText.get_width() // 2, 2 * self.upperBar // 3 - XWinnerText.get_height() // 2))
        self.screen.blit(OWinnerText, (self.screenWidth-self.textMargin - OWinnerText.get_width() // 2, 2 * self.upperBar // 3 - OWinnerText.get_height() // 2))

    def drawButton(self):
        self.buttonDrawn = True

        pygame.draw.rect(self.screen, self.buttonColor, pygame.Rect(self.buttonXbounds[0], self.buttonYbounds[0], self.buttonXbounds[1] - self.buttonXbounds[0], self.buttonYbounds[1] - self.buttonYbounds[0]))

        text = pygame.font.SysFont("comicsansms", 24).render("New game", True, self.textColor)
        self.screen.blit(text, ((self.screenWidth-text.get_width())//2, 3 * self.upperBar // 4 - text.get_height() // 2))


    def drawGrid(self):
        pygame.draw.line(self.screen, self.lineColor, (self.gridWidth+self.screenMargin, self.upperBar+self.screenMargin), (self.gridWidth+self.screenMargin, self.screenHeight-self.screenMargin))
        pygame.draw.line(self.screen, self.lineColor, (2*self.gridWidth+self.screenMargin, self.upperBar+self.screenMargin), (2*self.gridWidth+self.screenMargin, self.screenHeight-self.screenMargin))
        pygame.draw.line(self.screen, self.lineColor, (self.screenMargin, self.upperBar+self.gridWidth+self.screenMargin), (self.screenWidth-self.screenMargin, self.upperBar+self.gridWidth+self.screenMargin))
        pygame.draw.line(self.screen, self.lineColor, (self.screenMargin, self.upperBar+2*self.gridWidth+self.screenMargin), (self.screenWidth-self.screenMargin, self.upperBar+2*self.gridWidth+self.screenMargin))

    def drawCross(self, position):
        posx = (position[1]-1)*self.gridWidth+self.screenMargin+self.iconMargin
        posy = self.upperBar+(position[0]-1)*self.gridWidth+self.screenMargin+self.iconMargin

        pygame.draw.line(self.screen, self.XColor, (posx, posy), (posx+self.gridWidth-2*self.iconMargin, posy+self.gridWidth-2*self.iconMargin))
        pygame.draw.line(self.screen, self.XColor, (posx+self.gridWidth-2*self.iconMargin, posy), (posx, posy+self.gridWidth-2*self.iconMargin))

    def drawCircle(self, position):
        pygame.draw.circle(self.screen, self.OColor, (int((position[1]-1)*self.gridWidth+self.screenMargin+self.gridWidth/2), int(self.upperBar+(position[0]-1)*self.gridWidth+self.screenMargin+self.gridWidth/2)), int(self.gridWidth/2-self.screenMargin), 1)

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

    def drawIcon(self, position):
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

    def buttonClicked(self):
        self.turnX = True
        self.buttonDrawn = False

        self.XPositions = []
        self.OPositions = []
        self.positions = list(self.positionsStatic)

        self.screen.fill(self.backgroundColor)
        self.drawTitle()
        self.drawScores()
        self.drawGrid()

    def mouseClick(self, event):
        if self.buttonDrawn and self.buttonXbounds[0] <= event.pos[0] and event.pos[0] <= self.buttonXbounds[1] and self.buttonYbounds[0] <= event.pos[1] and event.pos[1] <= self.buttonYbounds[1]:
            self.buttonClicked()
        else:
            position = (int((event.pos[1]-self.upperBar)/self.gridWidth)+1, int(event.pos[0]/self.gridWidth)+1)

            if position in self.positions:
                self.positions.remove(position)
                self.drawIcon(position)
                self.turnX = not self.turnX

    def redrawBoard(self):
        self.screen.fill(self.backgroundColor)
        self.drawTitle()
        self.drawScores(True)
        self.drawGrid()
        for position in self.XPositions:
            self.drawCross(position)
        for position in self.OPositions:
            self.drawCircle(position)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen.fill(self.backgroundColor)
        self.drawTitle()
        self.drawScores()
        self.drawGrid()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseClick(event)
                if not self.winner == None:
                    self.scores[self.winner] += 1
                    self.redrawBoard()
                    self.drawButton()
                    self.winner = None

            pygame.display.flip()

def main():
    tictactoe = TwoPlayerTTT()
    tictactoe.run()

if __name__ == "__main__":
    main()
