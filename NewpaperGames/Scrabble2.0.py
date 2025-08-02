import random
import string
try:
    import enchant
except ImportError:
    print("Error: 'pyenchant' module not found. Please install it using 'pip install pyenchant'.")
    exit(1)

class WordGames:
    def __init__(self,G)-> None:
        self.number_of_players = 0
        self.game = G
        print("Hello Players, welcome to this simulation of",self.game)
        print("press 'E' to exit simulaton")
    def playerName(self):
        name= (input("enter the name")).strip()
        while not name:
            print("enter value")
            name= (input("enter the name")).strip()
        return name
    def randomGenerator(self,num):
        if self.game.lower() == "scrabble" or self.game.lower() == "spellathon":
            return [random.choice(string.ascii_uppercase) for _ in range(num)]
        elif self.game.lower() == "scramble":
            try:
                file = open("corncob_lowercase.txt","r")
                words = file.read()
                wordList =words.split("\n")
                list_of_words =random.choices(wordList,k=num)
                return list_of_words

            except FileNotFoundError:
                print("Word list file not found. Please ensure 'corncob_lowercase.txt' is in the same directory.")
                return []
    def isValid(self,list,word):
        if not word.isalpha():
            return False
        list = list.copy()
        for letter in word:
                if letter.upper() in list:
                    list.remove(letter.upper())
                else:
                    return False
        try:
            d = enchant.Dict("en_US")
            return d.check(word.lower())
        except enchant.errors.DictNotFoundError:
            print("Error: English dictionary not found for validation.")
            return False
        
class Scrabble(WordGames):
    def __init__(self):
        self.score_chart ={'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
            'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
            'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
        self.playerScore=[]
        self.player =[]
        self.number=0
        super().__init__("scrabble")
    def rules(self):
        print("Each of u will be given 8 letters using those u need to create a valid english word ")
        print("Based on your word u will be awarded points")
        print("Player with the maximum points shall be the winner")
        print("this is a multi player & multi round game ")
    def players(self):
        self.number = int(input("Enter number of Players playing "))
        for i in range(self.number):
            name = input(f"Enter name of Player {i+1}: ")
            self.player.append(name)
            self.playerScore.append(0)
    def calcScore(self,word):
        sum = 0
        for letter in word.upper():
            sum += self.score_chart[letter]
        return sum
    def game_Scrabble(self):
        k=1
        while True:
            print(f"\nRound {k}",)
            for i in range(self.number):
                letters = super().randomGenerator(8)
                print(self.player[i],"' s turn")
                print("Letter", letters)
                word = input("Enter word (or press 'E' to exit simulation)").strip()
                word = word.upper()
                if(word=='E'):
                    print("Exiting Simulation")
                    print("FINAL SCORES")
                    for j in range(self.number):
                        print(self.player[j],"'s score =",self.playerScore[j])
                    print("GAME OVER")
                    print("thank you for playing")
                    print("see ya later")
                    return
                elif super().isValid(letters,word):
                    score = self.calcScore(word)
                    self.playerScore[i] +=score
                    print("Valid word! Score =",score)
                else:
                    print("invalid input , hence Score = 0")
                for j in range(self.number):
                    print(self.player[j],"'s score =",self.playerScore[j])
                print()
            k +=1
class Spellathon(WordGames):
    def __init__(self):
        super().__init__("spellathon")
        self.total_score=0
    def rules(self):
        print("Single Player Game")
        print("Player will be given 14 letters.")
        print("Scoring: 5-6 words = 10 points, 7-9 words = 15 points, 10 words = 20 points")
        print("Each additional word beyond 10 gives 5 points.")
    def calc_score(self,n):
        score=0
        if n<5:
            score=n*1
        if n>=5 and n<=6:
            score=10
        elif n>=7 and n<=9:
            score=15
        elif n==10:
            score=20
        elif n>10:
            score = 20 + (n - 10) * 5
        return score
    def game_Spellathon(self):
        name =super().playerName()
        k=1
        while True:
            print("Round",k)
            letters = super().randomGenerator(14)
            print("Letters: ",letters)
            print("Start spinning your answers:")
            word =[]
            c=0
            while True:
                w= input(f"{c+1}.Enter word : ").strip()
                if w.upper() =='E':
                    print("Exiting Simulation")
                    break
                if w.upper() in word:
                    print("Already used Word Try Again")
                    continue
                if super().isValid(letters,w.upper()) == True:
                    word.append(w.upper())
                    c=c+1
                else:
                    print("invalid word try again")
            k=k+1
            score= self.calc_score(c) 
            self.total_score += score
            print("Final Score of",name,"=",self.total_score)
            print(f"Final Score for {name}: {self.total_score}")
            print("Thank you for playing!")
            
class Scramble(WordGames):
    def __init__(self):
        super().__init__("scramble")
        self.score=0
        
    def rules(self):
        print("Single Player Game")
        print("in each round a set of jumbled words are generated") 
        print("and the player shall have tp unscramble them ")
        print("every correct word gives the player 4 points")
    def checker(self,word,quest):
        if word.lower() == quest.lower():
            print("correct answer")
            print("eligible for next round")
            self.score +=4
            return True
        else:
            print("incorrect")
            return False
    def game_scramble(self):
        name = self.playerName()
        print("Giddy up Player :",name)
        round_number = 1
        while True:
            print(f"\n--- Round {round_number} ---")
            original_word = self.randomGenerator(1)
            if not original_word:
                print("Game cannot continue without word list.")
                return

            correct_word = original_word[0]
            scrambled = list(correct_word.upper())
            random.shuffle(scrambled)
            scrambled_word = ''.join(scrambled)

            print("Scrambled word:", scrambled_word)

            word = input("Your guess (Press 'E' to exit): ").strip()
            if word.upper() == 'E':
                print("\nExiting Simulation...")
                print("Original word was:", correct_word)
                print("FINAL SCORE:", self.score)
                return

            if self.checker(word, correct_word):
                round_number += 1
                continue

            # Give 2 more chances (3 total)
            for i in range(2):
                print(f"Chance {i+2}:")
                word = input("Try again: ").strip()
                if word.upper() == 'E':
                    print("\nExiting Simulation...")
                    print("Original word was:", correct_word)
                    print("FINAL SCORE:", self.score)
                    return
                if self.checker(word, correct_word):
                    break

            round_number += 1
if __name__ == "__main__":
    game = input("Choose your game Scrabble , Spellathon , Scramble ").strip()
    if game.lower() == "scrabble":
        scrabble_obj = Scrabble()
        scrabble_obj.rules()
        scrabble_obj.players()
        scrabble_obj.game_Scrabble()
    elif game.lower() == "spellathon":
        spell = Spellathon()
        spell.rules()
        spell.game_Spellathon()
    elif game.lower() == "scramble":
        scramble_obj = Scramble()
        scramble_obj.rules()
        scramble_obj.game_scramble()
    else :
        print("Oopsie nothing of that soughts with us")