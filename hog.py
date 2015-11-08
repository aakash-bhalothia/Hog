"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Must roll at least once.'
    # BEGIN Question 1
    x = 0
    total = 0
    rolled_one = True
    while(x < num_rolls):
        outcome = dice()
        if outcome == 1:
            rolled_one = False
        total += outcome
        x+=1
    if rolled_one == False:
        return 0
    else:
        return total
        

    # END Question 1


def is_prime(n):
    if n < 2:
        return False
    for k in range(2, n-1):
            if n % k ==0:
                return 
    return True
        
    
def next_prime(n):
    assert is_prime(n) == True, 'Argument should be a prime'
    n = n+1
    while is_prime(n) != True:
        n = n + 1
    return n
        
def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    total = roll_dice(num_rolls, dice)
    if num_rolls == 0:
        q = opponent_score//10
        r = opponent_score%10
        total = max(q,r) + 1
        
    if is_prime(total):
        total = next_prime(total)
    
    return total
    

            


        
    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
        # BEGIN Question 3
    total = score + opponent_score
    if total % 7 == 0:
        return four_sided
    else:
        return six_sided

    
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4

    if score0>100:
        score0 = score0 - 100
    if score1>100:
        score1 = score1 - 100
    score0_digit1 = score0%10
    score0_digit2 = score0//10
    score1_digit1 = score1%10
    score1_digit2 = score1//10

    if score0_digit1 == score1_digit2 and score0_digit2 == score1_digit1:
        return True
    else:
        return False

    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
   
    while score0<goal and score1<goal:
        dice = select_dice(score0, score1)

        if(who==0):
            num_rolls = strategy0(score0, score1)
            total = take_turn(num_rolls, score1, dice)
            if total == 0:
                score1 = score1 + num_rolls
            score0 += total

        if(who==1):
            num_rolls = strategy1(score1,score0)
            total = take_turn(num_rolls, score0, dice)
            if total == 0:
                score0 = score0 + num_rolls
            score1 += total

        if is_swap(score0, score1):
            score0, score1 = score1, score0

        who = other(who)

    

    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6
    def returnav(*args):
        k = 0
        result = 0
        while k<num_samples:
            result += fn(*args)
            k = k+1
        return result/num_samples
    return returnav

  
    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    x = 1
    maxnum = 1
    score = 0
    a = make_averaged(roll_dice, num_samples)
    maxscore= a(x, dice)
    while x<=10:
        b = make_averaged(roll_dice, num_samples)
        score = b(x, dice)
        if score > maxscore:
            maxscore = score
            maxnum = x
        x+=1
    return maxnum


    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    q = opponent_score//10
    r = opponent_score%10
    total = max(q,r) + 1
    if is_prime(total):
        total = next_prime(total)
    
    if total>=margin:
        return 0
    else:
        return num_rolls
  # Replace this statement
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    q = opponent_score//10
    r = opponent_score%10
    max_digit = max(q,r) + 1
    if is_prime(max_digit):
        max_digit = next_prime(max_digit)
    total = score + max_digit

    if is_swap(total, opponent_score) and total != opponent_score:
        total = opponent_score
        if total > score:
            return 0
        else:
            return num_rolls
    else:
        return num_rolls

    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    If our score is greater than opponent score, use bacon strategy. If not, 
    check if is_swap would be true and if it is, implement swap strategy. 
    Check then if it is possible to give the opponent a 4-sided dice, do bacon strategy 
    to make him do so. Finally, check if our score is pretty close to or exceeds 100 then 
    choose to roll 0 times. We also check if we roll 0, then if the turn score plus the total score does 
    not get swapped we go on to roll 0 and in case it does, we roll 1 dice.
    Finally, if our score combined with opponent_score is less than 50, make the margin higher (8) 
    and if it is below 70, make the margin = to .1 times the opponent_score. Return the number of 
    dice that should be rolled.
    """
    # BEGIN Question 10
    margin = 0.1 * opponent_score
    a = bacon_strategy(score, opponent_score, margin)
    if score>opponent_score:
        a = bacon_strategy(score, opponent_score, 5)
    elif is_swap(score, opponent_score):
        a = bacon_strategy(score, opponent_score) 
    elif opponent_score-score > 90:
        a = swap_strategy(score, opponent_score)
    q = opponent_score//10
    r = opponent_score%10
    total = max(q,r) + 1
    if is_prime(total):
        total = next_prime(total)
    elif select_dice(score+total, opponent_score) == four_sided and score+total<90:
        a = bacon_strategy(score, opponent_score, 0, 1)
    elif score+total>100 and is_swap(score+total, opponent_score) == False:
        a = 0
    if is_swap(score+total, opponent_score) and score>opponent_score:
        a = 1
    if is_swap(score+total, opponent_score) and opponent_score>score:
        a = 0
    if score+opponent_score<50 and is_swap(score+total, opponent_score) == False:
        a = bacon_strategy(score, opponent_score, 8,2)
    elif score+opponent_score<70 and is_swap(score+total, opponent_score) == False:
        a = bacon_strategy(score, opponent_score, margin, 2)

    return a
    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
