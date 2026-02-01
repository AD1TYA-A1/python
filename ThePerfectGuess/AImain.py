"""
Enhanced Number Guessing Game
Players guess a random number between 1-100, and the one with the fewest guesses wins!
"""

import random
import os


class NumberGuessingGame:
    """Main game class to handle the guessing game logic"""
    
    def __init__(self, min_num=1, max_num=100):
        self.min_num = min_num
        self.max_num = max_num
        self.secret_number = None
        self.score_file = "leaderboard.txt"
        
    def generate_number(self):
        """Generate a random number within the specified range"""
        self.secret_number = random.randint(self.min_num, self.max_num)
        return self.secret_number
    
    def get_valid_input(self, prompt):
        """Get valid integer input from user with error handling"""
        while True:
            try:
                value = int(input(prompt))
                if self.min_num <= value <= self.max_num:
                    return value
                else:
                    print(f"Please enter a number between {self.min_num} and {self.max_num}!")
            except ValueError:
                print("Invalid input! Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                exit()
    
    def play_round(self, player_name):
        """Play one round of the game for a player"""
        print(f"\n{'='*50}")
        print(f"🎮 {player_name}'s Turn!")
        print(f"{'='*50}")
        print(f"I've chosen a number between {self.min_num} and {self.max_num}")
        print("Try to guess it in as few attempts as possible!\n")
        
        self.generate_number()
        attempts = 0
        guesses_history = []
        
        while True:
            guess = self.get_valid_input(f"Attempt #{attempts + 1} - Enter your guess: ")
            attempts += 1
            guesses_history.append(guess)
            
            if guess == self.secret_number:
                print(f"\n🎉 Congratulations {player_name}! You got it!")
                print(f"The number was {self.secret_number}")
                print(f"Total attempts: {attempts}")
                if len(guesses_history) > 1:
                    print(f"Your guesses: {', '.join(map(str, guesses_history))}")
                return attempts
            elif guess > self.secret_number:
                print("📉 Lower Number Please!")
            else:
                print("📈 Higher Number Please!")
            
            # Give a hint after 5 attempts
            if attempts == 5:
                range_hint = abs(guess - self.secret_number)
                if range_hint <= 10:
                    print("💡 Hint: You're very close!")
                elif range_hint <= 20:
                    print("💡 Hint: You're getting warm!")
    
    def save_score(self, player_name, score):
        """Save or update player score in the leaderboard"""
        # Create file if it doesn't exist
        if not os.path.exists(self.score_file):
            with open(self.score_file, "w") as f:
                f.write(f"{player_name}:{score}\n")
            return
        
        # Read existing scores
        scores = {}
        with open(self.score_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and ":" in line:
                    name, player_score = line.split(":", 1)
                    scores[name.strip()] = int(player_score.strip())
        
        # Update score only if it's better (lower)
        if player_name not in scores or score < scores[player_name]:
            scores[player_name] = score
            print(f"🏆 New best score for {player_name}!")
        else:
            print(f"Your best score remains: {scores[player_name]}")
        
        # Write updated scores
        with open(self.score_file, "w") as f:
            for name, player_score in scores.items():
                f.write(f"{name}:{player_score}\n")
    
    def display_leaderboard(self):
        """Display the current leaderboard"""
        if not os.path.exists(self.score_file):
            print("\n📊 No leaderboard data yet. Be the first to play!")
            return
        
        scores = {}
        with open(self.score_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and ":" in line:
                    name, score = line.split(":", 1)
                    scores[name.strip()] = int(score.strip())
        
        if not scores:
            print("\n📊 No leaderboard data yet. Be the first to play!")
            return
        
        # Sort by score (ascending - fewer attempts is better)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        
        print(f"\n{'='*50}")
        print("🏆 LEADERBOARD - Best Scores (Fewest Attempts)")
        print(f"{'='*50}")
        
        for rank, (name, score) in enumerate(sorted_scores, 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
            print(f"{medal} {rank}. {name}: {score} attempts")
        print(f"{'='*50}\n")


def main():
    """Main function to run the game"""
    game = NumberGuessingGame()
    
    print("╔" + "═"*48 + "╗")
    print("║" + " "*10 + "NUMBER GUESSING GAME" + " "*18 + "║")
    print("╚" + "═"*48 + "╝")
    
    # Display leaderboard at start
    game.display_leaderboard()
    
    while True:
        # Get player name
        player_name = input("\n👤 Enter your name (or 'quit' to exit): ").strip()
        
        if player_name.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for playing! Goodbye!")
            game.display_leaderboard()
            break
        
        if not player_name:
            print("Name cannot be empty!")
            continue
        
        # Play the round
        score = game.play_round(player_name)
        
        # Save the score
        game.save_score(player_name, score)
        
        # Ask if they want to continue
        print("\n" + "-"*50)
        continue_game = input("Play another round? (yes/no): ").strip().lower()
        
        if continue_game in ['no', 'n']:
            print("\n👋 Thanks for playing!")
            game.display_leaderboard()
            break
        elif continue_game not in ['yes', 'y']:
            print("Invalid choice. Showing leaderboard and exiting.")
            game.display_leaderboard()
            break


if __name__ == "__main__":
    main()