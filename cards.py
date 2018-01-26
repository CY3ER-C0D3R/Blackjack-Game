# coding: utf-8
import random

def make_deck():
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    suits = [u'♠',u'♥',u'♦',u'♣']
    #suits = ['S','H','D','C']
    deck = []
    for i in range(0,len(ranks)):
        for j in range(0, len(suits)):
            deck.append(unichr(ord('|'))+ranks[i]+suits[j]+unichr(ord('|')))
        random.shuffle(deck)
    return deck

def deal_hand(n, deck):
    hand = [deck[i] for i in range(n)]
    del deck[:n]
    return hand, deck

def deal(cards_per_hand, no_of_players):
    deck = make_deck()
    hands = []
    for i in range(no_of_players):    
        hand, deck = deal_hand(cards_per_hand, deck)
        hands.append(hand)
    return hands

players = deal(2, 2)
print '[[',players[0][0],',',players[0][1],'][',players[1][0],',',players[1][1],']]'
player_one = players[0]
print 'Player 1:', player_one[0],player_one[1]
player_two = players[1]
print 'Player 2:', player_two[0],player_two[1]







