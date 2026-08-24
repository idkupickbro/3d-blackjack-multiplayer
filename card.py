import math

class Card:
    """Represents a playing card"""
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    SUIT_SYMBOLS = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
    SUIT_COLORS = {'Hearts': (255, 0, 0), 'Diamonds': (255, 0, 0), 'Clubs': (0, 0, 0), 'Spades': (0, 0, 0)}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def get_value(self):
        """Returns the blackjack value of the card"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Aces are handled specially in hand calculation
        else:
            return int(self.rank)
    
    def __str__(self):
        return f"{self.rank}{self.SUIT_SYMBOLS[self.suit]}"
    
    def __repr__(self):
        return f"Card({self.suit}, {self.rank})"


class Deck:
    """Represents a shoe of cards (multiple decks shuffled together)"""
    
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.cards = []
        self.reset()
    
    def reset(self):
        """Reset and shuffle the deck"""
        self.cards = []
        for _ in range(self.num_decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    self.cards.append(Card(suit, rank))
        self.shuffle()
    
    def shuffle(self):
        """Shuffle the deck"""
        import random
        random.shuffle(self.cards)
    
    def draw(self):
        """Draw a card from the deck"""
        if len(self.cards) < len(self.cards) * 0.25:  # Reshuffle when 25% remains
            self.reset()
        return self.cards.pop()
    
    def cards_remaining(self):
        return len(self.cards)


class Hand:
    """Represents a hand of cards"""
    
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """Add a card to the hand"""
        self.cards.append(card)
    
    def get_value(self):
        """Calculate the best value of the hand"""
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                value += 11
            else:
                value += card.get_value()
        
        # Adjust for aces if busted
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self):
        """Check if hand is a blackjack (21 with 2 cards)"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def is_bust(self):
        """Check if hand is busted"""
        return self.get_value() > 21
    
    def clear(self):
        """Clear the hand"""
        self.cards = []
    
    def __str__(self):
        return ' '.join(str(card) for card in self.cards)
