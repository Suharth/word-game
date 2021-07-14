# Word Game

import random
import string


VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}



WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	




def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """

    score=0
    for letter in word:
        score+=SCRABBLE_LETTER_VALUES[letter]
    score*=len(word)
    if len(word)==n:
        score+=50
    return score




def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter+"("+str(SCRABBLE_LETTER_VALUES[letter])+")",end=" ")       # print all on the same line
    


def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand


def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    newhand={}
    #Make a copy of hand
    for key in hand:
        newhand[key]=hand[key]
    #Update newhand
    for letter in word:
        newhand[letter]-=1
    return newhand
    




def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    
    test1=False
    if word in wordList:
        test1=True
    wordDict=getFrequencyDict(word)
    test2=True
    for letter in wordDict:
        if wordDict[letter]>hand.get(letter,0):
            test2=False
            break
    return (test1 and test2)




def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    count=0
    for letter in hand:
        count+=hand[letter]
    return count



def playHand(wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    hand=dealHand(HAND_SIZE)
    score=0# Keep track of the total score
    
    # As long as there are still letters left in the hand:
    while(calculateHandlen(hand)>0):
        # Display the hand
        print("Current Hand:",end=" ")
        displayHand(hand)
        # Ask user for input
        word=input('Enter word, or a "." to indicate that you are finished:')
        # If the input is a single period:
        if word==".":
            # End the game (break out of the loop)
            break
            
        # Otherwise (the input is not a single period):
        else:
            # If the word is not valid:
            if not isValidWord(word, hand, wordList):
                # Reject invalid word (print a message followed by a blank line)
                print("Invalid word, please try again.")
                print()
                continue
            # Otherwise (the word is valid):
            else:
                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
                currentWordScore=getWordScore(word, n)
                score+=currentWordScore
                print('"'+word+'"',"earned",str(currentWordScore),"points. Total:",score,"points")
                print()
                # Update the hand 
                hand=updateHand(hand, word)

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    if calculateHandlen(hand)==0:
        print("You ran out of letters. Total score:",score,"points.")
    elif word==".":
        print("Oh! that's all you got? Total score:",score,"points.")
    return score



def multiplayer():
    '''
    Main function that makes the program interactive and calls other functions.

    '''
    print("Scoring:\n")
    print("->The score for the hand is the sum of the scores for each word formed.\n")
    print("->The score for a word is the sum of the points for letters in the word, multiplied by the length of the word, plus 50 points if all letters are used on the first word created.\n")
    print("->The score for each letter is shown in a bracket next to it.")
    while True:
        fancystuff="**********"
        print()
        print(fancystuff)
        print("Welcome to the word game!")
        players=int(input("Number of players:"))
        winScore=((players+1)//2)+1
        playerNames={}
        for i in range(1,players+1):
            playerNames[i]=input("Player-"+str(i)+":")
        print()
        print("First one to win",str(winScore),"rounds wins!")
        Round=1
        playerScores={1:0} #Random values stored which will be updated in the loop
        
        
        while max(playerScores.values())<winScore:
            playerRoundScore={}
            print()
            print(fancystuff,"ROUND",Round,fancystuff)
            for i in range(1,players+1):
                print(playerNames[i]+", your turn")
                playerRoundScore[i]=playHand(wordList, HAND_SIZE)
                print()
            Round+=1
            roundmax=max(playerRoundScore.values())
            count=0 #Counts how many players got the max score to check for draw
            for i in range(1,players+1):
                if playerRoundScore[i]==roundmax:
                    count+=1
                    winner=i
                if count>1:
                        print("Damn, the round ends in a tie!")
                        break
                elif i==players:
                        print(playerNames[winner],"wins the round!")
                        playerScores[winner]=playerScores.get(winner,0)+1
        print()
        
        for i in range(1,players+1):
            if playerScores[i]==winScore:
                print(playerNames[i],"wins the game!")
                print("CONGRATULATIONS, YOU LEGEND!")
                break
        
        
        playOption=input("Play again[Y/N]?")
        if playOption=='N':
            print("Thanks for playing! Hope you enjoyed! :)")
            break

if __name__ == '__main__':
    wordList = loadWords()
    multiplayer()


