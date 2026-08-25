class Player:
    """Represents a blackjack player"""
    
    def __init__(self, name, initial_balance=1000):
        self.name = name
        self.balance = initial_balance
        self.hand = None
        self.current_bet = 0
        self.is_playing = False
        self.is_doubled = False
        self.is_split = False
        
        # Stats tracking
        self.stats = {
            'total_hands': 0,
            'wins': 0,
            'losses': 0,
            'pushes': 0,
            'blackjacks': 0,
            'total_winnings': 0,
            'total_losses': 0
        }
    
    def place_bet(self, amount):
        """Place a bet"""
        if amount <= self.balance and amount > 0:
            self.current_bet = amount
            self.balance -= amount
            return True
        return False
    
    def win_bet(self, multiplier=1.0):
        """Win the current bet"""
        winnings = int(self.current_bet * (1 + multiplier))
        self.balance += winnings
        self.stats['total_winnings'] += winnings
        self.stats['wins'] += 1
    
    def lose_bet(self):
        """Lose the current bet"""
        self.stats['total_losses'] += self.current_bet
        self.stats['losses'] += 1
    
    def push_bet(self):
        """Push (tie) - return the bet"""
        self.balance += self.current_bet
        self.stats['pushes'] += 1
    
    def double_down(self, additional_bet):
        """Double down on current bet"""
        if additional_bet <= self.balance and additional_bet == self.current_bet:
            self.balance -= additional_bet
            self.current_bet *= 2
            self.is_doubled = True
            return True
        return False
    
    def split_hand(self):
        """Split hand (requires matching cards)"""
        if len(self.hand.cards) == 2 and self.hand.cards[0].rank == self.hand.cards[1].rank:
            if self.current_bet <= self.balance:
                self.balance -= self.current_bet
                self.is_split = True
                return True
        return False
    
    def reset_hand(self):
        """Reset hand for new round"""
        self.current_bet = 0
        self.is_doubled = False
        self.is_split = False
    
    def add_hand_played(self):
        """Increment hands played"""
        self.stats['total_hands'] += 1
    
    def add_blackjack(self):
        """Record a blackjack"""
        self.stats['blackjacks'] += 1
    
    def get_stats(self):
        """Get player statistics"""
        total_played = self.stats['total_hands']
        if total_played == 0:
            win_rate = 0
        else:
            win_rate = (self.stats['wins'] / total_played) * 100
        
        return {
            'name': self.name,
            'balance': self.balance,
            'hands_played': self.stats['total_hands'],
            'wins': self.stats['wins'],
            'losses': self.stats['losses'],
            'pushes': self.stats['pushes'],
            'blackjacks': self.stats['blackjacks'],
            'win_rate': f"{win_rate:.1f}%",
            'net_winnings': self.stats['total_winnings'] - self.stats['total_losses']
        }
    
    def can_afford_bet(self, amount):
        """Check if player can afford a bet"""
        return amount > 0 and amount <= self.balance
    
    def is_busted_out(self):
        """Check if player is out of money"""
        return self.balance <= 0


class Dealer:
    """Represents the dealer"""
    
    def __init__(self):
        self.hand = None
        self.is_playing = False
        self.stats = {
            'hands_dealt': 0,
            'natural_blackjacks': 0,
            'wins': 0,
            'pushes': 0
        }
    
    def should_hit(self):
        """Dealer hits on 16 or less, stands on 17 or more (hard 17 rule)"""
        value = self.hand.get_value()
        return value < 17
    
    def reset_hand(self):
        """Reset hand for new round"""
        self.hand = None
    
    def add_hand_dealt(self):
        """Increment hands dealt"""
        self.stats['hands_dealt'] += 1
    
    def add_blackjack(self):
        """Record a natural blackjack"""
        self.stats['natural_blackjacks'] += 1
    
    def add_win(self):
        """Record a win"""
        self.stats['wins'] += 1
    
    def add_push(self):
        """Record a push"""
        self.stats['pushes'] += 1
    
    def get_stats(self):
        """Get dealer statistics"""
        return {
            'hands_dealt': self.stats['hands_dealt'],
            'natural_blackjacks': self.stats['natural_blackjacks'],
            'wins': self.stats['wins'],
            'pushes': self.stats['pushes']
        }
