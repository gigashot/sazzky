from datetime import datetime

class BettingSystem:
    def __init__(self):
        self.bets = {
            1: {'total': 0, 'players': {}},
            2: {'total': 0, 'players': {}},
            3: {'total': 0, 'players': {}}
        }
        self.commission_rate = 0.10  # 10% commission komise
    
    def place_bet(self, player_name: str, bet_option: int, amount: float) -> bool:
        """
        Place a bet for a player.
        Returns True if bet was placed successfully, False otherwise.
        """
        if bet_option not in [1, 2, 3]:
            return False
        # 
        if amount <= 0:
            return False
            
        # Calculate commission and net bet
        commission = amount * self.commission_rate
        net_bet = amount - commission
        
        # Save commission to file
        self._save_commission(player_name, commission)
        
        # Update bet totals and player info
        self.bets[bet_option]['total'] += net_bet
        if player_name in self.bets[bet_option]['players']:
            self.bets[bet_option]['players'][player_name] += net_bet
        else:
            self.bets[bet_option]['players'][player_name] = net_bet
            
        return True
    
    def _save_commission(self, player_name: str, commission: float):
        """Save commission to a text file with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("commissions.txt", "a") as f:
            f.write(f"{timestamp} - Player: {player_name}, Commission: czk{commission:.2f}\n")
    
    def distribute_winnings(self, winning_option: int) -> Dict[str, float]:
        """
        Distribute winnings to players who chose the correct option.
        Returns a dictionary of player names and their winnings.
        """
        if winning_option not in [1, 2, 3]:
            return {}
            
        # Calculate total pot (excluding winning option)
        total_pot = sum(self.bets[opt]['total'] for opt in self.bets if opt != winning_option)
        
        # Get winners and their bets
        winners = self.bets[winning_option]['players']
        if not winners:
            return {}
            
        total_winning_bets = self.bets[winning_option]['total']
        
        # Calculate and distribute winnings
        winnings = {}
        for player, bet_amount in winners.items():
            # Winner gets their original bet plus a proportion of the pot
            proportion = bet_amount / total_winning_bets
            player_winnings = bet_amount + (total_pot * proportion)
            winnings[player] = player_winnings
            
        return winnings
    
    def get_bet_totals(self) -> Dict[int, float]:
        """Return the total amount bet on each option."""
        return {opt: data['total'] for opt, data in self.bets.items()}
    
    def get_player_bets(self, bet_option: int) -> Dict[str, float]:
        """Return all players and their bets for a specific option."""
        if bet_option not in [1, 2, 3]:
            return {}
        return self.bets[bet_option]['players']

# Example usage:
def main():
    betting_system = BettingSystem()
    
    while True:
        print("\nBetting System")
        print("1. Place Bet / Vsadit")
        print("2. View Bet Totals / Zobrazit vsazené částky")
        print("3. Call Winners / Vyhlásit vítěze")
        print("4. Exit / Konec")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            name = input("Enter your name / Zadejte své jméno: ")
            try:
                print("1. The G.O.A.T (0/0/0)")
                print("2. Iceman (0/1/0)")
                print("3. no contest / remíza ")
                bet_option = int(input("Choose / Vybererte (1/2/3): "))
                amount = float(input("Enter bet amount czk: "))
                if betting_system.place_bet(name, bet_option, amount):
                    print(" Bet placed successfully! / Sázka byla úspěšně umístěna!")
                else:
                    print("Invalid bet option or amount! / Neplatná volba sázky nebo částka!") 
            except ValueError:
                print("Invalid input! / Neplatný vstup!")
                
        elif choice == "2":
            totals = betting_system.get_bet_totals()
            print("\nCurrent Bet Totals:")
            for option, total in totals.items():
                print(f"Option {option}: czk{total:.2f}")
                
        elif choice == "3":
            try:
                print("1. The G.O.A.T (0/0/0)")
                print("2. Iceman (0/1/0)")
                print("3. no contest / remíza ")
                winning_option = int(input("Enter winning option (1-3): "))
                winnings = betting_system.distribute_winnings(winning_option)
                print("\nWinnings Distribution:")
                for player, amount in winnings.items():
                    print(f"{player}: czk{amount:.2f}")
            except ValueError:
                print("Invalid input!")
                
        elif choice == "4":
            print("Goodbye! / Nashledanou!")
            break
            
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()