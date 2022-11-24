# Imports and setting up database
from tkinter import *
import sqlite3
from random import randrange

try:
    conn = sqlite3.connect('high_scores.db')
    c = conn.cursor()
    c.execute("CREATE TABLE scores (score int);")
    c.execute("DELETE * FROM scores;")
    #c.execute("INSERT INTO scores (score) VALUES 0;")
    conn.commit()
    conn.close()
except:
    pass
""" 
    IDEAS: 
        1 High Score on database _/
        2 Way to identify newly spawned tile 
        3 fix bug ???
        4 menu
        5 stats 
        6 sound (bg music and slide / merge noises
        7 reverse 2048? make 2
        8 undo button _/
        )
"""
class Game:
    colours = {
        '': 'white',
        '2': 'bisque1',
        '4': 'bisque3',
        '8': 'orange',
        '16': 'chocolate',
        '32': 'IndianRed',
        '64': 'crimson',
        '128': 'yellow',
        '256': 'yellow2',
        '512': 'yellow3',
        '1024': 'gold1',
        '2048': 'gold2',
        '4096': 'yellow',
        }
    directions  = ["Up", "Down", "Left", "Right"]
    def __init__(self):
        
        # Setting key attributes and setting up gui
        self.root = Tk()
        self.root.title('2048')
        self.root.iconbitmap('MbTurtle.ico')
        self.root.geometry("455x580")
        self.root.configure(background="LemonChiffon")

        # Fetching and displaying high score
        conn = sqlite3.connect('high_scores.db')
        c = conn.cursor()
        c.execute("SELECT *,oid FROM scores")
        scs = c.fetchall()
        self.highscore = str(scs[0][0])
        conn.commit()
        conn.close()

        # Initialising grid properties and score
        self.score = 0
        self.grid = [['','','',''],['','','',''],['','','',''],['','','','']]
        self.prev = self.grid
        self.turncount = 1

        # Populating gui with relevant buttons and binding key presses
        self.load()
        self.spawner = Button(self.root, text="Spawn another tile", command=self.spawn)
        self.spawner.grid(row=6, column=0, columnspan=2)
        self.undo = Button(self.root, text="Undo Move", command=self.undo)
        self.undo.grid(row=6, column=2, columnspan=2)
        self.root.bind("<Left>",self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)

        # Run main game loop
        self.root.mainloop()
    
    # Function generates tile with given value in given position on grid
    def tile(self, r, c, value):
        # Ensure that r and c are within bounds
        if r >= 5 or c >= 4:
            raise Exception("Doesn't fit on grid")
        
        # Tkinter formatting for square
        number = str(value)
        visual = Label(self.root, text=number, font=("Helvetica",12), \
        height=5, width=10, bg=Game.colours[number],borderwidth=5, \
        relief="groove")
        visual.grid(row=r+1,column=c, padx=5, pady=5)
        return

    # Loads GUI after each turn
    def load(self):
        # Loading the grid after each turn, setting relevant tkinter buttons
        self.grid = [['','','',''],['','','',''],['','','',''],['','','','']]
        self.score = 0
        self.turncount = 1
        Label(self.root, text="2048!!!", font=('Helvetica',12)).grid(row=0,column=0,columnspan=1, pady=5)
        Label(self.root, text="High Score: "+str(self.highscore)).grid(row=0,column=1,columnspan=1, pady=5)
        Label(self.root, text="turn: "+str(self.turncount)).grid(row=0, column=2, pady=5)
        Label(self.root, text="score: "+str(self.score)).grid(row=0, column=3, pady=5)
        for i in range(4):
            for j in range(4):
                self.tile(i, j, '')
        i = 1
        while i <= 2:
            self.spawn()
            i += 1

    # reloads board in event of a game over, removes old gui and creates new one.
    def reload(self):
        g_o.destroy()
        retry.destroy()
        self.load()

    # Spawns a new tile, or recognises a game over state
    def spawn(self):
        # Checks whether grid is full
        fullcheck = TRUE
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == '':
                    fullcheck = FALSE
        
        # If a new tile cannot be spawned, displays game over and allows user to replay
        if fullcheck == TRUE:
            global g_o
            g_o = Label(self.root, text="GAME OVER!!!", font= ('Helvetica',20))
            g_o.grid(row=1,column=0, rowspan=4, columnspan=4)
            global retry
            retry = Button(self.root, text="retry?", command=self.reload)
            retry.grid(row=7, column=0, columnspan=4)
            return

        # This is to simulate the 1 in 10 chance of a 4 tile being spawned
        r = randrange(10)
        if r == 9:
            value= 4
        else:
            value = 2

        # Generates a random position to spawn tile
        x = randrange(4)
        y = randrange(4)

        # Redoes this until it generates on an empty slot
        while self.grid[x][y] != '':
            x = randrange(4)
            y = randrange(4)

        # Creates a tile with this value and updates grid
        self.grid[x][y] = str(value)
        self.tile(x,y,value)

    # Updates high score in database, and in game
    def hs_update(self):
        if int(self.score) > int(self.highscore):
            conn = sqlite3.connect('high_scores.db')
            c = conn.cursor()
            c.execute("""UPDATE scores SET
            score = :score

            WHERE oid = :oid""",
            {
            'score': self.score,
            'oid': 1
            })

            c.execute("SELECT *, oid FROM scores")
            scs = c.fetchall()
            self.highscore = str(scs[0][0])
            conn.commit()
            conn.close()
            return







    #### Equivalent functions for sliding up, down, left and right

    def up(self, event):

        #for checking whether anything has moved, whether to record as move / to spawn another piece
        self.temp = [['','','',''],['','','',''],['','','',''],['','','','']]
        for i in range(4):
            for j in range(4):
                self.temp[i][j] = self.grid[i][j]

        #actual movement
        for c in range(4):
            r = 0
            while r < 3:
                for i in range(3):
                    self.shuffle_up(i,c)
                for i in range(3):
                    self.shuffle_up(i,c)
                if self.grid[r][c] == self.grid[r+1][c] and self.grid[r][c] != '':
                    self.grid[r][c] = str(2*int(self.grid[r][c]))
                    self.score += int(self.grid[r][c])
                    self.grid[r+1][c] = ''
                    r += 1
                else:
                    r += 1

        #spawning new tile if necessary, and updating gui
        if self.temp == self.grid:
            fullcheck = TRUE
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == '':
                        fullcheck = FALSE
            if fullcheck == TRUE:
                global g_o
                g_o = Label(self.root, text="GAME OVER!!!", font= ('Helvetica',20))
                g_o.grid(row=1,column=0, rowspan=4, columnspan=4)
                global retry
                retry = Button(self.root, text="retry?", command=self.reload)
                retry.grid(row=7, column=0, columnspan=4)
                return
        self.prev = self.temp
        self.turncount += 1
        self.hs_update()
        self.reprint()
        self.spawn()


    def down(self, event):

        #for checking whether anything has moved, whether to record as move / to spawn another piece
        self.temp = [['','','',''],['','','',''],['','','',''],['','','','']]
        for i in range(4):
            for j in range(4):
                self.temp[i][j] = self.grid[i][j]

        #actual movement
        for c in range(4):
            r = 3
            while r > 0:
                for i in range(3,0,-1):
                    self.shuffle_down(i,c)
                for i in range(3,0,-1):
                    self.shuffle_down(i,c)
                if self.grid[r][c] == self.grid[r-1][c] and self.grid[r][c] != '':
                    self.grid[r][c] = str(2*int(self.grid[r][c]))
                    self.score += int(self.grid[r][c])
                    self.grid[r-1][c] = ''
                    r -= 1
                else:
                    r -= 1

       #spawning new tile if necessary, and updating gui
        if self.temp == self.grid:
            fullcheck = TRUE
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == '':
                        fullcheck = FALSE
            if fullcheck == TRUE:
                global g_o
                g_o = Label(self.root, text="GAME OVER!!!", font= ('Helvetica',20))
                g_o.grid(row=1,column=0, rowspan=4, columnspan=4)
                global retry
                retry = Button(self.root, text="retry?", command=self.reload)
                retry.grid(row=7, column=0, columnspan=4)
                return

        self.prev = self.temp
        self.turncount += 1
        self.hs_update()
        self.reprint()
        self.spawn()

    def left(self, event):

        #for checking whether anything has moved, whether to record as move / to spawn another piece
        self.temp = [['','','',''],['','','',''],['','','',''],['','','','']]
        for i in range(4):
            for j in range(4):
                self.temp[i][j] = self.grid[i][j]

        #actual movement
        for r in range(4):
            c = 0
            while c < 3:
                for i in range(3):
                    self.shuffle_left(r,i)
                for i in range(3):
                    self.shuffle_left(r,i)
                if self.grid[r][c] == self.grid[r][c+1] and self.grid[r][c] != '':
                    self.grid[r][c] = str(2*int(self.grid[r][c]))
                    self.score += int(self.grid[r][c])
                    self.grid[r][c+1] = ''
                    c += 1
                else:
                    c += 1

       #spawning new tile if necessary, and updating gui
        if self.temp == self.grid:
            fullcheck = TRUE
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == '':
                        fullcheck = FALSE
            if fullcheck == TRUE:
                global g_o
                g_o = Label(self.root, text="GAME OVER!!!", font= ('Helvetica',20))
                g_o.grid(row=1,column=0, rowspan=4, columnspan=4)
                global retry
                retry = Button(self.root, text="retry?", command=self.reload)
                retry.grid(row=7, column=0, columnspan=4)
                return
        self.prev = self.temp
        self.turncount += 1
        self.hs_update()
        self.reprint()
        self.spawn()

    def right(self, event):

       #for checking whether anything has moved, whether to record as move / to spawn another piece
        self.temp = [['','','',''],['','','',''],['','','',''],['','','','']]
        for i in range(4):
            for j in range(4):
                self.temp[i][j] = self.grid[i][j]

        #actual movement
        for r in range(4):
            c = 3
            while c > 0:
                for i in range(3,0,-1):
                    self.shuffle_right(r,i)
                for i in range(3,0,-1):
                    self.shuffle_right(r,i)
                if self.grid[r][c] == self.grid[r][c-1] and self.grid[r][c] != '':
                    self.grid[r][c] = str(2*int(self.grid[r][c]))
                    self.score += int(self.grid[r][c])
                    self.grid[r][c-1] = ''
                    c -= 1
                else:
                    c -= 1

       #spawning new tile if necessary, and updating gui
        if self.temp == self.grid:
            fullcheck = TRUE
            for i in range(4):
                for j in range(4):
                    if self.grid[i][j] == '':
                        fullcheck = FALSE
            if fullcheck == TRUE:
                global g_o
                g_o = Label(self.root, text="GAME OVER!!!", font= ('Helvetica',20))
                g_o.grid(row=1,column=0, rowspan=4, columnspan=4)
                global retry
                retry = Button(self.root, text="retry?", command=self.reload)
                retry.grid(row=7, column=0, columnspan=4)
                return
        self.prev = self.temp
        self.turncount += 1
        self.hs_update()
        self.reprint()
        self.spawn()
            

    ### Equivalent functions to shuffle grid incrementally left, right, up or down.

    def shuffle_up(self, r, c):
        if self.grid[r][c] == '':
            if r == 0:
                self.grid[0][c] = self.grid[1][c]
                self.grid[1][c] = self.grid[2][c]
                self.grid[2][c] = self.grid[3][c]
                self.grid[3][c] = ''
            if r == 1:
                self.grid[1][c] = self.grid[2][c]
                self.grid[2][c] = self.grid[3][c]
                self.grid[3][c] = ''
            if r == 2:
                self.grid[2][c] = self.grid[3][c]
                self.grid[3][c] = ''
            return
    
    def shuffle_down(self, r, c):
        if self.grid[r][c] == '':
            if r == 3:
                self.grid[3][c] = self.grid[2][c]
                self.grid[2][c] = self.grid[1][c]
                self.grid[1][c] = self.grid[0][c]
                self.grid[0][c] = ''
            if r == 2:
                self.grid[2][c] = self.grid[1][c]
                self.grid[1][c] = self.grid[0][c]
                self.grid[0][c] = ''
            if r == 1:
                self.grid[1][c] = self.grid[0][c]
                self.grid[0][c] = ''
            return

    def shuffle_left(self, r, c):
        if self.grid[r][c] == '':
            if c == 0:
                self.grid[r][0] = self.grid[r][1]
                self.grid[r][1] = self.grid[r][2]
                self.grid[r][2] = self.grid[r][3]
                self.grid[r][3] = ''
            if c == 1:
                self.grid[r][1] = self.grid[r][2]
                self.grid[r][2] = self.grid[r][3]
                self.grid[r][3] = ''
            if c == 2:
                self.grid[r][2] = self.grid[r][3]
                self.grid[r][3] = ''
            return

    def shuffle_right(self, r, c):
        if self.grid[r][c] == '':
            if c == 3:
                self.grid[r][3] = self.grid[r][2]
                self.grid[r][2] = self.grid[r][1]
                self.grid[r][1] = self.grid[r][0]
                self.grid[r][0] = ''
            if c == 2:
                self.grid[r][2] = self.grid[r][1]
                self.grid[r][1] = self.grid[r][0]
                self.grid[r][0] = ''
            if c == 1:
                self.grid[r][1] = self.grid[r][0]
                self.grid[r][0] = ''
            return


    # Repopulates GUI with correct tiles
    def reprint(self):
        for i in range(4):
            for j in range(4):
                self.tile(i, j, self.grid[i][j])
        
        Label(self.root, text="turn: "+str(self.turncount)).grid(row=0, column=2, pady=5)
        Label(self.root, text="score: "+str(self.score)).grid(row=0, column=3, pady=5)
        Label(self.root, text="High Score: "+self.highscore).grid(row=0,column=1,columnspan=1, pady=5)


    # Updates turn count and score   
    def turn(self):
        #get key input and choose up down left right
        self.turncount += 1
        Label(self.root, text="turn: "+str(self.turncount)).grid(row=0, column=2, pady=5)
        Label(self.root, text="score: "+str(self.score)).grid(row=0, column=3, pady=5)

    # Undoes previous trun
    def undo(self):
        self.grid = self.prev
        self.reprint()
        return
    
# Runs game
Game()

