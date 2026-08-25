import pygame
import sys
import math
from game_logic import BlackjackGame, Player
from card_renderer import Card3DRenderer, Button, BettingPanel

class BlackjackUI:
    """Main UI and game renderer"""
    
    def __init__(self, width=1400, height=900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("3D Multiplayer Blackjack")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game
        self.game = BlackjackGame()
        self.game.add_player("Player 1")
        self.game.add_player("Player 2")
        self.game.add_player("Player 3")
        
        # Renderer
        self.card_renderer = Card3DRenderer()
        
        # Betting
        self.betting_panels = {}
        for i, player in enumerate(self.game.players):
            x = 50 + i * (self.width - 100) // len(self.game.players)
            self.betting_panels[player.name] = BettingPanel(x, self.height - 250)
        
        # Buttons
        self.hit_button = Button(self.width // 2 - 150, self.height - 80, 100, 50, "Hit", (100, 50, 50))
        self.stand_button = Button(self.width // 2 - 25, self.height - 80, 100, 50, "Stand", (50, 100, 50))
        self.bet_button = Button(self.width // 2 + 100, self.height - 80, 100, 50, "Place Bet", (50, 50, 100))
        
        self.current_player_bets = {}
        self.game.start_round()
    
    def handle_events(self):
        """Handle pygame events"""
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEMOTION:
                self.hit_button.update(pos)
                self.stand_button.update(pos)
                self.bet_button.update(pos)
                for panel in self.betting_panels.values():
                    panel.update(pos)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.game_state == 'betting':
                    for panel in self.betting_panels.values():
                        panel.handle_click(pos)
                    
                    if self.bet_button.is_clicked(pos):
                        self.place_bets()
                
                elif self.game.game_state == 'playing':
                    if self.hit_button.is_clicked(pos):
                        self.game.player_hit()
                    elif self.stand_button.is_clicked(pos):
                        self.game.player_stand()
        
        return True
    
    def place_bets(self):
        """Place bets for all players"""
        all_bet = True
        for player in self.game.players:
            panel = self.betting_panels[player.name]
            bet = panel.get_bet()
            if bet == 0:
                all_bet = False
                break
            try:
                player.place_bet(bet)
                panel.reset()
            except ValueError:
                pass
        
        if all_bet:
            self.game.deal_initial_cards()
    
    def draw(self):
        """Draw the game"""
        self.screen.fill((0, 100, 0))  # Green table
        
        # Draw title
        title = self.font_large.render("3D Multiplayer Blackjack", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # Draw dealer area
        dealer_x = self.width // 2 - 100
        dealer_y = 100
        
        # Dealer label
        dealer_label = self.font_medium.render("Dealer", True, (255, 255, 255))
        self.screen.blit(dealer_label, (dealer_x, dealer_y))
        
        # Dealer cards (only show first card initially, then all cards)
        card_x = dealer_x
        for i, card in enumerate(self.game.dealer.hand.cards):
            # In playing state, only show dealer's first card
            if self.game.game_state == 'playing' and i > 0:
                self.card_renderer.draw_card(self.screen, None, card_x, dealer_y + 40, face_up=False)
            else:
                self.card_renderer.draw_card(self.screen, card, card_x, dealer_y + 40, face_up=True)
            card_x += 70
        
        if self.game.game_state in ['dealer_turn', 'results']:
            dealer_value = self.font_small.render(f"Value: {self.game.dealer.hand.get_value()}", True, (255, 255, 255))
            self.screen.blit(dealer_value, (dealer_x, dealer_y + 170))
        
        # Draw players
        player_spacing = (self.width - 100) // len(self.game.players)
        for i, player in enumerate(self.game.players):
            player_x = 50 + i * player_spacing
            player_y = self.height // 2 - 100
            
            # Player label and balance
            color = (255, 255, 0) if i == self.game.current_player_index and self.game.game_state == 'playing' else (255, 255, 255)
            player_label = self.font_medium.render(player.name, True, color)
            self.screen.blit(player_label, (player_x, player_y))
            
            balance_text = self.font_small.render(f"Balance: ${player.balance}", True, (255, 255, 255))
            self.screen.blit(balance_text, (player_x, player_y + 35))
            
            if player.bet > 0:
                bet_text = self.font_small.render(f"Bet: ${player.bet}", True, (255, 200, 0))
                self.screen.blit(bet_text, (player_x, player_y + 60))
            
            # Player cards (only show own cards or dealer reveal)
            card_x = player_x
            for card in player.hand.cards:
                self.card_renderer.draw_card(self.screen, card, card_x, player_y + 90, face_up=True)
                card_x += 70
            
            # Player status
            if self.game.game_state in ['playing', 'dealer_turn', 'results']:
                hand_value = self.font_small.render(f"Value: {player.hand.get_value()}", True, (255, 255, 255))
                self.screen.blit(hand_value, (player_x, player_y + 160))
                
                if player.busted:
                    status = self.font_small.render("BUSTED!", True, (255, 0, 0))
                    self.screen.blit(status, (player_x, player_y + 190))
                elif player.standing:
                    status = self.font_small.render("STAND", True, (0, 255, 0))
                    self.screen.blit(status, (player_x, player_y + 190))
        
        # Draw message
        if self.game.message:
            msg = self.font_medium.render(self.game.message, True, (255, 255, 0))
            self.screen.blit(msg, (self.width // 2 - msg.get_width() // 2, 300))
        
        # Draw buttons and betting panels
        if self.game.game_state == 'betting':
            for panel in self.betting_panels.values():
                panel.draw(self.screen)
            self.bet_button.draw(self.screen)
        
        elif self.game.game_state == 'playing':
            self.hit_button.draw(self.screen)
            self.stand_button.draw(self.screen)
        
        elif self.game.game_state == 'results':
            # Draw results
            results_y = self.height - 300
            results_text = self.font_medium.render("Round Results:", True, (255, 255, 0))
            self.screen.blit(results_text, (50, results_y))
            
            dealer_result = f"Dealer: {self.game.dealer.hand.get_value()}" + (" (BUST)" if self.game.dealer.hand.is_bust() else "")
            dealer_text = self.font_small.render(dealer_result, True, (255, 255, 255))
            self.screen.blit(dealer_text, (50, results_y + 40))
            
            for i, player in enumerate(self.game.players):
                player_result = f"{player.name}: {player.hand.get_value()}" + (" (BUST)" if player.busted else "")
                player_text = self.font_small.render(player_result, True, (255, 255, 255))
                self.screen.blit(player_text, (50 + i * 300, results_y + 80))
            
            # Next round button
            next_button = Button(self.width // 2 - 50, self.height - 100, 100, 50, "Next Round", (50, 100, 50))
            next_button.draw(self.screen)
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if next_button.is_clicked(pos):
                    self.game.start_round()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = BlackjackUI()
    ui.run()
