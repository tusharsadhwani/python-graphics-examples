import mines
import connect_four
from warnings import filterwarnings
filterwarnings("ignore")

while True:
    print('''------------------------------------------------

 ___________________________________
|                                   |
|  Welcome to 99999999 games in 1!  |
|      (actually only 2 in 1)       |
|                                   |
| CHOICE:                           |
|                                   |
| 1: Minesweeper                    |
| 2: Connect Four                   |
| 3: Exit                           |
|___________________________________|
''')
    try:
        a = int(input("Enter the game no. you want to play:"))
    except Exception:
        print('Invalid choice.')
        continue

    print('\n------------------------------------------------')
    if a == 1:
        mines.run()
        continue
    elif a == 2:
        connect_four.run()
        continue
    elif a == 3:
        print('Goodbye!')
        exit()

    print('Invalid choice.')
