import pygame
import math

class Card3DRenderer:
    """Renders 3D cards using pygame"""
    
    def __init__(self, width=100, height=150):
        self.width = width
        self.height = height
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 20)
    
    def draw_card(self, surface, card, x, y, rotation=0, scale=1.0, face_up=True):
        """Draw a 3D-looking card"""
        w = int(self.width * scale)
        h = int(self.height * scale)
        
        if not face_up:
            # Draw card back (blue pattern)
            self._draw_card_back(surface, x, y, w, h)
        else:
            # Draw card front
            self._draw_card_front(surface, card, x, y, w, h)
    
    def _draw_card_back(self, surface, x, y, w, h):
        """Draw the back of a card"""
        # Outer shadow
        pygame.draw.rect(surface, (0, 0, 0), (x + 3, y + 3, w, h))
        
        # Card background (dark blue)
        pygame.draw.rect(surface, (25, 45, 100), (x, y, w, h))
        
        # Border
        pygame.draw.rect(surface, (200, 200, 200), (x, y, w, h), 3)
        
        # Pattern
        for i in range(0, h, 15):
            for j in range(0, w, 15):
                pygame.draw.line(surface, (50, 100, 150), (x + j, y + i), (x + j + 10, y + i + 10), 1)
    
    def _draw_card_front(self, surface, card, x, y, w, h):
        """Draw the front of a card"""
        # Outer shadow for 3D effect
        pygame.draw.rect(surface, (0, 0, 0), (x + 4, y + 4, w, h))
        
        # Card background (white)
        pygame.draw.rect(surface, (240, 240, 240), (x, y, w, h))
        
        # Border
        pygame.draw.rect(surface, (50, 50, 50), (x, y, w, h), 2)
        
        # Get suit color
        suit_color = card.SUIT_COLORS[card.suit]
        suit_symbol = card.SUIT_SYMBOLS[card.suit]
        
        # Draw rank and suit in corners
        rank_text = self.font_large.render(card.rank, True, suit_color)
        suit_text = self.font_small.render(suit_symbol, True, suit_color)
        
        # Top-left
        surface.blit(rank_text, (x + 5, y + 5))
        surface.blit(suit_text, (x + 8, y + 25))
        
        # Bottom-right (upside down)
        rank_rotated = pygame.transform.rotate(rank_text, 180)
        suit_rotated = pygame.transform.rotate(suit_text, 180)
        surface.blit(rank_rotated, (x + w - rank_rotated.get_width() - 5, y + h - rank_rotated.get_height() - 5))
        surface.blit(suit_rotated, (x + w - suit_rotated.get_width() - 8, y + h - suit_rotated.get_height() - 25))
        
        # Center design
        center_suit = self.font_large.render(suit_symbol, True, suit_color)
        center_x = x + (w - center_suit.get_width()) // 2
        center_y = y + (h - center_suit.get_height()) // 2
        surface.blit(center_suit, (center_x, center_y))


class Button:
    """Simple button class"""
    
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = tuple(min(255, c + 50) for c in color)
        self.is_hovered = False
        self.font = pygame.font.Font(None, 24)
    
    def draw(self, surface):
        """Draw the button"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(pos)
    
    def update(self, pos):
        """Update button state"""
        self.is_hovered = self.rect.collidepoint(pos)


class BettingPanel:
    """Panel for betting"""
    
    def __init__(self, x, y, width=300):
        self.x = x
        self.y = y
        self.width = width
        self.height = 200
        self.current_bet = 0
        self.min_bet = 10
        self.max_bet = 1000
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)
        
        # Buttons
        button_y = y + 100
        self.bet_buttons = [
            Button(x + 10, button_y, 60, 40, "$10", (100, 50, 50)),
            Button(x + 75, button_y, 60, 40, "$50", (100, 50, 50)),
            Button(x + 140, button_y, 60, 40, "$100", (100, 50, 50)),
            Button(x + 205, button_y, 60, 40, "$500", (100, 50, 50)),
        ]
        
        self.clear_button = Button(x + 10, button_y + 50, 90, 40, "Clear", (100, 100, 100))
        self.confirm_button = Button(x + 175, button_y + 50, 90, 40, "Bet", (50, 100, 50))
    
    def draw(self, surface):
        """Draw the betting panel"""
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)
        
        # Title
        title = self.font.render("Betting", True, (0, 0, 0))
        surface.blit(title, (self.x + 10, self.y + 10))
        
        # Current bet
        bet_text = self.small_font.render(f"Bet: ${self.current_bet}", True, (0, 0, 0))
        surface.blit(bet_text, (self.x + 10, self.y + 50))
        
        # Draw buttons
        for button in self.bet_buttons:
            button.draw(surface)
        
        self.clear_button.draw(surface)
        self.confirm_button.draw(surface)
    
    def handle_click(self, pos):
        """Handle button clicks"""
        for i, button in enumerate(self.bet_buttons):
            if button.is_clicked(pos):
                bet_amounts = [10, 50, 100, 500]
                self.current_bet += bet_amounts[i]
                if self.current_bet > self.max_bet:
                    self.current_bet = self.max_bet
        
        if self.clear_button.is_clicked(pos):
            self.current_bet = 0
    
    def get_bet(self):
        """Get current bet"""
        return self.current_bet
    
    def reset(self):
        """Reset bet"""
        self.current_bet = 0
    
    def update(self, pos):
        """Update button states"""
        for button in self.bet_buttons:
            button.update(pos)
        self.clear_button.update(pos)
        self.confirm_button.update(pos)
