# coding: utf-8
import random

values={}
deck=[]

def make_deck():
    global deck
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = [u'♠',u'♥',u'♦',u'♣']
    for i in range(0,len(ranks)):
        for j in range(0, len(suits)):
            deck.append(unichr(ord('|'))+ranks[i]+suits[j]+unichr(ord('|')))
        random.shuffle(deck)
    return

def deal_hand(n):
    global deck
    hand=[]
    for i in range(n):
        hand.append(deck.pop())
    #hand = [deck[i] for i in range(n)]
    #del deck[:n]
    return hand

def card_values():
    '''

    :param deck: list
    :return:dictionary with cards:blackjack value
    '''
    global values
    global deck
    #Each card is built in the form of |nx|. n-card rank
    for card in deck:
        if card[1].isdigit():
            if card[2].isdigit():
                values[card] = 10 #only ten cards have two digits |10x|
            else:
                values[card] = card[1]
        elif card[1] == 'A':
            values[card] = 11 #Ace is either 1 or 11 in blackjack
        else:
            values[card] = 10 #face cards are valued 10 points each in blackjack
    values['1']=1
    return

def print_player_hand(player,name):
    '''

    :param player: list
    :param name: string
    :return: prints the player's hand
    '''
    print name,'hand: ',
    for cards in player:
        print cards,
    print
    return

def get_best_sum(player):
    '''

    :param player: list
    :return: sum of cards
    '''
    global values
    sum = 0
    ace_counter = 0
    for cards in player:
        if cards != u'1':
            if cards[1] == 'A': #if one of the cards is Ace, note so for further reference
                ace_counter = ace_counter + 1
        sum = sum + int(values[cards])
    if sum > 21 and ace_counter > 0: #if player lost and has an Ace change the Ace's value to 1 in the best way possible
        change_hand = [card for card in player]
        for i in range(0,len(change_hand)):
            if change_hand[i].find('A') != -1: #if the card is ace save its index
                index = i
        change_hand[index] = u'1'
        return get_best_sum(change_hand)
    return sum

def hit(player):
    '''

    :param player: list
    :return: list+1 card more
    '''

    hand = deal_hand(1)
    player = player + hand
    return player

def check_if_lost(player):
    '''

    :param player: list
    :return: if sum > 21 True, else False
    '''

    sum = get_best_sum(player)
    if sum > 21:
        return True
    return False

def do_computer_turn(computer,player):
    '''

    :param player: list
    :param computer: list
    :return: almost the best possible option for the computer
    '''
    global deck
    player_score = get_best_sum(player)
    computer_score = get_best_sum(computer)
    if player_score > computer_score:
        computer = hit(computer)
    elif computer_score <= 16:
        computer = hit(computer)
    else:
        return computer,'pass' #computer will pass next turn if the computer's score is below 17 and has more than the player
    return computer,'hit' #computer will hit next turn if he can

def determine_winner(player,computer):
    '''

    :param player: list
    :param computer: list
    :return: checks which of the two players won and prints it
    '''

    player_score = get_best_sum(player)
    computer_score = get_best_sum(computer)
    print 'Player: ', player_score
    print 'Computer: ',computer_score
    print '-----DETERMINE WINNER-----'
    if check_if_lost(player) and not check_if_lost(computer):
        print 'Computer won'
    elif check_if_lost(computer) and not check_if_lost(player):
        print 'Player won'
    elif player_score < computer_score:
        print 'Computer won'
    elif player_score > computer_score:
        print 'Player won'
    else:
        print 'Tie'
    if player_score == 21 or computer_score == 21:
        print 'Reached BlackJack!'
    return

def start_game():
    global values
    global deck
    make_deck()
    card_values()
    player = deal_hand(2)
    computer = deal_hand(2)
    print 'Welcome to python blackjack!'
    print '-----START GAME-----'
    print_player_hand(player,'Player')
    print_player_hand(computer,'Computer')
    print 'Do you want to hit? (y/n)',
    response = raw_input()
    while response != 'n':
        print '-----NEW HAND SCORE-----'
        player = hit(player)
        print print_player_hand(player,'player')
        print print_player_hand(computer,'Computer')
        if check_if_lost(player):
            determine_winner(player,computer)
            end_game()
        else:
            computer, decision = do_computer_turn(computer,player)
            print '-----NEW HAND SCORE-----'
            print print_player_hand(player, 'player')
            print print_player_hand(computer, 'Computer (%s)'%decision)
            if check_if_lost(computer):
                determine_winner(player, computer)
                end_game()
        print 'Do you want to hit? (y/n)',
        response = raw_input()
    computer,decision= do_computer_turn(computer,player)
    while decision != 'pass':
        computer, decision = do_computer_turn(computer, player)
        print '-----NEW HAND SCORE-----'
        print print_player_hand(player, 'player')
        print print_player_hand(computer, 'Computer (%s)'%decision)
    print '-----NEW HAND SCORE-----'
    print print_player_hand(player, 'player')
    print print_player_hand(computer, 'Computer'),"- I'm done."
    determine_winner(player,computer)
    end_game()

def end_game():
    print 'Do you want to play again? (y/n)',
    if raw_input() != 'n':
        start_game()
    else:
        exit()

if __name__ == "__main__":
    start_game()