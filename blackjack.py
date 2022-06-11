#!/usr/bin/env python
# coding: utf-8

# ## Import Required Modules

# In[1]:


import random
import time
import os
from IPython.display import clear_output


# ## Define Unchanging Values

# In[2]:


# Unchanging values
suits = ["Hearts♥️", "Diamonds♦️", "Spades♠️", "Clubs♣️"]
ranks = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
values = {"Ace": 11, # Default value of Ace is 11 unless total is greater than 21 in that case the value of Ace has to be changed to 1
          "Two": 2,
          "Three": 3,
          "Four": 4,
          "Five": 5,
          "Six": 6,
          "Seven": 7,
          "Eight": 8,
          "Nine": 9,
          "Ten": 10,
          "Jack": 10,
          "Queen": 10,
          "King": 10}

# Test ace conversion
# ranks = ["Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace", "Ace"]
# values = {"Ace": 11, # Default value of Ace is 11 unless total is greater than 21 in that case the value of Ace has to be changed to 1
#           "Two": 2,
#          }


# ## Create Card Object

# In[3]:


class Card:
    def __init__(self, suit: str, rank: str, faceup: bool = True):
        self.suit = suit
        self.rank = rank
        # First dealer card is facedown, so cards need to have a property that they're either faceup or facedown
        self.faceup = faceup
        self.value = values[rank]

    def flip(self):
        if self.faceup == True:
            self.faceup = False
            # Facedown cards are not counted towards total on the board until they are shown
            self.value = 0
        else:
            self.faceup = True
            self.value = values[self.rank]
            
    def ascii_version_of_card(*cards, return_string=True):
#     """
#     Instead of a boring text version of the card we render an ASCII image of the card.
#     :param cards: One or more card objects
#     :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
#     keep it as a list so that the dealer can add a hidden card in front of the list
#     """

    # we will use this to prints the appropriate icons for each card
        suits_name = ['Spades♠️', 'Diamonds♦️', 'Hearts♥️', 'Clubs♣️']
        suits_symbols = ['♠', '♦', '♥', '♣']
        rank_conversion = {"Ace": "Ace",
          "Two": "2",
          "Three": "3",
          "Four": "4",
          "Five": "5",
          "Six": "6",
          "Seven": "7",
          "Eight": "8",
          "Nine": "9",
          "Ten": "10",
          "Jack": "Jack",
          "Queen": "Queen",
          "King": "King"}
        # create an empty list of list, each sublist is a line
        lines = [[] for i in range(9)]

        for index, card in enumerate(cards):
            # ascii version of hidden cards
            if card.faceup == False:
                lines = ['┌─────────┐'] + ['│░░░░░░░░░│'] * 7 + ['└─────────┘']
                return '\n'.join(lines)
            # "King" should be "K" and "10" should still be "10"
            if rank_conversion[card.rank] == '10':  # ten is the only one who's rank is 2 char long
                rank = rank_conversion[card.rank]
                space = ''  # if we write "10" on the card that line will be 1 char to long
            else:
                rank = rank_conversion[card.rank][0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
                space = ' '  # no "10", we use a blank space to will the void
            # get the cards suit in two steps
            suit = suits_name.index(card.suit)
            suit = suits_symbols[suit]

            # add the individual card on a line by line basis
            lines[0].append('┌─────────┐')
            lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
            lines[2].append('│         │')
            lines[3].append('│         │')
            lines[4].append('│    {}    │'.format(suit))
            lines[5].append('│         │')
            lines[6].append('│         │')
            lines[7].append('│       {}{}│'.format(space, rank))
            lines[8].append('└─────────┘')

        result = []
        for index, line in enumerate(lines):
            result.append(''.join(lines[index]))

        # hidden cards do not use string
        if return_string:
            return '\n'.join(result)
        else:
            return result

    
    def __str__(self) -> str:
        if self.faceup == True:
            return f"{self.rank} of {self.suit}"
        else:
            return f"A facedown card"


# ## Create Deck Object

# In[4]:


class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def draw_card(self, faceup: bool = True):
        # check if you want the card to be drawn face up or face down
        if faceup == True:
            # if the card property of the one you're about to pick out (pop default index is -1) is set to False, flip it
            if self.all_cards[-1].faceup == False:
                self.all_cards[-1].flip()
                return self.all_cards.pop()
            else: 
                return self.all_cards.pop()
        # check if you want the card to be drawn face up or face down
        elif faceup == False:
            # if the card property of the one you're about to pick out is set to True, flip it
            if self.all_cards[-1].faceup == True:
                self.all_cards[-1].flip()
                return self.all_cards.pop()
            else: 
                return self.all_cards.pop()
    
    def reset(self):
        Deck.__init__(self)
    
    def __str__(self) -> str:
        return f"Deck has {len(self.all_cards)} cards"

# Instantiate deck
blackjack_deck = Deck()


# ## Create Dealer Object

# In[5]:


class Dealer:
        
    def __init__(self, points: int = 0):
        self.points = points
        self.dealer_hand = []
    
    def get_points(self):
        self.points = sum(Card.value for Card in self.dealer_hand)
        return self.points
    
    # pick up cards
    def pickup(self):
        # If this is the first card in the dealer's hand, pickup facedown
        if len(self.dealer_hand) == len([]):
            self.dealer_hand.append(blackjack_deck.draw_card(faceup = False))
            self.get_points()
        # Otherwise pick it up and place it face up on the table
        else:
            self.dealer_hand.append(blackjack_deck.draw_card(faceup = True))
            self.get_points()

    # flip any cards that are face down (and reveal their value)        
    def show_cards(self):
        for index, card in enumerate(self.dealer_hand):
            if card.faceup == False:
                card.flip()
                self.dealer_hand[index] = card
                self.get_points()
    
    def reset(self):
        Dealer.__init__(self)
            
    def __str__(self) -> str:
        gen_exp = (card for card in self.dealer_hand)
        new_list = []
        for x in gen_exp:
            new_list.append(Card.ascii_version_of_card(x))
        lines = [card.splitlines() for card in new_list]
        zipped_lines = list(zip(*lines))
        formatted_card_output_side_by_side = ""
        for index, line in enumerate(list(zipped_lines)):
            formatted_card_output_side_by_side += "".join(list(zipped_lines)[index]) + "\n"
        nl = '\n'
        if len(self.dealer_hand) < 1:
            return f"Dealer has {len(self.dealer_hand)} cards and {self.get_points()} points"
        else:
            return f"Dealer has {len(self.dealer_hand)} cards and {self.get_points()} points \n{formatted_card_output_side_by_side}"
        
# Instantiate dealer
dealer = Dealer()


# ## Create Player Object

# In[6]:


class Player:

    def __init__(self,
                 name: str = "You",
                 money: int = 1000,
                 points: int = 0,
                 current_bet: int = 0,
                 wins: int = 0,
                 losses: int = 0,
                 standing: bool = False,
                 at_table: bool = True
                 ):
        self.name = name
        self.money = money
        self.points = points
        self.current_bet = current_bet
        self.wins = wins
        self.losses = losses
        self.standing = standing
        self.at_table = at_table
        self.player_hand = []

    def get_points(self):
        self.points = sum(Card.value for Card in self.player_hand)
        return self.points

    def bet(self):
        # DISREGARD: every round, can place bet up to $1000. Also have to make sure you have enough money to bet
#         if self.money >= 1000:
#             acceptable_betting_range = range(1, 1001)  # Bet from $1-$1000
#             betting_amount_available = 1000
#         else:
        acceptable_betting_range = range(1, self.money + 1)  # Bet from $1-available money
        betting_amount_available = self.money

        # Keep asking until a valid response is given
        betting_amount = ""
        betting_amount_int = 0
        while (betting_amount.isdigit() is False) or (betting_amount_int not in acceptable_betting_range):
            print(f"Place your bet (you have ${betting_amount_available} available for betting)")
            betting_amount = input()

            # check if input is valid
            if betting_amount.isdigit() is False:
                print("Not a valid betting amount. Please input a whole number")
            elif int(betting_amount) not in acceptable_betting_range:
                betting_amount_int = int(betting_amount)
                print(f"Not a valid betting amount. Please choose a number between 1 and {betting_amount_available}")

            # if input is valid
            else:
                self.current_bet = int(betting_amount)
                self.money -= self.current_bet
                break

#         print("\n"*100) 
        print("\n")
        print(f"You have bet ${self.current_bet} and have ${self.money} total")

    def pickup(self):
        self.player_hand.append(blackjack_deck.draw_card(faceup=True))
        self.get_points()

    def hit(self):
        self.pickup()
        self.get_points()
        print('"Hit me!"')

#     def insurance(self):
#         pass
        
#     def double_down(self):
#         pass

#     def split(self):
#         pass

    def stand(self):
        self.standing = True
        print(f"{self.name} stands")
        
    def leave_table(self):
        self.at_table = False

    def win(self):
        self.wins += 1

    def lose(self):
        self.losses += 1

    def reset_cards(self):
        self.player_hand = []
        self.points = 0
        self.standing = False

    def reset_money(self, amount: int = 1000):
        self.money = amount
        self.current_bet = 0

    def reset_wins_and_losses(self):
        self.wins = 0
        self.losses = 0

    def full_reset(self):
        Player.__init__(self, name=self.name)

    def __str__(self) -> str:
        gen_exp = (card for card in self.player_hand)
        new_list = []
        for x in gen_exp:
            new_list.append(Card.ascii_version_of_card(x))
        lines = [card.splitlines() for card in new_list]
        zipped_lines = list(zip(*lines))
        formatted_card_output_side_by_side = ""
        for index, line in enumerate(list(zipped_lines)):
            formatted_card_output_side_by_side += "".join(list(zipped_lines)[index]) + "\n"
        nl = '\n'
        if len(self.player_hand) < 1:
            return f"{self.name.title()} has {len(self.player_hand)} cards and {self.get_points()} points"
        else:
            return f"{self.name.title()} has {len(self.player_hand)} cards and {self.get_points()} points \n{formatted_card_output_side_by_side}"


# ## Create Function With Blackjack Game Logic

# In[7]:


def blackjack():
    # Set function for asking to play again
    def play_again():
        acceptable_responses = {"yes": "yes",
                                "y": "yes",
                                "no": "no",
                                "n": "no"
                                }
        response = ""
        while response.lower() not in acceptable_responses.keys():
            print("Do you want to play again?")
            response = input().lower()

            # Check if response is valid
            if response.lower() not in acceptable_responses.keys():
                print("""
Please give a valid response.
For Yes, type: Yes, yes, Y, or y
For No, type: No, no, N, or n
                """)
            else:
                break

        if acceptable_responses[response] == "yes":
            return "yes"
        else:
            return "no"

    def hit_or_stand():
        nonlocal player # need this for player to be in the scope of this function for some reason
        acceptable_responses = {"hit": "hit",
                                "h": "hit",
                                "y": "hit",
                                "1": "hit",
                                "stand": "stand",
                                "s": "stand",
                                "n": "stand",
                                "2": "stand"
                                }

        response = ""
        while response.lower() not in acceptable_responses.keys():
            print("Hit or Stand?")
            response = input().lower()

            # Check if response is valid
            if response.lower() not in acceptable_responses.keys():
                print("""
            Please give a valid response.
            For Hit, type: Hit, hit, H, h, Y, y, or 1
            For Stand, type: Stand, stand, S, s, N, n, or 2
                                """)
            else:
                break

        # This runs either player.hit() or player.stand()
        eval("player." + acceptable_responses[response] + "()")
            
        
    # Set function to display complex print statements
    def output(option: str) -> str:
        if option == "play_again":
            return f"""
{player.name.title()}'s wins: {player.wins}
{player.name.title()}'s losses: {player.losses}

{player.name.title()}'s money: {player.money}
            """
        if option == "show_table":
            return f"""
{player.name.title()}'s wins: {player.wins}
{player.name.title()}'s losses: {player.losses}

{player.name.title()}'s money: {player.money}
{player.name.title()}'s bet: {player.current_bet}

{'-' * os.get_terminal_size()[0]}
{player}



{dealer} 
{'-' * os.get_terminal_size()[0]}
            """
        if option == "dealer_about_to_check_his_cards":
            return f"""
{player.name.title()}'s wins: {player.wins}
{player.name.title()}'s losses: {player.losses}

{player.name.title()}'s money: {player.money}
{player.name.title()}'s bet: {player.current_bet}

{'-' * os.get_terminal_size()[0]}
{player}



Dealer checks his cards...

{dealer} 
{'-' * os.get_terminal_size()[0]}
            """

    def ace_check_player():
        index_list = []
        for index, card in enumerate(player.player_hand):
            if card.value == 11:
                index_list.append(index)

        while player.points > 21:
            for index in index_list:
                player.player_hand[index].value = 1
                player.get_points()
                # check if value of hand is below 21 (check here allows some aces to be 11)
                if player.points > 21:
                    continue
                else:
                    break

            if player.points > 21:
                return "bust"
                break
            else:
                return player.points
                break

    def ace_check_dealer():
        index_list = []
        for index, card in enumerate(dealer.dealer_hand):
            if card.value == 11:
                index_list.append(index)

        while dealer.points > 21:
            for index in index_list:
                dealer.dealer_hand[index].value = 1
                dealer.get_points()
                # check if value of hand is below 21 (check here allows some aces to be 11)
                if dealer.points > 21:
                    continue
                else:
                    break

            if dealer.points > 21:
                return "bust"
                break
            else:
                return dealer.points
                break

    def check_if_beat_dealer():
        # Scenarios for if dealer goes over 21 
        #(you already checked for if you busted before standing so don't have to take those scenarios into account)
        if dealer.points > 21 and (player.points == 21) and (len(player.player_hand) == 2):
            print(f"BLACKJACK! {player.name.title()} wins!")
            print(f"Payout is 2.5x your initial bet. You recieve ${int(2.5 * player.current_bet)}.")
            player.win()
            player.money += int(2.5 * player.current_bet)
            ### INSERT PAYOUT (your initial bet back + 1.5x your initial bet matched by the dealer)
        elif dealer.points > 21:
            print(f"Dealer busts. {player.name.title()} wins!")
            print(f"Payout is 2x your initial bet. You recieve ${2 * player.current_bet}.")
            player.win()
            player.money += 2* player.current_bet
            ### INSERT PAYOUT (your initial bet back + your initial bet matched by the dealer))
        
        # Scenarios for if the dealer doesn't go over 21
        else:
            if player.points == dealer.points:
                print("It's a tie!")
                print(f"Your betting amount is returned (${player.current_bet}).")
                # Return betting money
                player.money += player.current_bet
                ### INSERT PAYOUT (PROBABLY NOTHING)
            elif (player.points > dealer.points) and (player.points == 21) and (len(player.player_hand) == 2):
                print(f"BLACKJACK! {player.name.title()} wins!")
                print(f"Payout is 2.5x your initial bet. You recieve ${int(2.5 * player.current_bet)}.")
                player.win()
                player.money += int(2.5 * player.current_bet)
                ### INSERT PAYOUT (your initial bet back + 1.5x your initial bet matched by the dealer)
            elif player.points > dealer.points:
                print(f"{player.name.title()} wins!")
                print(f"Payout is 2x your initial bet. You recieve ${2 * player.current_bet}.")
                player.win()
                player.money += 2* player.current_bet
                ### INSERT PAYOUT (your initial bet back + your initial bet matched by the dealer))
            else:
                print("Dealer wins")
                print(f"You lose ${player.current_bet}.")
                player.lose()

    print("\n"*100)
    # Set player name for player instance

    player_name = ""
    while player_name == "":
        print("What is your name?")
        player_name = input()

        # check if name is valid
        if player_name == "":
            print("Please enter a valid name")
        else:
            break

    # Create instances
    ## Need to have instantiated deck outside of blackjack function for all the methods to act upon in (scope)
    blackjack_deck.reset()
    blackjack_deck.shuffle()
    dealer = Dealer()
    player = Player(name=player_name)

    # Set toggle variable (turn game off when round is done)
    game_on = True

    # check if game is on
    while game_on == True:

        # check if player has left the table
        if player.at_table == False:
            if player.money > 1000:
                print(f"Congrats! You have left the table with ${player.money}. Thank you for playing!")
            else:
                print(f"You have left the table with ${player.money}. Better luck next time!")
            game_on = False
            break

        # Initiate betting
        player.bet()

        # Initiate dealing (player gets dealt first)
        player.pickup()
        dealer.pickup()
        player.pickup()
        dealer.pickup()

        # variable for breaking out of loop
        y_or_n = ""
        bankrupt = False
        
        # Inner while loop executed until stand is said or bust
        # Round ends when player stands or busts
        while player.standing == False:

            # check if player has bust
            if player.points > 21:
                # check if player has Ace(s) in their hand and reduce their value
                checked = ace_check_player()  # This function does that

                if checked == "bust":
                    print(output("show_table"))
                    time.sleep(2)
                    print("BUST: You lose")
                    time.sleep(2)
                    player.lose()
                    
                    # check if money left
                    if player.money <= 0:
                        print("Game is over! You are bankrupt")
                        bankrupt = True
                        break

                    print(output("play_again"))

                    y_or_n = play_again()

                    if y_or_n == "yes":
                        dealer.reset()
                        player.reset_cards()
                        blackjack_deck.reset()
                        blackjack_deck.shuffle()
                        print("\n"*100)
                        break
                    elif y_or_n == "no":
                        player.leave_table()
                        ### PRINT HOW MUCH MONEY THEY MADE
                        break

            # Print out information
            print(output("show_table"))
            
            # Game logic
            hit_or_stand()
            ace_check_player()
            print("\n"*100)

        # Code in this indentation gets executed if player is standing
        
        # break out of outer loop
        if bankrupt == True:
            break
        if y_or_n == "yes" or y_or_n == "no":
            continue

        
        print(output("show_table"))

        # Dealer checks his card
        print("\n"*100)
        print(output("dealer_about_to_check_his_cards"))
        time.sleep(3)
        dealer.show_cards()
        ace_check_dealer()
        print("\n"*100)
        print(output("show_table"))
        time.sleep(3)
        while dealer.points <= 16:
            print("Dealer picks up a card")
            dealer.pickup()
            ace_check_dealer()
            time.sleep(1)
        
        print("\n"*100)
        print(output("show_table"))
        time.sleep(1)
        print("\n")
        check_if_beat_dealer()
        
        # check if money left
        if player.money <= 0:
            print("Game is over! You are bankrupt")
            break
        
        print(output("play_again"))
        
        y_or_n = play_again()

        if y_or_n == "yes":
            dealer.reset()
            player.reset_cards()
            blackjack_deck.reset()
            blackjack_deck.shuffle()
            print("\n"*100)
        elif y_or_n == "no":
            player.leave_table()
        


# ## Play Blackjack

# In[8]:


blackjack()


# ## Convert Jupyter Notebook to Python Script

# In[11]:


# get_ipython().system('jupyter nbconvert --to script blackjack.ipynb')
# the following commands clean up the file to be used in the terminal
## print("\n"*100) doesn't work outside of jupyter notebook, so equivalent command in other environment would be print("\\n"*100) (pushes everything out of view)
## exclude changing the clear_output() string in the sed command using # get_ipython().system/ ! (see here for more info https://stackoverflow.com/questions/38694081/executing-terminal-commands-in-jupyter-notebook)
## add a comment to all these unix commands in this block (which are executed by # get_ipython().system()) in python
# get_ipython().system('sed \'/# get_ipython().system/ ! s/clear_output()/print("\\\\n"*100)/g\' blackjack.py | sed \'s/# get_ipython().system/# # get_ipython().system/g\' > tempfile.py')
# get_ipython().system('mv tempfile.py blackjack.py')

