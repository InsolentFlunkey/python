import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing_blackjack = True
playing_hand = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_contents = ""
        for card in self.deck:
            deck_contents += "\n" + card.__str__()
        return deck_contents

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("Enter bet amount: "))
        except:
            print("Please enter a numeric value")
        else:
            if chips.bet <= chips.total:
                break
            else:
                print("Bet cannot be more than you total number of chips!")

def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing_hand  # to control an upcoming while loop
    response = ""
    while True:
        response = input("Do you want to Hit or Stand? Enter H or S: ")
        if response.upper() == 'H':
            hit(deck,hand)
            playing_hand = True
            break
        elif response.upper() == 'S':
            playing_hand = False
            break
        else:
            print("Please enter H to hit or S to stand")

def show_some(player,dealer):
    print( "\n"*3 )
    print("Dealer's cards (first card is hidden): ")
    card_ct = 0
    for card in dealer.cards:
        if card_ct == 0:
            print("\t<Hidden>")
        else:
            print( "\t" + card.rank + " of " + card.suit )
        card_ct += 1
    
    print("\nYour cards:")
    for card in player.cards:
        print( "\t" + card.rank + " of " + card.suit )
    print("\t" + "Total value: {}".format(player.value) )
    
def show_all(player,dealer):
    print( "\n"*3 )
    print("Dealer's cards: ")
    for card in dealer.cards:
        print( "\t" + card.rank + " of " + card.suit )
    print( "\t" + "Total value: {}".format(dealer.value) )
    
    print( "\nYour cards:" )
    for card in player.cards:
        print( "\t" + card.rank + " of " + card.suit )
    print( "\t" + "Total value: {}".format(player.value) )

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts, Player wins!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push():
    print("It's a tie!")

# Print an opening statement
print("Welcome to Blackjack!")
playing_blackjack = True

# Set up the Player's chips
player_chips = Chips()

while playing_blackjack:
    
    # Create & shuffle the deck, deal two cards to each player
    new_deck = Deck()
    new_deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(new_deck.deal())
    player_hand.add_card(new_deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(new_deck.deal())
    dealer_hand.add_card(new_deck.deal())

    # Prompt the Player for their bet
    print("Player, you have {} chips".format(player_chips.total))
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)

    
    while playing_hand:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(new_deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(new_deck,dealer_hand)
            show_some(player_hand,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif player_hand.value == dealer_hand.value:
            push()
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
    
    # Inform Player of their chips total
    if player_chips.total > 0:
        print("Player, you have {} chips".format(player_chips.total))
    else:
        print("Player, you are out of chips!  Game over!!")
        playing_blackjack = False
        break
    
    # Ask to play again
    response = ""
    while response != "Y" and response != "N":
        response = input("Do you want to play again? (Y/N): ")
        response = response.upper()
        if response == 'Y':
            playing_hand = True
            print( "\n"*5 )
            break
        elif response == 'N':
            print("Thanks for playing!")
            playing_blackjack = False
        else:
            print("Please enter Y for Yes or N for No")
