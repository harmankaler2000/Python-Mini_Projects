import random

def play():
    user = input("What's your choice? :'r' for rock, 'p' for paper, 's' for scissors \n")
    print(f"You chose {user}")

    computer = random.choice(['r','p','s'])
    print(f"The computer chose {computer}")
    
    if user == computer:
        return 'It\'s a tie'
    
    #r > s, s > p, p > r
    if is_win(user, computer):
        return 'You won!'
    
    #no need for else statement or
    #if is_win(computer, user)
    #as all the possibilities for the user to win 
    #have already been checked
    return 'You lost!'

def is_win(player, opponent):
    #return true if player wins
    #r > s, s > p, p > r
    if (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponent == 'r'):
        return True
print(play())