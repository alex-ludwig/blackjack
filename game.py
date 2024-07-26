import banking
import random 

'''
Black Jack.
- Card
- Deck of 52 Cards
- Table
- Game

# GAME PLAY
- Create Players
    - Player & Dealer : Bank, Holding
    - Table : Bet, Laid
A
- Minimum Bet ok?
- Player Bets : input with amount next to it
- Money Deposited on the table, dealer matches
B
- Card Deal: 
    
    - Check card sum
    - Check game status
    - Option: Hit or Stand
    - Repeat A or STAND
    - Next Player : Back to B
C
- Win/Loose : money for the winner, check accounts, 
- Back to A

'''

class Player():
    
    def __init__(self, name="Player, Dealer", deposit = 0):
        
        self.name = name
        self.account = banking.Account(name, deposit)
        self.hand = []
        self.buy_in = False
        

# CARDS

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

# sets up each card
class Card():

    # Defines A Card
    def __init__(self, suit = "Hearts",rank = "Two"):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    # returns Card Value
    def __str__(self):
        return(self.rank + " of " +  self.suit)


#two_hearts = Card(suits[0],ranks[0])
#two_hearts.value

# sets up the deck with cards
# controls hits
class Deck(Card):

    def __init__(self):
        self.all_cards = []
        
        for suit in suits:
            for rank in ranks:
                self.all_cards.append( Card(suit, rank) )
        
        self.len = len(self.all_cards)
        
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    
    def hit(self):
        # Note we remove one card from the list of all_cards
        try:
            self.len -= 1
            # print (f"The Card {self.all_cards[-1]} has been flipped")
            return self.all_cards.pop()
        except:
            print ("No more cards = Game Over")

#deck = Deck()
#deck.shuffle()


# sets up the game table
# controls buy in, pay back, deal
class Table(Deck):
    
    def __init__(self):
        
        self.deck = Deck()
        self.deck.shuffle()
        
    def buy_in(self):
        
        #print("Ready to Deal")
        game.pot += game.player.account.withdraw(game.buy_in)
        game.pot += game.dealer.account.withdraw(game.buy_in)
        
    def pay_back(self):
        #self.winner.account.deposit(game.pot)
        pass
    
    def reset_table(self):
        self.deck = Deck()
        self.deck.shuffle()
    
    def deal(self, playing, n = 1):
        
        for x in range(n):
            playing.hand.append(self.deck.hit())


# sets up the game: players, dealer, table.
# changes player

# initial values
deposit = 500
house = 1000000

class Game(Table, Player):
    on = False
    
    def __init__(self, on = False, pot = 0, buy_in = 0):

        self.player = Player("player", deposit)
        self.dealer = Player("dealer", house)
        
        # SETS PLAYER
        self.playing = self.player
        
        # SETS MAIN ATTRIBUTES
        self.on = on
        self.pot = pot
        self.buy_in = buy_in
        
        # SETS THE TABLE
        self.table = Table()
        
    def change_player(self):
        
        if self.playing == game.player: 
            return game.dealer
        else: 
            return game.player
    
    # ace check
    def ace_check(self, playing, total):
        playing.aces = []
        for card in playing.hand:
            if card.value == 11:
                print("ACE")
                playing.aces.append(card)
            if len(playing.aces) > 1 and total > 10:
                total -= 10
                return total
        else:
            return total     
        
#player = Player("player", 500)
#dealer = Player("dealer", 1000000)

# aux function to return the sum of a list
def get_sum(card_list):
    return sum([card.value for card in card_list])


def run_game(game):
    
    def reset_game():
        game.player.hand = []
        game.dealer.hand = []
        game.table.reset_table()
        game.winner = ""
        game.on = True
    
    while game.on:

        cash = game.player.account.balance
        game.pot = 0

        if cash < game.buy_in:
            game.on = False
            print(f"CASH: {cash}")
            print("No money to play. Get out!")

        else:
            game.check = False
            game.wait = True

            while game.wait:
                game.playing = game.player

                print(f"{game.playing.name.capitalize()}, your balance is: {game.playing.account.balance}")
                print(f"The Buy In Cost is: {game.buy_in}")
                reply = input("Would you like to play? (Yes or No) ")

                if(reply.upper() == "YES" or reply.upper() == "Y"):
                    reset_game()
                    game.wait = False
                    game.check = True
                    print("\n## Game Starting ##")
                    pass
                else:
                    game.winner = ""
                    game.wait = False
                    game.on = False
                    print("\nPlay another time. Goodbye!")
                    break
                    #reply = input("Please answer correctly: (Yes or No) ")

            # check money
            game.table.buy_in()

            # deal cards
            game.table.deal(game.player,2)
            game.table.deal(game.dealer,1)


            # check cards loop
            while game.check:

                # shortcuts
                current = game.playing
                #print(f"\n## {current.name.upper()} IS ON ##", "\n")

                # dealer gets another card
                if len(game.dealer.hand) == 1 and game.playing == game.dealer:
                    game.table.deal(game.dealer, 1)

                #gets the hand values
                hand_values = [card.value for card in current.hand]
                other_values = [card.value for card in game.change_player().hand]

                # ACES CHECK
                current_hand_total = game.ace_check(current, sum(hand_values))
                other_hand_total = game.ace_check(game.change_player(), sum(other_values))

                #display cards
                print(f"\n{current.name.capitalize()}")
                print(f"Hand: {' '.join(str(hand_values))} x {' '.join(str(other_values))}")
                #main value after Aces check  
                print(f"{current.name.capitalize()} Total: {current_hand_total} x {sum(other_values)}")

                ## MAIN CHECKS 
                #
                # DEALER HIT OR END
                if current_hand_total in range(17, 21) and current == game.dealer:

                    if get_sum(game.player.hand) > current_hand_total:
                        game.winner = game.player
                    else:
                        game.winner = current

                    game.check = False

                # CURRENT HITS
                elif current_hand_total < 18:

                    #print(f"{current.name.upper()} HITS","\n")
                    game.table.deal(current, 1)



                else:
                    # CURRENT STAY
                    if current_hand_total in range(18,21):

                        game.playing = game.change_player()

                    # CURRENT WINS
                    elif current_hand_total == 21:

                        game.winner = current
                        game.check = False

                    # CURRENT LOSES    
                    else:
                        game.winner = game.change_player()
                        game.check = False



            if not game.winner == "":
                game.winner.account.deposit(game.pot)
                print(f"\n## {game.winner.name.upper()} WINS {game.pot}! ##\n")
                print("\n##################################################\n")
                game.buy_in = game.pot
            
                
                #break

            #game.on = False
            
            
game = Game(True, 0, 20)
run_game(game)


'''
OUTPUT:

Player, your balance is: 500
The Buy In Cost is: 20
Would you like to play? (Yes or No) Yes

'''
