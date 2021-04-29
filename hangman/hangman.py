import random
import string
from words import words
from hangman_visual import lives_visual_dict


def get_valid_word(words):
    word = random.choice(words) #randomly chooses a word from the list
    
    #we don't want a word with spaces or dashes in it
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()

def hangman():

    word = get_valid_word(words)
    word_letters = set(word) #letters in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set() #what the user has guessed

    lives = 7

    while len(word_letters) > 0 and lives > 0:
        #letters used
        #' '.join(['a','b','cd]) --> 'a b cd'
        print('You have ',lives,' lives left\n','You have used these letters: ',' '.join(used_letters))

        #current word is ie. W - O R D
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print(lives_visual_dict[lives])
        print('Current Word: ',' '.join(word_list))

        #get user input to guess the word
        user_letter = input('Guess a letter: ').upper()

        #new guess that does has not been used before and is in the word
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')
            else:
                lives -= 1
                print(f"Your letter {user_letter} is not in the word.")

        #already used this guess before
        elif user_letter in used_letters:
            print("You have already used that character. Please try again!.")
    
        else:
            print("Invalid character. Please try again. ")

    #gets here when len(word_letters) == 0 OR when lives == 0
    if lives == 0:
        print('You died, sorry, the word was ',word)
    else:
        print('You guessed the word ',word,'!!')
    
hangman()