import random, string, time

def test_Die():
    # Test Die object
    print('Test Die Object: ', end = '')
    die1 = Die()
    die2 = Die(10)
    die3 = Die(20)
    dice = [die1, die2, die3]

    passed = 'Pass'
    for die in dice:
        tempDict = {}
        for num in range(die._sides):
            tempDict[num + 1] = num + 1
        for roll in range(die._sides * 10):
            if 1 > roll > die._sides:
                passed = 'Fail'
            try:
                del tempDict[die.roll_die()]
            except KeyError:
                pass
        if tempDict != {}:
            passed = 'Fail'
    return passed

def test_Loaded_Die():
    # Test Loaded Die object
    print('Test Loaded Die Object: ', end = '')
    die1 = Loaded_Die(4)
    die2 = Loaded_Die(7,10)
    die3 = Loaded_Die(19,20)
    dice = [die1, die2, die3]

    passed = 'Pass'
    for die in dice:
        tempDict = {}
        try:
            for roll in range(die._sides * 10):
                if 1 > roll > die._sides:
                    passed = 'Fail'
                if tempDict[roll+1]:
                    tempDict[roll+1] += 1
                else:
                    tempDict[roll+1] = 0
            if tempDict[die._load_num] < (die._sides/2)*10:
                passed = 'Fail'
        except KeyError:
            pass
    return passed

def test_Cup():
    #Test Cup object
    print('Test Loaded Die Object: ', end = '')
    cup1 = Cup(5, 0, 1, 6, 1)
    cup2 = Cup(0, 5, 4, 6, 1)
    cup3 = Cup(20, 20, 10, 20, 1)
    cups = [cup1, cup2, cup3]

    passed = 'Pass'
    for cup in cups:
        MIN = (cup._num_normal + cup._num_loaded) * cup._interval
        MAX = (cup._num_normal + cup._num_loaded) * cup._num_sides * cup._interval
        if MIN > cup.roll_dice() > MAX:
            passed = 'Fail'
    return passed


class Die(object):
    def __init__(self, sides=6):
        '''
        sides(int)  - Initialize number of sides (defaults to 6).
        '''
        self._sides = sides

    def roll_die(self):
        '''
        Returns new value (int) for rolled die.
        '''
        return random.randint(1,self._sides)

class Loaded_Die(Die):
    '''
    A die with a user-defined loaded value
    that will be the roll result 50% of the time.
    '''
    def __init__(self, load_num, sides=6):
        '''
        num(int) - set the loaded value.
        sides(int) - set number of sides the die has.
        
        Initialize new die object and assign the rolled
        value and loaded value to a list (self._chance).
        '''
        Die.__init__(self, sides)
        self._load_num = load_num
        self._chance = []
        for i in range(sides):
            self._chance.append(i+1)
        for i in range(sides - 2):
            self._chance.append(self._load_num)

    def roll_die(self):
        '''
        Reassign the random roll value to index 0
        on self._chance.
        
        Value for loaded die roll will be randomly
        chosen between two values in self._chance.
        
        Returns new value (int) for rolled loaded die.
        '''
        return random.choice(self._chance)
        
    

class Cup(object):
    '''
    Cup object to hold multiple rolled dice.
    '''
    def __init__(self, num_normal, num_loaded, load_value, num_sides, interval):
        '''
        Create new dictionary to store cup contents.
        '''
        self._num_normal = num_normal
        self._num_loaded = num_loaded
        self._num_sides = num_sides
        self._interval = interval
        self._contents = {}
        counter = 1
        for i in range(num_normal):
            newDie = Die(num_sides)
            self._contents[counter] = newDie
            counter += 1
        for i in range(num_loaded):
            newDie = Loaded_Die(load_value, num_sides)
            self._contents[counter] = newDie
            counter += 1

    def roll_dice(self):
        '''
        dice(dict) - all normal and loaded dice in cup

        Takes cup contents and calculates the total
        value from each rolled die.
        
        Returns the total value of rolled dice (int).
        '''
        total = 0
        for die in self._contents:
            total += self._contents[die].roll_die()
        return total


def get_num_dice():
    '''
    Get number of dice to roll from the user.
    '''
    num_dice = 0
    while num_dice < 1:
        try:
            num_dice = int(input('How many dice would you like to roll?\n'))
        except ValueError:
            print('Invalid value. Please enter an integer.')
        if num_dice < 1:
            print('Invalid value. Please enter a positive integer.')
    return num_dice

def get_refer_dice(num_dice):
    '''
    String variable for referring to either single/multiple REGULAR die.
    '''
    if num_dice == 1:
        return  'die'
    else:
        return  'dice'
    
def get_num_sides(refer_dice):
    '''
    Get number of sides for each die from user.
    '''
    num_sides = 0
    while num_sides < 2:
        try:
            num_sides = int(input('How many sides should the ' + refer_dice + ' have?\n'))
        except ValueError:
            print('Invalid value. Please enter an integer.')
        if num_sides < 2:
            print('Invalid value. The ' + refer_dice + 'must have at least 2 sides.')
    return num_sides

def get_interval(refer_dice):
    '''
    Get interval number between values of each side from user.
    '''
    interval = 0
    while interval < 1:
        try:
            interval = int(input('What interval should there be between each side value on the ' + refer_dice + '?\n(e.g. A starndard die has an interval of 1 with side values of 1, 2, 3, 4, 5, and 6)\n'))
        except ValueError:
            print('Invalid value. Please enter an integer.')
        if interval < 1:
            print('Invalid value. Please enter a positive integer.')
    return interval

def get_num_loaded(num_dice):
    '''
    See if the user wants any loaded dice, and how many.
    '''
    num_loaded = -1
    while num_loaded < 0:
        try:
            if num_dice == 1:
                num_loaded = int(input("Would you like the die to be loaded? Enter '1' for yes and '0' for no.\n"))
            else:
                num_loaded = int(input('How many of the dice should be loaded? Enter a number from 0 to ' + str(num_dice) + '.\n'))
        except ValueError:
            print('Invalid value. Please enter an integer.')
        if num_loaded < 0 or num_loaded > num_dice:
            print('Invalid value. Please enter a number from 0 to ' + str(num_dice) + '.')
            num_loaded = -1
    return num_loaded

def get_load_value(refer_loaded, num_loaded, num_sides):
    '''
    Get loaded value from user (if there are any loaded dice)
    '''
    load_value = 0
    while load_value < 1 or load_value > num_sides:
        try:
            if num_loaded > 0:
                load_value = int(input('What number should be assigned to the loaded ' + refer_loaded + '? This number has a 50% chance of being rolled each time.\n'))
            else:
                load_value = 1
        except ValueError:
            print('Invalid value. Please enter an integer.')
        if load_value < 1 or load_value > num_sides:
            print('Invalid value. Please enter a number from 1 to ' + str(num_sides) + '.')
    return load_value



def main():
    print('Welcome to DICE ROLL!\n')
    playing = True
    
    while playing:
        # Get number of dice to roll from the user.
        num_dice = get_num_dice()

        # Get's a string for how to refer to the number of dice the user has selected.
        refer_dice = get_refer_dice(num_dice)

        # Get number of sides for each die from user.
        num_sides = get_num_sides(refer_dice)

        # Get interval number between values of each side from user.
        interval = get_interval(refer_dice)

        # See if the user wants any loaded dice, and how many.
        num_loaded = get_num_loaded(num_dice)

        # Get's a string for how to refer to the number of LOADED dice the user has selected.
        refer_loaded = get_refer_dice(num_loaded)

        # Get loaded value from user (if there are any loaded dice)
        load_value = get_load_value(refer_loaded, num_loaded, num_sides)

        # Determine number or regular dice
        num_normal = num_dice - num_loaded

        # Roll the die/dice
        if num_normal == 1 == num_dice:
            die = Die(num_sides)
            print('Rolling a ' + str(num_sides) + '-sided die with an interval of ' + str(interval) + '...')
            time.sleep(2)
            print(die.roll_die() * interval)
        elif num_loaded == 1 == num_dice:
            die = Loaded_Die(load_value, num_sides)
            print('Rolling a ' + str(num_sides) + '-sided loaded die with an interval of ' + str(interval) + ' set to ' + str(load_value) + '...')
            time.sleep(2)
            print(die.roll_die() * interval)
        else:
            print('Rolling ' + str(num_normal) + ' normal and ' + str(num_loaded) + ' loaded ' + str(num_sides) + '-sided dice with an interval of ' + str(interval) + '...')
            time.sleep(2)
            cup = Cup(num_normal, num_loaded, load_value, num_sides, interval)
            print(cup.roll_dice())


        # Ask the user if they want to roll again.
        play_again = input("\n\nWould you like to roll some new dice? Enter anything other than 'y' to end the game.\n")
        if play_again != 'y':
            playing = False


##print(test_Die())
##print(test_Loaded_Die())
##print(test_Cup())
##print()
##print()
##time.sleep(1)
main()

