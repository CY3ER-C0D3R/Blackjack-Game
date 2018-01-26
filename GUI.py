# coding: utf-8
from Tkinter import *
import os,sys
import random
import tkMessageBox
import datetime
import sqlite3 as lite
try:
    import tkFont, ttk
except ImportError:
    tkMessageBox.showerror('Error','Please install ttk.')
    raise SystemExit

deck=[]
values={}
player=[]
computer=[]
player_balance = 0
computer_balance = 0
#database globals
conn = None
cursor = None
# The time when the program was first launched - for database interaction
game_time = datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")

def make_deck():
    """

    :return: the function makes a deck of cards and shuffles it
    """
    global deck

    deck = [] #initialize deck
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = [u'♠',u'♥',u'♦',u'♣']
    for i in range(0,len(ranks)):
        for j in range(0, len(suits)):
            deck.append(unichr(ord('|'))+ranks[i]+suits[j]+unichr(ord('|')))
        random.shuffle(deck)
    return

def deal_hand(n):
    """

    :param n: int, number of hands to deal
    :return: array of cards
    """
    global deck
    hand=[]
    for i in range(n):
        hand.append(deck.pop())
    return hand

def card_values():
    """

    :return:dictionary with cards:blackjack value
    """
    global deck,values

    values={}
    #Each card is built in the form of |nx|. n-card rank; x-card suit
    for card in deck:
        if card[1].isdigit():
            if card[2].isdigit():
                values[card] = 10 #only ten cards have two digits |10x|
            else:
                values[card] = card[1]
        elif card[1] == 'A':
            values[card] = 11 #Ace is either 1 or 11 in blackjack, initiate to 11
        else:
            values[card] = 10 #face cards are valued 10 points each in blackjack
    values['1']=1
    return

def print_player_hand(game_player,name):
    """

    :param player: list of cards
    :param name: string
    :return: prints the player's hand
    """
    hand = "%s hand: "%name
    for card in game_player:
        hand = hand + " " + card
    game.insert("end", hand)
    return

def get_best_sum(game_player):
    """

    :param player: list of cards
    :return: the best sum of cards - if there are aces the functions uses them to create the best combination
    Note: the function is recursive in case there is more than 1 ace
    """
    global values

    sum = 0
    ace_counter = 0
    for cards in game_player:
        if cards != u'1':
            if cards[1] == 'A': #if one of the cards is Ace, note so for further reference
                ace_counter = ace_counter + 1
        sum = sum + int(values[cards])
    if sum > 21 and ace_counter > 0: #if player lost and has an Ace change the Ace's value to 1 in the best way possible
        change_hand = [card for card in game_player]
        index=0
        for i in range(0,len(change_hand)):
            if change_hand[i].find('A') != -1: #if the card is ace save its index
                index = i
        change_hand[index] = u'1' #change the ace card to be '1'. This doesn't change the hand of the player as it is saved in a temporary place
        return get_best_sum(change_hand)
    return sum

def hit(game_player):
    """

    :param player: list of cards
    :return: list with one more card
    """

    card = deal_hand(1)
    game_player = game_player + card
    return game_player

def hit_option():
    """

    :return: updates the players hand (player is global, no need to return anything)
    """
    global player
    player = hit(player)
    update_scores() #updates the text on the gui
    main_game('hit') #continue the game

def pass_option():
    """

    :return: only updates the gui, no need for adding cards to the player's hand
    """
    global player
    update_scores() #updates the text on the gui
    main_game('pass') #continue the game

def check_if_lost(game_player):
    '''

    :param player: list of cards
    :return: bool: checks if the player lost or not
    '''

    sum = get_best_sum(game_player)
    if sum > 21:
        return True
    return False

def do_computer_turn():
    '''

    :param player: list of cards
    :param computer: list of cards
    :return: string: almost the best possible option for the computer (can be 'hit' or 'pass')
    '''
    global player, computer

    player_score = get_best_sum(player)
    computer_score = get_best_sum(computer)
    if player_score > computer_score:
        computer = hit(computer)
    elif computer_score <= 16:
        computer = hit(computer)
    else:
        return 'pass' #computer will pass next turn if the computer's score is below 17 and has more than the player
    return 'hit' #computer will hit next turn if he can

def update_scores():
    """

    :return: the function updates the player and the computers scores on the gui
    """
    global player,computer
    global conn

    #update GUI
    player_score["text"] = "Player Score: %d"%(get_best_sum(player))
    computer_score["text"] = "Computer Score: %d"%(get_best_sum(computer))

def update_game_balance(winner_name):
    """

    :param winner_name: string
    :return: the function updates the whole database (without saving) according to the games and names in the name_entery (may be changed during the game)
    Note: their are two tables in the Scores.db database. One is for saving all the players and giving them an id, the second is for
          saving connecting each id to to it's user.
          The PRIMARY KEY in the USERS db is their ID which is the id placed in the USER db.
          The PRIMARY KEY in the USER db is the ID_DATE_TIME as these are three key factors to determining if the player name was changed
            during the game, or if the name was changed in separate games.
    """
    global player_balance, computer_balance
    global game_time

    # update Database (Scores.db)

    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT max(id) FROM USERS''')
        player_id = cursor.fetchone()[0]
        if player_id == None: #first player to play
            if winner_name == 'player':
                player_balance = 1
                computer_balance = 0
            else:  # winner name == 'computer'
                player_balance = 0
                computer_balance = 1
            cursor.execute('''INSERT INTO USERS(id,name) VALUES(?,?)''',(0, player_name.get()))  # player_name.get() = name_entry.get()
            cursor.execute('''REPLACE INTO USER(id,id_date_time,player,computer) VALUES(?,?,?,?)''',(0, '0  '+game_time, player_balance, computer_balance))
        else:
            cursor.execute('''SELECT id,name FROM USERS''')
            found = False
            for users in cursor.fetchall():
                if users[1] == player_name.get():
                    found = True
                    player_id = users[0] #existing player
            if not found:
                player_id += 1 #new player
                if winner_name == 'player':
                    player_balance = 1
                    computer_balance = 0
                else: #winner name == 'computer'
                    player_balance = 0
                    computer_balance = 1
            else: #Get computer balance and player balance from database USER and updates it
                cursor.execute('''SELECT id_date_time,player,computer FROM USER WHERE id=?''',(player_id,))
                user = cursor.fetchall()
                #user = [(id_date_time,player,computer),...]
                found = False
                for elements in user:
                    if elements[0] == str(player_id)+"  "+game_time: #if still the same game run
                        player_balance = elements[1] #player
                        computer_balance = elements[2] #computer
                        found = True
                if not found: #same player new game run
                    player_balance = 0
                    computer_balance = 0
                if winner_name == 'player':
                    player_balance += 1
                else: #winner name == 'computer'
                    computer_balance += 1
            #The replace function adds a new line to the table if it doesn't exist and updates a line if it does exist
            cursor.execute('''REPLACE INTO USERS(id,name) VALUES(?,?)''',(player_id, player_name.get()))
            cursor.execute('''REPLACE INTO USER(id,id_date_time,player,computer) VALUES(?,?,?,?)''',(player_id, str(player_id)+'  '+game_time, player_balance, computer_balance))

        # update GUI
        balance["text"] = "Balance %d:%d" % (player_balance, computer_balance)

        return

def start_new_game():
    """

    :return: function starts a new game, note: deck,player, and computer are global -> no need for returning anything
    """
    global deck
    global player,computer

    make_deck()
    card_values()
    player = deal_hand(2)
    computer = deal_hand(2)
    print_game('START GAME')
    update_scores()
    new_round_button["state"] = DISABLED
    hit_button["state"] = NORMAL
    pass_button["state"] = NORMAL

def main_game(decision):
    """

    :param decision: 'hit' or 'pass', comes from the buttons
    :return: users other functions to print correctly the game
    """
    global player
    global computer
    if decision != 'pass':
        print_game('NEW HAND SCORE (Player %s)' %decision)
        update_scores()
        if check_if_lost(player):
            print_game('DETERMINE WINNER')
        else:
            computer_decision = do_computer_turn()
            if computer_decision == 'pass':
                print_game('NEW HAND SCORE (Computer %sed)' %computer_decision)
            else:
                print_game('NEW HAND SCORE (Computer %s)' % computer_decision)
            update_scores()
            if check_if_lost(computer):
                print_game('DETERMINE WINNER')
            else:
                game.insert('end', 'Do you want to hit?')
    else: #player passed
        print_game('NEW HAND SCORE (Player %sed)' %decision)
        update_scores()
        if check_if_lost(player):
            print_game('DETERMINE WINNER')
        else:
            computer_decision = do_computer_turn()
            while computer_decision != 'pass' and not check_if_lost(computer):
                print_game('NEW HAND SCORE (Computer %s)' %computer_decision)
                update_scores()
                computer_decision = do_computer_turn()
            if computer_decision == 'hit':
                print_game('NEW HAND SCORE (Computer %s)' %computer_decision)
            else: #computer passed
                print_game('NEW HAND SCORE (Computer %sed)' % computer_decision)
            update_scores()
            print_game('DETERMINE WINNER')

def print_game(string):
    """

    :return: prints the string given in the game format
    """
    global player,computer

    game.insert("end",'-----%s-----'%string)
    if string != 'DETERMINE WINNER':
        game.insert("end",print_player_hand(player,'Player'))
        game.insert("end",print_player_hand(computer,'Computer'))
        if string.split("(")[0] == 'Player' or string == 'START GAME':
            game.insert('end','Do you want to hit?')
        if not scroll_state.get(): #if checked don't scroll down
            game.see(END)
    else: #string = DETERMINE WINNER
        player_score = get_best_sum(player)
        computer_score = get_best_sum(computer)
        game.insert("end", 'Player: ' + str(player_score))
        game.insert("end", 'Computer: ' + str(computer_score))
        if check_if_lost(player) and not check_if_lost(computer):
            game.insert('end','Computer won')
            update_game_balance('computer')
        elif check_if_lost(computer) and not check_if_lost(player):
            game.insert('end','Player won')
            update_game_balance('player')
        elif player_score < computer_score:
            game.insert('end','Computer won')
            update_game_balance('computer')
        elif player_score > computer_score:
            game.insert('end','Player won')
            update_game_balance('player')
        else:
            game.insert('end','Tie')
        if player_score == 21 or computer_score == 21:
            game.insert('end','Reached BlackJack!')
        game.insert('end','----------------------------------------')
        hit_button["state"] = DISABLED
        pass_button["state"] = DISABLED
    game.insert('end','') #line spacing
    if not scroll_state.get(): #if checked don't scroll down
        game.see(END)
    new_round_button["state"] = NORMAL
    return

def load_scores():
    """

    :return: loads the scores from the db
    """
    global conn

    #clear current score board
    clear_scores()
    #print updated score board
    if conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM USERS WHERE name=?''',(player_name.get(),))
        player_id = cursor.fetchone()
        #Name doesn't exist in db
        if player_id == None:
            pop_up = Tk()
            pop_up.title = 'Error'
            error_label = Label(pop_up,text="Player does not exist.")
            error_label.pack(expand='yes',fill='both',padx=5)
            ok_button = Button(pop_up,text="ok",command=pop_up.destroy, relief="groove")
            ok_button.pack(expand='yes',fill='both',pady=5,padx=5)
            error_label.mainloop()
        else: #load player with id: player_id
            player_id = player_id[0]
            cursor.execute('''SELECT id_date_time,player,computer FROM USER WHERE id=?''',(player_id,))
            for games in cursor.fetchall():
                #games[0] = (id_date_time)
                date = games[0].split()[1]
                time = games[0].split()[2]
                scores.insert('','end',text="%s"%date,values=(time,games[1],games[2]))
    return

def clear_scores():
    """

    :return: clears all the scores in the table in the gui (Treeview)
    """
    x = scores.get_children()
    if x != '()':
        for child in x:
            scores.delete(child)
    return

def save_scores():
    """

    :return: saves the changes in the db, Note: if the 'save' button isn't pressed changes won't be saved to db
    """
    global conn

    if conn:
        conn.commit()
    return

def connect_to_database(file_name):
    """

    :param file_name: string
    :return: connects to db
    """
    global conn

    try:
        conn = lite.connect(file_name)
    except lite.Error, e:
        pass
    finally:
        return

def create_new_table(file_name):
    """

    :param file_name: string
    :return: creates the db
    """
    global conn

    try:
        #USERS Table
        create_str = '''CREATE TABLE USERS (
                ID INT PRIMARY KEY NOT NULL,
                NAME TEXT NOT NULL
                )'''
        conn.execute(create_str)
        conn.commit() #save changes
    except lite.Error, e:
        pass
    finally:
        try:
            #USER Table
            create_str = '''CREATE TABLE USER (
                    ID INT NOT NULL,
                    ID_DATE_TIME TEXT PRIMARY KEY NOT NULL,
                    PLAYER INT NOT NULL,
                    COMPUTER INT NOT NULL
                    )'''
            conn.execute(create_str)
            conn.commit() #save changes
        except lite.Error, e:
            pass
        finally:
            return

def instructions():
    """

    :return: the function prints the instructions of the game in a new window
    """

    instructions = Tk()
    instructions.title("Game Instructions")
    helv18 = tkFont.Font(family="Helvetica", size=18, weight="bold")
    instructions_scrollbar = ttk.Scrollbar(instructions)
    instructions_scrollbar.pack(side=RIGHT,expand=0,fill=Y)
    txt = Text(instructions,bg="white",fg="dark blue",bd=4,wrap=WORD, font=helv16, yscrollcommand=instructions_scrollbar.set)
    instructions_scrollbar.config(command=txt.yview)
    os.chdir("C:\\Python26\\") #Blackjack Instructions.txt is in default in the python26 dir
    try:
        text = open('Blackjack Instructions.txt','rb')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    for line in text.readlines():
        txt.insert(END,line)
    txt.pack(expand=1,fill=BOTH)
    text.close() #close file
    instructions.mainloop()

def about():
    """

    :return: The function print further information about the program
    """

    about = Tk()
    about.title("About the program")
    helv18 = tkFont.Font(family="Helvetica", size=18, weight="bold")
    txt = Text(about,bg="white",fg="dark blue",bd=4,wrap=WORD, font=helv16)
    try:
        text = open('about.txt','rb')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    for line in text.readlines():
        txt.insert(END,line)
    txt.pack(expand="YES",fill="both")
    text.close() #close file
    about.mainloop()

#Alignment

def resizeable():
    # Make sure the whole window is resizeable
    for x in range(0, 5):
        root.columnconfigure(x, weight=1)
    root.columnconfigure(3, weight=0)
    root.columnconfigure(6, weight=0)
    for y in range(1, 4):
        root.rowconfigure(y, weight=1)

def align_window_to_center(width,height):
    x = root.winfo_screenwidth() / 2 - 0.5 * width
    y = root.winfo_screenheight() / 2 - 0.5 * height
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))

root = Tk()
root.title("Python Blackjack")

#connect to database and create USERS table
file_name = 'c:\\Python26\\Scores.db' #default location, can be changed if necessary.
connect_to_database(file_name)
create_new_table(file_name)

#labels
welcome_label = Label(root, text="WELCOME TO PYTHON BLACKJACK!", font="Arial 18", anchor="center", padx=10)
welcome_label.grid(row=0,column=0,padx=10,pady=5,columnspan=3)
name_label = Label(root,text="Player Name: ", font="Arial 18",compound="center")
name_label.grid(row=0,column=4,pady=5,sticky="e")
#name entry
player_name = StringVar() #saves the name in the entry
name_entry = Entry(root, font="Arial 18", fg="dark red",textvariable=player_name)
player_name.set("Enter your name") #Default value
name_entry.grid(row = 0, column=5,pady=5,padx=5,sticky="w")
#game - Listbox
game_scrollbar = ttk.Scrollbar(root)
game_scrollbar.grid(row=1,column=3,rowspan=4,sticky="ns")
helv16 = tkFont.Font(family="Helvetica",size=16,weight="bold")
game = Listbox(root,bg="white", yscrollcommand=game_scrollbar.set, font=helv16, disabledforeground="black", activestyle="dot",selectbackground="light blue",selectforeground="black")
game.see(END)
game_scrollbar.config(command=game.yview)
game.grid(row=1,column=0,rowspan=4,padx=10,pady=10,sticky="ewns",columnspan=3)
#scores - Treeview
scores_scrollbar = ttk.Scrollbar(root)
scores_scrollbar.grid(row=1,column=6,rowspan=4,ipady=121,padx=10,sticky="wns")
scores = ttk.Treeview(root, yscrollcommand=scores_scrollbar.set)
scores['columns'] = ('Time','Date','Scores')
scores.heading('#0',text='Date')
scores.column('#0',anchor='center',width=60)
scores.heading('#1',text='Time')
scores.column('#1',anchor='center',width=60)
scores.heading('#2',text='Player')
scores.column('#2',anchor='center',width=60)
scores.heading('#3',text='Computer')
scores.column('#3',anchor='center',width=60)
ttk.Style().configure("Treeview",font=('',11),background="black",foreground="white",)
scores_scrollbar.config(command=scores.yview)
#game changing info
scores.grid(row=1, column=4, rowspan=4,padx=10, pady=10, columnspan=2, sticky="nsew")
computer_score = Label(root,text="Computer score: 0",font="Arial 14",compound="center")
computer_score.grid(row=5,column=0,pady=10,columnspan=2)
player_score = Label(root,text="Player score: 0",font="Arial 14",compound="center")
player_score.grid(row=5,column=2,pady=10,columnspan=2)
balance = Label(root,text="Balance: 0:0",font="Arial 14",compound="center") #Balance = Player:Computer
balance.grid(row=5,column=4,pady=10,columnspan=2)
#buttons
hit_button = Button(root,text="Hit",font="Arial 14",relief="raise",width="15",command=hit_option, state=DISABLED)
hit_button.grid(row = 6, column=0, pady=5,padx=15)
pass_button = Button(root,text="Pass",font="Arial 14",relief="raise",width="15",command=pass_option, state=DISABLED)
pass_button.grid(row=6,column=1,pady=5,padx=15)
new_round_button = Button(root,text="New game",font="Arial 14",relief="raise",width="15",command=start_new_game)
new_round_button.grid(row=6,column=2,pady=5,padx=15)
exit_button = Button(root,text="Exit",font="Arial 14",relief="raise",width="15",command=root.destroy)
exit_button.grid(row=6,column=4,pady=5,columnspan=2)

#menubar

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Load", command=load_scores)
filemenu.add_command(label="Save", command=save_scores)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)

menubar.add_cascade(label="File", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
#scroll boolean var for changing the scrolling state
scroll_state = BooleanVar() #default is that the scroll bar goes down automatically with the text
scroll_state.set(False) #default is to scroll down automatically
editmenu.add_checkbutton(label="Scroll disabled",variable=scroll_state)

menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=1)
helpmenu.add_command(label="How to play?", command=instructions)
helpmenu.add_command(label="About...", command=about)

menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)  # displays the menu

resizeable()
align_window_to_center(1100,500) #size: width=1100, height=500
root.update()
root.minsize(root.winfo_width(),root.winfo_height())

root.mainloop()