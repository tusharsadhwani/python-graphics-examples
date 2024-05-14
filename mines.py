from graphics import *
from random import randint, seed
from time import sleep, time

class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.t = ''
        self.bee = False
        self.flagged = False
        self.revealed = False
        self.flooding = False

    def show(self):
        if self.flagged:
            self.flagged = False
        if not self.revealed:
            rect = Rectangle(Point(self.col * State.size, self.row * State.size),
                             Point((self.col+1) * State.size, (self.row+1) * State.size))
            rect.setFill(color_rgb(170, 170, 170))
            rect.setWidth(2)
            rect.draw(State.win)
            self.revealed = True
        if self.bee:
            self.revealed = True
            showall(False)

            alert = GraphWin("You Hit a mine!", 300, 100)
            alert.setBackground('white')
            txt = Text(Point(150, 30), "You lose.")
            retry = Text(Point(150, 65), "Retry?(y/n)")
            txt.draw(alert)
            retry.draw(alert)
            while True:
                try:
                    key_input = alert.getKey()
                except:
                    State.win.close()
                    State.playing = False
                    return
                if key_input == 'y' or key_input == 'Y':
                    alert.close()
                    State.win.close()
                    main()
                    break
                elif key_input == 'n' or key_input == 'N':
                    State.playing = False
                    alert.close()
                    State.win.close()
                    break
        else:
            neighbours = self.countNeighbours()
            if neighbours == 0:
                if not self.flooding:
                    floodfill(self)
            else:
                self.t = Text(Point(State.size * 0.5 + self.col * State.size,
                                    State.size * 0.5 + self.row * State.size), neighbours)
                textsize = int(State.size * 0.5) - (int(State.size * 0.5) % 4)
                if textsize <= 36:
                    self.t.setSize(textsize)
                else:
                    self.t.setSize(36)
                self.t.draw(State.win)

    def flag(self):
        if not self.revealed:
            if not self.flagged:
                self.flagged = True
                self.t = Text(Point(State.size * 0.5 + self.col * State.size,
                                    State.size * 0.5 + self.row * State.size), 'F')
                textsize = int(State.size * 0.5) - (int(State.size * 0.5) % 4)
                if textsize <= 36:
                    self.t.setSize(textsize)
                else:
                    self.t.setSize(36)
                self.t.setFill('red')
                self.t.draw(State.win)
            else:
                self.t.undraw()
                self.flagged = False

        flag_count = 0
        invalid = False
        for i in State.grid:
            for j in i:
                if j.flagged and not j.bee:
                    invalid = True
                if j.flagged and j.bee:
                    flag_count += 1

        if flag_count == State.mine_num and not invalid:
            showall(True)
            alert = GraphWin("You WIN!!!", 300, 100)
            alert.setBackground('white')
            txt = Text(Point(150, 30), "You won the game!")
            retry = Text(Point(150, 65), "Replay?(y/n)")
            txt.draw(alert)
            retry.draw(alert)
            while True:
                try:
                    key_input = alert.getKey()
                except:
                    State.win.close()
                    State.playing = False
                    return
                if key_input == 'y' or key_input == 'Y':
                    alert.close()
                    State.win.close()
                    main()
                    break
                elif key_input == 'n' or key_input == 'N':
                    State.playing = False
                    alert.close()
                    State.win.close()
                    break

    def countNeighbours(self):
        r = self.row
        c = self.col
        n = 0
        for i in [r-1, r, r+1]:
            for j in [c-1, c, c+1]:
                if (not (i == r and j == c)) and i >= 0 and i <= State.gridsize - 1 and j >= 0 and j <= State.gridsize - 1:
                    if State.grid[i][j].bee:
                        n += 1
        return n


def floodfill(self):
    self.flooding = True
    r = self.row
    c = self.col
    n = 0
    for i in [r-1, r, r+1]:
        for j in [c-1, c, c+1]:
            if (i >= 0 and
                i <= State.gridsize - 1 and
                j >= 0 and
                j <= State.gridsize - 1 and
                State.grid[i][j].revealed == False and
                State.grid[i][j].bee == False):
                State.grid[i][j].show()
                if State.grid[i][j].countNeighbours() == 0:
                    floodfill(State.grid[i][j])


def showall(won):
    for i in range(len(State.grid)):
        for j in range(len(State.grid[i])):
            cell = State.grid[i][j]
            if not cell.revealed:
                rect = Rectangle(Point(cell.col * State.size, cell.row * State.size),
                                 Point((cell.col+1) * State.size, (cell.row+1) * State.size))
                rect.setFill(color_rgb(170, 170, 170))
                rect.setWidth(2)
                rect.draw(State.win)
                cell.revealed = True
            if cell.bee:
                cell.revealed = True
                rect = Rectangle(Point(cell.col * State.size, cell.row * State.size),
                                 Point((cell.col+1) * State.size, (cell.row+1) * State.size))
                if won == True:
                    rect.setFill('green')
                else:
                    rect.setFill('red')
                rect.setWidth(2)
                rect.draw(State.win)
                b = Circle(Point(State.size * 0.5 + cell.col * State.size,
                                 State.size * 0.5 + cell.row * State.size), State.size * 0.25)
                b.setFill('black')
                b.draw(State.win)
                for k in [-1, 0, 1]:
                    for l in [-1, 0, 1]:
                        if k == 0 or l == 0:
                            spoke = Line(Point(State.size * 0.5 + cell.col * State.size, State.size * 0.5 + cell.row * State.size), Point(
                                (State.size * 0.5 + State.size * 0.33 * k) + cell.col * State.size, (State.size * 0.5 + State.size * 0.33 * l) + cell.row * State.size))
                        else:
                            spoke = Line(Point(State.size * 0.5 + cell.col * State.size, State.size * 0.5 + cell.row * State.size), Point(
                                (State.size * 0.5 + State.size * 0.25 * k) + cell.col * State.size, (State.size * 0.5 + State.size * 0.25 * l) + cell.row * State.size))
                        spoke.setWidth(5)
                        spoke.draw(State.win)

            else:
                neighbours = cell.countNeighbours()
                if neighbours == 0:
                    pass
                else:
                    t = Text(Point(State.size * 0.5 + cell.col * State.size,
                                   State.size * 0.5 + cell.row * State.size), neighbours)
                    textsize = int(State.size * 0.5) - (int(State.size * 0.5) % 4)
                    if textsize <= 36:
                        t.setSize(textsize)
                    else:
                        t.setSize(36)
                    t.draw(State.win)


def drawboard():
    board = []
    for i in range(State.gridsize + 1):
        h = Line(Point(0 + State.size * i, 0), Point(0 + State.size * i, State.windowsize))
        h.setWidth(2)
        v = Line(Point(0, 0 + State.size * i), Point(State.windowsize, 0 + State.size * i))
        v.setWidth(2)
        board.append(v)
        board.append(h)
    for k in range(len(board)):
        board[k].draw(State.win)


def get_input():
    try:
        click = State.win.getMouse()
    except:
        State.playing = False
        return
    row = int(click.getY() / State.size)
    col = int(click.getX() / State.size)
    if row > State.gridsize - 1:
        row = State.gridsize - 1
    if col > State.gridsize - 1:
        col = State.gridsize - 1

    start = time()
    while time() - start < 0.12:
        click = State.win.checkMouse()
        if click:
            if int(click.getY() / State.size) == row and int(click.getX() / State.size) == col:
                State.grid[row][col].flag()
                break
    else:
        State.grid[row][col].show()


def difficulty():
    mode = GraphWin("Choose Difficulty", 450, 450)
    mode.setBackground('white')
    heading = Text(Point(225, 22), "Choose game mode: ")
    heading.setSize(25)
    heading.draw(mode)

    easy = Rectangle(Point(40, 50), Point(210, 220))
    easy.setOutline('green3')
    easy.setWidth(3)
    easy.draw(mode)
    text = Text(Point(125, 100), "Easy:")
    text.setSize(15)
    text.draw(mode)
    desc = Text(Point(125, 150), "8x8 grid, 8 bombs")
    desc.draw(mode)

    medium = Rectangle(Point(240, 50), Point(410, 220))
    medium.setOutline('blue')
    medium.setWidth(3)
    medium.draw(mode)
    text = Text(Point(325, 100), "Medium:")
    text.setSize(15)
    text.draw(mode)
    desc = Text(Point(325, 150), "10x10 grid, 12 bombs")
    desc.draw(mode)

    hard = Rectangle(Point(40, 250), Point(210, 420))
    hard.setOutline('red')
    hard.setWidth(3)
    hard.draw(mode)
    text = Text(Point(125, 300), "Hard:")
    text.setSize(15)
    text.draw(mode)
    desc = Text(Point(125, 350), "12x12 grid, 20 bombs")
    desc.draw(mode)

    insane = Rectangle(Point(240, 250), Point(410, 420))
    insane.setWidth(3)
    insane.draw(mode)
    text = Text(Point(325, 300), "Insane:")
    text.setSize(15)
    text.draw(mode)
    desc = Text(Point(325, 350), "15x15 grid, 40 bombs")
    desc.draw(mode)

    while True:
        try:
            click = mode.getMouse()
        except:
            State.playing = False
            return(0, 0)

        if (40 < click.getX() < 210 and 50 < click.getY() < 220):
            mode.close()
            return(8, 8)
        elif (240 < click.getX() < 410 and 50 < click.getY() < 220):
            mode.close()
            return(10, 12)
        elif (40 < click.getX() < 210 and 250 < click.getY() < 420):
            mode.close()
            return(12, 20)
        elif (240 < click.getX() < 410 and 250 < click.getY() < 420):
            mode.close()
            return(15, 40)


def main():
    State.grid = []
    State.playing = True

    State.gridsize, State.mine_num = difficulty()
    try:
        State.size = State.windowsize / State.gridsize
    except:
        return

    for rows in range(State.gridsize):
        State.grid.append([])
        for cols in range(State.gridsize):
            State.grid[rows].append(Cell(rows, cols))

    seed()
    mines = 0
    while mines < State.mine_num:
        cell_row = randint(0, State.gridsize - 1)
        cell_col = randint(0, State.gridsize - 1)
        if not State.grid[cell_row][cell_col].bee:
            State.grid[cell_row][cell_col].bee = True
            mines += 1

    State.win = GraphWin("Minesweeper", State.windowsize + 1, State.windowsize + 1)
    State.win.setBackground('white')

    drawboard()

# main
class State:
    gridsize = 8
    windowsize = 600
    mine_num = 8

    win = None
    playing = True
    grid = []
    size = windowsize / gridsize

def run():
    main()

    while State.playing:
        get_input()

    print("Thank you for playing Minesweeper!")

if __name__ == '__main__':
    run()