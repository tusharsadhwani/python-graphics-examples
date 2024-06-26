from graphics import *
from random import randint, seed
from time import sleep

def drawboard():
    board = []
    for i in range(9):
        h = Line(Point(0 + 75 * i, 0), Point(0 + 75 * i, 600))
        h.setWidth(2)
        v = Line(Point(0, 0 + 75 * i), Point(600, 0 + 75 * i))
        v.setWidth(2)
        board.append(v)
        board.append(h)
    for k in range(len(board)):
        board[k].draw(State.win)

    buttons = []
    txt = []
    for i in range(8):
        buttons.append(Rectangle(Point(10 + 75 * i, 610), Point(65 + 75 * i, 665)))
        buttons[i].setWidth(3)
        buttons[i].setFill('green')
        txt.append(Text(buttons[i].getCenter(),i+1))

        buttons[i].draw(State.win)
        txt[i].draw(State.win)

def user_input():
    while True:
        try:
            click = State.win.getMouse()
            if click.getY() >= 610 and click.getY() <= 665:
                row = (int(click.getX() / 75))
                valid = False
                for i in range(len(State.discs[row])):
                    if State.discs[row][i] == 0: 
                        State.discs[row][i] = 1
                        valid = True
                        drawdisc(row, i, 1)
                        break
                if valid:
                    break
        except:
            State.win.close()
            State.playing = False
            return

def computer_input():
    sleep(0.3)
    while True:
        seed()
        row = randint(0,7)
        valid = False
        for i in range(len(State.discs[row])):
            if State.discs[row][i] == 0: 
                State.discs[row][i] = 2
                valid = True
                drawdisc(row, i, 2)
                break
        if valid:
            break

def check_user():           # Checking User's win
    won = False
    for i in range(len(State.discs)-3):
        for j in range(len(State.discs[i])):
            if State.discs[i][j] == State.discs[i+1][j] == State.discs[i+2][j] == State.discs[i+3][j] == 1:
                won = True
                wd = ((i,j), (i+3,j))
                break
        for j in range(len(State.discs[i])-3):
            if State.discs[i][j] == State.discs[i+1][j+1] == State.discs[i+2][j+2] == State.discs[i+3][j+3] == 1:
                won = True
                wd = ((i,j), (i+3,j+3))
                break
            elif State.discs[i][j+3] == State.discs[i+1][j+2] == State.discs[i+2][j+1] == State.discs[i+3][j] == 1:
                won = True
                wd = ((i,j+3), (i+3,j))
                break
    for i in range(len(State.discs)):
        for j in range(len(State.discs[i])-3):
            if State.discs[i][j] == State.discs[i][j+1] == State.discs[i][j+2] == State.discs[i][j+3] == 1:
                won = True
                wd = ((i,j), (i,j+3))
                break

    if won:
        line = Line(Point(37.5 + wd[0][0] * 75, 600 - (37.5 + wd[0][1] * 75)), Point(37.5 + wd[1][0] * 75, 600 - (37.5 + wd[1][1] * 75)))
        line.setWidth(5)
        line.draw(State.win)
        
        alert = GraphWin("You Win!",300,100)
        alert.setBackground('white')
        txt = Text(Point(150,30),"You win!")
        retry = Text(Point(150,65), "Retry?(y/n)")
        txt.draw(alert)
        retry.draw(alert)
        while True:
            key_input = alert.getKey()
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
        
            
def check_comp():           #Checking Computer's win
    won = False
    for i in range(len(State.discs)-3):
        for j in range(len(State.discs[i])):
            if State.discs[i][j] == State.discs[i+1][j] == State.discs[i+2][j] == State.discs[i+3][j] == 2:
                won = True
                wd = ((i,j), (i+3,j))
                break
        for j in range(len(State.discs[i])-3):
            if State.discs[i][j] == State.discs[i+1][j+1] == State.discs[i+2][j+2] == State.discs[i+3][j+3] == 2:
                won = True
                wd = ((i,j), (i+3,j+3))
                break
            elif State.discs[i][j+3] == State.discs[i+1][j+2] == State.discs[i+2][j+1] == State.discs[i+3][j] == 2:
                won = True
                wd = ((i,j+3), (i+3,j))
                break
    for i in range(len(State.discs)):
        for j in range(len(State.discs[i])-3):
            if State.discs[i][j] == State.discs[i][j+1] == State.discs[i][j+2] == State.discs[i][j+3] == 2:
                won = True
                wd = ((i,j), (i,j+3))
                break

    if won:
        line = Line(Point(37.5 + wd[0][0] * 75, 600 - (37.5 + wd[0][1] * 75)), Point(37.5 + wd[1][0] * 75, 600 - (37.5 + wd[1][1] * 75)))
        line.setWidth(5)
        line.draw(State.win)
        
        alert = GraphWin("You Lose!",300,100)
        alert.setBackground('white')
        txt = Text(Point(150,30),"You Lose!")
        retry = Text(Point(150,65), "Retry?(y/n)")
        txt.draw(alert)
        retry.draw(alert)
        while True:
            key_input = alert.getKey()
            if key_input == 'y' or key_input == 'Y':
                alert.close()
                State.win.close()
                main()
            elif key_input == 'n' or key_input == 'N':
                State.playing = False
                alert.close()
                State.win.close()
            break
    
    complete = True
    for i in range(len(State.discs)):
        for j in range(len(State.discs[i])):
            if State.discs[i][j] == 0:
                complete = False

    if complete:
        alert = GraphWin("Draw!",300,100)
        alert.setBackground('white')
        txt = Text(Point(150,30),"It's a draw!")
        retry = Text(Point(130,65), "Retry?(y/n)")
        txt.draw(alert)
        retry.draw(alert)
        while True:
            key_input = alert.getKey()
            if key_input == 'y' or key_input == 'Y':
                alert.close()
                State.win.close()
                main()
            elif key_input == 'n' or key_input == 'N':
                State.playing = False
                alert.close()
                State.win.close()
            break

def drawdisc(row, i, colour):
    c = Circle(Point(37.5 + row * 75, 562.5 - i * 75), 28)
    c.setWidth(2)
    if colour == 1:
        c.setFill('red')
    else:
        c.setFill('yellow')
    c.draw(State.win)

def main():
    State.discs = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
    ]

    State.win = GraphWin("Connect four!", 601, 676)
    State.win.setBackground(color_rgb(45, 107, 206))
    drawboard()

#main
class State:
    playing = True
    discs = None
    win = None

def run():
    main()

    user_input()
    while State.playing:
        computer_input()
        check_comp()
        user_input()
        check_user()

    print('Thank you for playing Connect Four!')

if __name__ == '__main__':
    run()
