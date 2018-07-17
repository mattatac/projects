import random, string, time

class Deck(object):
    def __init__(self):
        self.deck = [
            ['Ace of Spades', 11, 1], ['Ace of Hearts', 11, 1], ['Ace of Clubs', 11, 1], ['Ace of Diamonds', 11, 1],
            ['King of Spades', 10], ['King of Hearts', 10], ['King of Clubs', 10], ['King of Diamonds', 10],
            ['Queen of Spades', 10], ['Queen of Hearts', 10], ['Queen of Clubs', 10], ['Queen of Diamonds', 10],
            ['Jack of Spades', 10], ['Jack of Hearts', 10], ['Jack of Clubs', 10], ['Jack of Diamonds', 10],
            ['Ten of Spades', 10], ['Ten of Hearts', 10], ['Ten of Clubs', 10], ['Ten of Diamonds', 10],
            ['Nine of Spades', 9], ['Nine of Hearts', 9], ['Nine of Clubs', 9], ['Nine of Diamonds', 9],
            ['Eight of Spades', 8], ['Eight of Hearts', 8], ['Eight of Clubs', 8], ['Eight of Diamonds', 8],
            ['Seven of Spades', 7], ['Seven of Hearts', 7], ['Seven of Clubs', 7], ['Seven of Diamonds', 7],
            ['Six of Spades', 6], ['Six of Hearts', 6], ['Six of Clubs', 6], ['Six of Diamonds', 6],
            ['Five of Spades', 5], ['Five of Hearts', 5], ['Five of Clubs', 5], ['Five of Diamonds', 5],
            ['Four of Spades', 4], ['Four of Hearts', 4], ['Four of Clubs', 4], ['Four of Diamonds', 4],
            ['Three of Spades', 3], ['Three of Hearts', 3], ['Three of Clubs', 3], ['Three of Diamonds', 3],
            ['Two of Spades', 2], ['Two of Hearts', 2], ['Two of Clubs', 2], ['Two of Diamonds', 2]]
        self.current_card = 0

    def shuffle_deck(self):
        for i in range(10):
            random.shuffle(self.deck)
        print('Shuffling deck...')
        time.sleep(3)

    def deal_card(self):
        if self.current_card == 51:
            self.__init__()
            self.shuffle_deck()
        card = self.deck[self.current_card]
        self.current_card += 1
        return card

    def __str__(self):
        return str(self.deck)


class Hand(object):
    def __init__(self, deck, player):
        '''
        Takes in the deck that is in play as a list(deck) of lists(cards and values)
        and the player as a string, whether it's the computer dealer or human player.
        '''
        self.hand = [deck.deal_card(), deck.deal_card()]
        self.name = player
        
    def hit(self, deck):
        self.hand.append(deck.deal_card())

    def change_ace_value(self):
        for i in self.hand:
            if len(i) == 3:
                del i[1]
                break

    def eval_hand(self):
        tempTotal = 0
        aces = False
        for i in self.hand:
            tempTotal += i[1]
            if 'Ace' in i[0]:
                aces = True
        if tempTotal > 21:
            if aces:
                self.change_ace_value()

    def display_hand(self):
        self.eval_hand()
        text = '#     ' + self.name + "'s hand:\n"
        total = 0
        for i in self.hand:
            text = text + '#     - ' + str(i[0]) + ' (' + str(i[1]) + ')\n'
            total += i[1]
        text = text + '#     Total: ' + str(total) + '\n#'
        return text

    def get_hand_value(self):
        self.eval_hand()
        total = 0
        for i in self.hand:
            total += i[1]
        return total

    def __str__(self):
        return str(self.hand)

class Player(Hand):
    def __init__(self, name, cash = 100):
        self.cash = cash
        self.player = Hand.__init__(self, deck, name)

    def display_cash(self):
        return '$' + str(self.cash)

    def get_cash(self):
        return self.cash
    
class Dealer(Hand):
    def __init__(self, name):
        self.dealer = Hand.__init__(self, deck, name)

    def display_partial_hand(self):
        self.eval_hand()
        text = '#     ' + self.name + "'s hand:\n"
        firstCard = True
        for i in self.hand:
            if firstCard:
                text = text + '#     - ' + str(i[0]) + ' (' + str(i[1]) + ')\n'
                value = i[1]
                firstCard = False
            else:
                text = text + '#     - [Face down card]\n'
        text = text + '#     Total: ' + str(value) + '+\n#'
        return text

    def deal_card_check(self):
        card = deck.deck[deck.current_card]
        if dealer.get_hand_value() + card[1] > 21:
            return False
        else:
            return True

deck = Deck()
deck.shuffle_deck()
dealer = Dealer('Kyle')  

def main():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n===========================================================')
    print('==================== Blackjack Version 1.0 ====================\n')
    play = 'yes'
    first = True
    bust = False
    while play != 'n':
        try:
            if first:
                play = str.lower(input('Would you like to play? (Y or N):\n'))
            else:
                play = str.lower(input('Would you like to play again? (Y or N):\n'))
        except ValueError:
            print("Please enter a valid option. Typing 'N' will exit the game.")
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n======================================================')
        if play == 'n':
            break
        if play != 'y':
            print("Please enter a valid option. Typing 'N' will exit the game.")
        if play == 'y':
            while first or player.cash > 0:
                if first:
                    print('Welcome to the game!')
                    print('My name is ' + dealer.name + '. I will be your dealer today.\n')
                    player = Player(input('What is your name?\n'))
                    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n======================================================')
                    print('Hello, ' + str(player.name) + '!')
                else:
                    input('Nice round! Ready for the next one?')
                    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n======================================================')
                    player.__init__ (player.name, player.cash)
                    dealer.__init__(dealer.name)
                if first:
                    print('I will deal us both a hand.\n')
                else:
                    print('I will deal us both another hand.\n')
                print('# # # # # # # # # # # # # # # # # # #')
                print(player.display_hand())
                print(dealer.display_partial_hand())
                print('# # # # # # # # # # # # # # # # # # #\n')
                valid = False
                while not valid:
                    try:
                        bet = int(input('You have $' + str(player.cash) + '. How much would you like to bet?\n'))
                    except ValueError:
                        print('Please enter a valid amount.')
                    if 0 >= bet or  bet > player.cash:
                        print('Please enter a valid amount.')
                    else:
                        valid = True
                    print('\n\n======================================================')
                hit = True
                while hit:
                    try:
                        deal = str.lower(input('Would you like to hit? (Y or N):\n'))
                    except ValueError:
                        print("Please enter a valid option. Typing 'N' will end the round.")
                    if deal == 'n':
                        hit = False
                        break
                    elif deal == 'y':
                        player.hit(deck)
                        if player.get_hand_value() > 21:
                            hit = False
                            bust = True
                            break
                        print()
                        print('# # # # # # # # # # # # # # # # # # #')
                        print(player.display_hand())
                        print(dealer.display_partial_hand())
                        print('# # # # # # # # # # # # # # # # # # #\n')
                    else:
                        print("Please enter a valid option. Typing 'N' will end the round.")
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n========================================================')
                print('=====================ROUND OVER=======================')
                hit = True
                if not bust:
                    while dealer.get_hand_value() <= 16:
                        #if dealer.deal_card_check():
                        dealer.hit(deck)
                if dealer.get_hand_value() == player.get_hand_value():
                    print('Tie game.\n')
                    print('# # # # # # # # # # # # # # # # # # #')
                    print(player.display_hand())
                    print(dealer.display_hand())
                    print('# # # # # # # # # # # # # # # # # # #\n')
                elif bust or (dealer.get_hand_value() > player.get_hand_value() and dealer.get_hand_value() <= 21):
                    if bust:
                        print('You busted!')
                    print('I win!\n')
                    player.cash -= bet
                    print('# # # # # # # # # # # # # # # # # # #')
                    print(player.display_hand())
                    print(dealer.display_hand())
                    print('# # # # # # # # # # # # # # # # # # #\n')
                else:
                    print('Wow! You beat me...\n')
                    player.cash += bet
                    print('# # # # # # # # # # # # # # # # # # #')
                    print(player.display_hand())
                    print(dealer.display_hand())
                    print('# # # # # # # # # # # # # # # # # # #\n')
                play = 'yes'
                first = False
                bust = False
            print('You ran out of cash! Game over.')
            player.cash = 100
    print('Thanks for playing!\n')

main()
