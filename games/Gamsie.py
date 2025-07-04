import streamlit as st
import random
import string
import os

# Try to import enchant with fallback
try:
    import enchant
    enchant_available = True
except ImportError:
    st.warning("Warning: 'pyenchant' not found. Word validation will be disabled. Install with 'pip install pyenchant'.")
    enchant_available = False

# WordGames base class
class WordGames:
    def __init__(self, G):
        self.number_of_players = 0
        self.game = G
    
    def playerName(self, key_prefix=""):
        name = st.text_input("Enter the player's name:", key=f"{key_prefix}_player_name").strip()
        if not name:
            st.error("Name cannot be empty.")
            return None
        return name
    
    def randomGenerator(self, num):
        if self.game.lower() in ["scrabble", "spellathon"]:
            return [random.choice(string.ascii_uppercase) for _ in range(num)]
        elif self.game.lower() == "scramble":
            try:
                if not os.path.exists("corncob_lowercase.txt"):
                    st.error("Error: 'corncob_lowercase.txt' not found in the current directory.")
                    return [], []
                with open("corncob_lowercase.txt", "r") as file:
                    words = file.read().splitlines()
                if not words:
                    st.error("Error: 'corncob_lowercase.txt' is empty.")
                    return [], []
                unshuffled = random.choices(words, k=num)
                shuffled = [''.join(random.sample(list(word.upper()), len(word))) for word in unshuffled]
                return unshuffled, shuffled
            except Exception as e:
                st.error(f"Error loading word list: {str(e)}")
                return [], []
    
    def isValid(self, letters, word):
        if not word.isalpha():
            return False
        letters = letters.copy()
        for letter in word.upper():
            if letter in letters:
                letters.remove(letter)
            else:
                return False
        if enchant_available:
            try:
                d = enchant.Dict("en_US")
                return d.check(word.lower())
            except enchant.errors.DictNotFoundError:
                st.warning("English dictionary not found for validation. Validation skipped.")
                return True
        return True  # Fallback if enchant is not available

# Scrabble class
class Scrabble(WordGames):
    def __init__(self):
        self.score_chart = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
            'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
            'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
            'Y': 4, 'Z': 10
        }
        self.playerScore = []
        self.player = []
        self.number = 0
        super().__init__("Scrabble")
    
    def rules(self):
        st.markdown("""
        **Scrabble Rules**:
        - Each player is given 8 letters to create a valid English word.
        - Points are awarded based on the word's letters.
        - The player with the most points wins.
        - This is a multi-player, multi-round game.
        """)
    
    def players(self):
        self.number = st.number_input("Enter number of players:", min_value=1, step=1, key="scrabble_players")
        for i in range(self.number):
            name = st.text_input(f"Enter name of Player {i+1}:", key=f"scrabble_player_{i}").strip()
            if not name:
                st.error(f"Player {i+1} name cannot be empty.")
                return False
            self.player.append(name)
            self.playerScore.append(0)
        return True
    
    def calcScore(self, word):
        return sum(self.score_chart.get(letter, 0) for letter in word.upper())
    
    def game_Scrabble(self):
        if 'scrabble_round' not in st.session_state:
            st.session_state.scrabble_round = 1
        if 'scrabble_current_player' not in st.session_state:
            st.session_state.scrabble_current_player = 0
        if 'scrabble_letters' not in st.session_state:
            st.session_state.scrabble_letters = self.randomGenerator(8)[0]  # Use first element of tuple
        
        st.markdown(f"### Round {st.session_state.scrabble_round}")
        current_player = st.session_state.scrabble_current_player
        st.write(f"{self.player[current_player]}'s turn")
        st.write(f"Letters: {st.session_state.scrabble_letters}")
        
        word = st.text_input("Enter word (or 'E' to exit):", key=f"scrabble_word_{current_player}_{st.session_state.scrabble_round}").strip()
        if st.button("Submit Word", key=f"scrabble_submit_{current_player}_{st.session_state.scrabble_round}"):
            if word.upper() == 'E':
                st.markdown("### Exiting Simulation")
                st.markdown("**FINAL SCORES**")
                for j in range(self.number):
                    st.write(f"{self.player[j]}'s score = {self.playerScore[j]}")
                st.markdown("**GAME OVER**")
                st.write("Thank you for playing!")
                st.session_state.scrabble_game_over = True
            elif self.isValid(st.session_state.scrabble_letters, word):
                score = self.calcScore(word)
                self.playerScore[current_player] += score
                st.success(f"Valid word! Score = {score}")
            else:
                st.error("Invalid input, hence Score = 0")
            
            st.write("Current Scores:")
            for j in range(self.number):
                st.write(f"{self.player[j]}'s score = {self.playerScore[j]}")
            
            st.session_state.scrabble_current_player += 1
            if st.session_state.scrabble_current_player >= self.number:
                st.session_state.scrabble_current_player = 0
                st.session_state.scrabble_round += 1
                st.session_state.scrabble_letters = self.randomGenerator(8)[0]
            else:
                st.session_state.scrabble_letters = self.randomGenerator(8)[0]

# Spellathon class
class Spellathon(WordGames):
    def __init__(self):
        super().__init__("Spellathon")
        self.total_score = 0
    
    def rules(self):
        st.markdown("""
        **Spellathon Rules**:
        - Single Player Game.
        - Player is given 14 letters to form valid English words.
        - Scoring: 5-6 words = 10 points, 7-9 words = 15 points, 10 words = 20 points, each additional word beyond 10 gives 5 points.
        """)
    
    def calc_score(self, n):
        score = 0
        if 5 <= n <= 6:
            score = 10
        elif 7 <= n <= 9:
            score = 15
        elif n >= 10:
            score = 20 + (n - 10) * 5
        return score
    
    def game_Spellathon(self):
        if 'spellathon_round' not in st.session_state:
            st.session_state.spellathon_round = 1
        if 'spellathon_words' not in st.session_state:
            st.session_state.spellathon_words = []
        if 'spellathon_letters' not in st.session_state:
            st.session_state.spellathon_letters = self.randomGenerator(14)[0]
        if 'spellathon_word_count' not in st.session_state:
            st.session_state.spellathon_word_count = 0
        
        st.markdown(f"### Round {st.session_state.spellathon_round}")
        st.write(f"Letters: {st.session_state.spellathon_letters}")
        st.write("Start spinning your answers:")
        
        word = st.text_input(f"{st.session_state.spellathon_word_count + 1}. Enter word (or 'E' to end):", 
                            key=f"spellathon_word_{st.session_state.spellathon_round}_{st.session_state.spellathon_word_count}").strip()
        if st.button("Submit Word", key=f"spellathon_submit_{st.session_state.spellathon_round}_{st.session_state.spellathon_word_count}"):
            if word.upper() == 'E':
                score = self.calc_score(st.session_state.spellathon_word_count)
                self.total_score += score
                st.markdown(f"### Round {st.session_state.spellathon_round} Score: {score}")
                st.markdown(f"**Total Score for {st.session_state.spellathon_name}: {self.total_score}**")
                if st.button("Play another round?", key=f"spellathon_play_again_{st.session_state.spellathon_round}"):
                    st.session_state.spellathon_round += 1
                    st.session_state.spellathon_words = []
                    st.session_state.spellathon_letters = self.randomGenerator(14)[0]
                    st.session_state.spellathon_word_count = 0
                else:
                    st.markdown("### Exiting Simulation")
                    st.markdown(f"**Final Score for {st.session_state.spellathon_name}: {self.total_score}**")
                    st.write("Thank you for playing!")
                    st.session_state.spellathon_game_over = True
            elif word.upper() in st.session_state.spellathon_words:
                st.error("Already used word. Try again.")
            elif self.isValid(st.session_state.spellathon_letters, word):
                st.session_state.spellathon_words.append(word.upper())
                st.session_state.spellathon_word_count += 1
                st.success(f"Valid word: {word}!")
            else:
                st.error("Invalid word. Try again.")

# Scramble class
class Scramble(WordGames):
    def __init__(self):
        super().__init__("Scramble")
        self.score = 0
    
    def rules(self):
        st.markdown("""
        **Scramble Rules**:
        - Single Player Game.
        - In each round, a jumbled word is generated.
        - The player must unscramble it within 3 attempts.
        - Each correct word gives 4 points.
        """)
    
    def checker(self, word, correct_word):
        return word.lower() == correct_word.lower()
    
    def game_scramble(self):
        if 'scramble_round' not in st.session_state:
            st.session_state.scramble_round = 1
        if 'scramble_attempts' not in st.session_state:
            st.session_state.scramble_attempts = 3
        if 'scramble_words' not in st.session_state:
            st.session_state.scramble_words = []
        if 'scramble_correct_words' not in st.session_state:
            st.session_state.scramble_correct_words = []
        
        st.markdown(f"### Round {st.session_state.scramble_round}")
        if 'scramble_current_word' not in st.session_state or st.session_state.scramble_attempts == 3:
            unshuffled, shuffled = self.randomGenerator(1)
            if not unshuffled or not shuffled:
                st.error("Game cannot continue without word list.")
                st.session_state.scramble_game_over = True
                return
            st.session_state.scramble_current_word = unshuffled[0].upper()
            st.session_state.scramble_scrambled_word = shuffled[0]
        
        st.write(f"Scrambled word: {st.session_state.scramble_scrambled_word}")
        st.write(f"Attempts left: {st.session_state.scramble_attempts}")
        
        word = st.text_input("Your guess (Press 'E' to exit):", 
                            key=f"scramble_word_{st.session_state.scramble_round}_{st.session_state.scramble_attempts}").strip()
        if st.button("Submit Guess", key=f"scramble_submit_{st.session_state.scramble_round}_{st.session_state.scramble_attempts}"):
            if word.upper() == 'E':
                st.markdown("### Exiting Simulation")
                st.markdown(f"**Original words**: {', '.join(st.session_state.scramble_correct_words)}")
                st.markdown(f"**Scrambled words**: {', '.join(st.session_state.scramble_words)}")
                st.markdown(f"**FINAL SCORE for {st.session_state.scramble_name}: {self.score}**")
                st.write("Thank you for playing!")
                st.session_state.scramble_game_over = True
            else:
                st.session_state.scramble_words.append(st.session_state.scramble_scrambled_word)
                st.session_state.scramble_correct_words.append(st.session_state.scramble_current_word)
                if self.checker(word, st.session_state.scramble_current_word):
                    st.success(f"Correct answer! Score: {self.score}")
                    st.session_state.scramble_round += 1
                    st.session_state.scramble_attempts = 3
                else:
                    st.session_state.scramble_attempts -= 1
                    if st.session_state.scramble_attempts > 0:
                        st.error("Incorrect answer. Try again.")
                    else:
                        st.error(f"Out of attempts. Correct word was: {st.session_state.scramble_current_word}")
                        if st.button("Play another round?", key=f"scramble_play_again_{st.session_state.scramble_round}"):
                            st.session_state.scramble_round += 1
                            st.session_state.scramble_attempts = 3
                        else:
                            st.markdown("### Exiting Simulation")
                            st.markdown(f"**Original words**: {', '.join(st.session_state.scramble_correct_words)}")
                            st.markdown(f"**Scrambled words**: {', '.join(st.session_state.scramble_words)}")
                            st.markdown(f"**FINAL SCORE for {st.session_state.scramble_name}: {self.score}**")
                            st.write("Thank you for playing!")
                            st.session_state.scramble_game_over = True

# Streamlit App
st.title("Word Games Simulation")

if 'game_selected' not in st.session_state:
    st.session_state.game_selected = None
if 'game_initialized' not in st.session_state:
    st.session_state.game_initialized = False
if 'scrabble_game_over' not in st.session_state:
    st.session_state.scrabble_game_over = False
if 'spellathon_game_over' not in st.session_state:
    st.session_state.spellathon_game_over = False
if 'scramble_game_over' not in st.session_state:
    st.session_state.scramble_game_over = False

game = st.selectbox("Choose your game:", ["Select a game", "Scrabble", "Spellathon", "Scramble"], key="game_select")

if game != "Select a game" and not st.session_state.game_initialized:
    st.session_state.game_selected = game.lower()
    if game.lower() == "scrabble":
        st.session_state.game_obj = Scrabble()
    elif game.lower() == "spellathon":
        st.session_state.game_obj = Spellathon()
    elif game.lower() == "scramble":
        st.session_state.game_obj = Scramble()
    st.session_state.game_initialized = True

if st.session_state.game_selected:
    game_obj = st.session_state.game_obj
    game_obj.rules()
    
    if st.session_state.game_selected == "scrabble" and not st.session_state.scrabble_game_over:
        if 'scrabble_players_set' not in st.session_state:
            st.session_state.scrabble_players_set = False
        if not st.session_state.scrabble_players_set:
            if game_obj.players():
                st.session_state.scrabble_players_set = True
                st.session_state.scrabble_name = game_obj.player[0]  # Default to first player
        else:
            game_obj.game_Scrabble()
    elif st.session_state.game_selected == "spellathon" and not st.session_state.spellathon_game_over:
        if 'spellathon_name' not in st.session_state:
            name = game_obj.playerName(key_prefix="spellathon")
            if name:
                st.session_state.spellathon_name = name
        else:
            game_obj.game_Spellathon()
    elif st.session_state.game_selected == "scramble" and not st.session_state.scramble_game_over:
        if 'scramble_name' not in st.session_state:
            name = game_obj.playerName(key_prefix="scramble")
            if name:
                st.session_state.scramble_name = name
                st.write(f"Giddy up Player: {name}")
        else:
            game_obj.game_scramble()