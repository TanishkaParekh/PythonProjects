import random  
import string

#generating a random list of letters for each player
def random_letterlist(n=8):
    return[random.choice(string.ascii_uppercase) for l in range(n)]

#each letter : said points
score_chart ={'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
    'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
    'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
    'Y': 4, 'Z': 10
}
#checking score for the player
def calcScore(word):
    sum = 0
    for letter in word.upper():
        sum += score_chart[letter]
    return sum

#checking if all letters used are from the list provided
def isValid(word, available):
    available = available.copy()
    for letter in word:
        if letter.upper() in available:
            available.remove(letter.upper())
        else:
            return False
    return True


#playing game
def game():
    print("Hello Players, welcome to this simulation of scrabble")
    print("Each of u will be given 8 letters using those u need to create a valid english word ")
    print("Based on your word u will be awarded points")
    print("Player with the maximum points shall be the winner")
    print("this is a multi player & multi round game ")
    print("press 'E' to exit simulaton")
    print("thank u so much and enjoy ur experience")
    print(" ")
    number = int(input("Enter number of Players playing "))
    player = []
    playerScore = []
    for i in range(number):
        name = input(f"Enter name of Player {i+1}: ")
        player.append(name)
        playerScore.append(0)
    k=1
    while True:
        print("Round",k)
        for i in range(number):
            
            letters = random_letterlist()
            print(player[i],"'s turn")
            print(letters)

            word = input("Enter word (or press 'E' to exit simulation)")
            word = word.upper()
            if(word=='E'):
                print("Exiting Simulation")
                print("FINAL SCORES")
                for j in range(number):
                            print(player[j],"'s score =",playerScore[j])
                print("GAME OVER")
                print("thank you for playing")
                print("see ya later")
                return;
            elif isValid(word,letters):
                score = calcScore(word)
                playerScore[i] +=score
                print("Valid word! Score =",score)
            else:
                print("invalid input , hence Score = 0")
            for j in range(number):
                print(player[j],"'s score =",playerScore[j])
            print()
        k +=1
    print("FINAL SCORES")
    for j in range(number):
                print(player[j],"'s score =",playerScore[j])
    print("GAME OVER")
game()



