import random
from nltk.corpus import words

stages = ["", "___+___", "   |\n   |\n   |\n   |\n___+___", "   ___\n   |  |\n   |\n   |\n   |\n___+___", "   ___\n   |  |\n   |  0\n   |\n   |\n___+___","   ___\n   |  |\n   |  0\n   |  |\n   |\n___+___", "   ___\n   |  |\n   |  0\n   | \\|\n   |\n___+___", "   ___\n   |  |\n   |  0\n   | \\|/\n   |\n___+___", "   ___\n   |  |\n   |  0\n   | \\|/\n   | /\n___+___","   ___\n   |  |\n   |  0\n   | \\|/\n   | / \\\n___+___"]

scoreDictionary = {"a": 1, "b": 3, "c": 3, "d": 2, "e": 1, "f": 4, "g": 2, "h": 4, "i": 1, "j": 8, "k": 5, "l": 1, "m": 3, "n": 1, "o": 1, "p": 3, "q": 10, "r": 1, "s": 1, "t": 1, "u": 1, "v": 4, "w": 4, "x": 8, "y": 4, "z": 10}

score = 0
scores = []

def validity(msg, inputs, letters=[]):
    response = input(msg).lower()
    if inputs == "letter":
        while True:
            if not(response.isalpha() and len(response) == 1):
                response = input("That is not a valid letter. Guess: ").lower()
                continue
            if response in letters:
                response = input("That has already been guessed. Guess: ").lower()
                continue
            return response
    else:
        while response not in inputs:
            response = input("That is not a valid response. " + msg).lower()
        return response

# Starting game
start = validity("Would you like to play hangman (Y/n)? ", ["yes", "y", "no", "n", ""])

if start not in ["no", "n"]:
    # Mode setting
    mode = validity("Would you like to play easy mode (common words) or hard mode (obscure words) (E/h)? ", ["easy", "e", "hard", "h", ""])

    # Word bank
    if mode in ["easy", "e", ""]:
        words = words.words()[-850:]
    else:
        words = words.words()

# Check if started
while start not in ["no", "n"]:
    word = random.choice(words).lower()
    guesses = []
    wordSpace = []
    stage = 0

    for char in word:
        wordSpace.append("_")

    while True:
        # Display
        print(stages[stage])
        print(" ".join(wordSpace))
        print("Guesses: " + str(sorted(guesses)))

        # Get the guess and add it to the list of guesses
        letter = validity("Guess: ", "letter", guesses)
        guesses.append(letter)

        # Add letters if letter in word and finish round if word completed
        if letter in word:
            score += scoreDictionary[letter]
            for i in range(0, len(word)):
                if word[i] == letter:
                    wordSpace[i] = letter
            if not "_" in wordSpace:
                score += 2*(len(stages)-stage)
                print(" ".join(wordSpace))
                print("Congratulations! The word was " + word + ".")
                print("Your score is " + str(score) + ".")
                break
        # Go to next stage in hangman if letter not in word and check if game has ended
        else:
            print("Sorry, that isn't in the word.")
            stage += 1
            if stage == len(stages)-1:
                print("Sorry, you have lost. The word was " + word)
                print("Your score is " + str(score) + ".")
                break
    # Ask if the player wants to play again
    start = validity("Do you want to play again (Y/n)? ", ["yes", "y", "no", "n", ""])

# Show score and ask for name
name = input("Your final score is " + str(score) + ". What is your name? ")
name = name[0].upper() + name[1:].lower()

# Find place on leaderboard
place = 1

try:
    file = open('hangmanScores.txt', 'r')
    scores = file.read().splitlines()
    for player in scores:
        if int(player.split(" ")[-1]) > score or (int(player.split(" ")[-1]) == score and sorted([name, " ".join(player.split(" ")[:-1])])[1] == name):
            place += 1
    file.close()
except:
    pass

# Change place value to place word
if place%10 == 0 or place%10 == 1:
    place = str(place) + "st"
elif place%10 == 2:
    place = str(place) + "nd"
elif place%10 == 3:
    place = str(place) + "rd"
else:
    place = str(place) + "th"

# Ask if player wants to record score
record = validity("You are in " + place + " place. Would you like to record your score (Y/n)? ", ["yes", "y", "n", "no", ""])

# Record the score
if record in ["yes", "y", ""]:
    file = open('hangmanScores.txt', 'w')
    file.truncate(0)
    scores.insert(int(place[:-2])-1, name + " " + str(score))
    file.writelines("\n".join(scores))
    file.close()

# Print the top scores and the closing statement
print("The current top scores are: " + "\n".join(scores[0:3]))
print("Thank you for playing!")
