#!/usr/bin/env python3
import random
import time
import os
import sys

# ANSI color codes for cyberpunk aesthetic
NEON_PINK = '\033[95m'
NEON_BLUE = '\033[94m'
NEON_CYAN = '\033[96m'
NEON_GREEN = '\033[92m'
NEON_YELLOW = '\033[93m'
NEON_RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'
BLINK = '\033[5m'

# Card suits with Unicode symbols
SUITS = {
    'Hearts': '♥',
    'Diamonds': '♦',
    'Clubs': '♣',
    'Spades': '♠'
}

SUIT_COLORS = {
    'Hearts': NEON_RED,
    'Diamonds': NEON_RED,
    'Clubs': NEON_CYAN,
    'Spades': NEON_CYAN
}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self._get_value()
        self.color = SUIT_COLORS[suit]
    
    def _get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def get_art(self, hidden=False):
        if hidden:
            return [
                f"{NEON_PINK}┌─────────┐{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░░░░░░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░░░░░░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░{NEON_YELLOW}CYBER{NEON_BLUE}░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░{NEON_CYAN}JACK{NEON_BLUE}░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░░░░░░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░░░░░░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}│{NEON_BLUE}░░░░░░░░░{NEON_PINK}│{RESET}",
                f"{NEON_PINK}└─────────┘{RESET}"
            ]
        
        # Format rank for display
        rank_display = self.rank
        if self.rank == '10':
            rank_left = '10'
            rank_right = '10'
        else:
            rank_left = rank_display + ' '
            rank_right = ' ' + rank_display
        
        symbol = SUITS[self.suit]
        
        # Special center designs for face cards
        if self.rank == 'K':
            center = f"{self.color}  ♔ K ♔  {RESET}"
        elif self.rank == 'Q':
            center = f"{self.color}  ♕ Q ♕  {RESET}"
        elif self.rank == 'J':
            center = f"{self.color}  ♗ J ♗  {RESET}"
        elif self.rank == 'A':
            center = f"{self.color}    {symbol}    {RESET}"
        else:
            # Number cards show multiple symbols
            if self.value <= 3:
                center = f"{self.color}    {symbol}    {RESET}"
            else:
                center = f"{self.color}   {symbol} {symbol}   {RESET}"
        
        return [
            f"{NEON_GREEN}┌─────────┐{RESET}",
            f"{NEON_GREEN}│{self.color}{rank_left}       {NEON_GREEN}│{RESET}",
            f"{NEON_GREEN}│{self.color} {symbol}       {NEON_GREEN}│{RESET}",
            f"{NEON_GREEN}│         │{RESET}",
            f"{NEON_GREEN}│{center}{NEON_GREEN}│{RESET}",
            f"{NEON_GREEN}│         │{RESET}",
            f"{NEON_GREEN}│{self.color}       {symbol} {NEON_GREEN}│{RESET}",
            f"{NEON_GREEN}│{self.color}       {rank_right}{NEON_GREEN}│{RESET}",
            f"{NEON_GREEN}└─────────┘{RESET}"
        ]
    
    def __str__(self):
        return f"{self.rank}{SUITS[self.suit]}"

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()
    
    def reset(self):
        self.cards = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for rank in ranks:
                self.cards.append(Card(rank, suit))
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self, bet=0):
        self.cards = []
        self.bet = bet
        self.stood = False
        self.doubled = False
    
    def add_card(self, card):
        self.cards.append(card)
    
    def get_value(self):
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
            value += card.value
        
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21
    
    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].value == self.cards[1].value
    
    def can_double(self):
        return len(self.cards) == 2 and not self.doubled
    
    def is_bust(self):
        return self.get_value() > 21
    
    def has_soft_17(self):
        """Check if hand is exactly soft 17 (A-6)"""
        if self.get_value() != 17:
            return False
        
        # Check if we have an ace counting as 11
        has_ace = any(card.rank == 'A' for card in self.cards)
        if not has_ace:
            return False
        
        # Calculate value counting all aces as 1
        hard_value = sum(1 if card.rank == 'A' else card.value for card in self.cards)
        
        # If hard value is 7 and we have 17 total, then we have soft 17
        return hard_value == 7
    
    def display_art(self, hide_first=False, label=""):
        if not self.cards:
            return
        
        # Print label if provided
        if label:
            print(f"{NEON_YELLOW}{label}{RESET}")
        
        # Get art for each card
        card_arts = []
        for i, card in enumerate(self.cards):
            if i == 0 and hide_first:
                card_arts.append(card.get_art(hidden=True))
            else:
                card_arts.append(card.get_art())
        
        # Print cards side by side
        for row in range(9):  # 9 rows per card
            line = ""
            for card_art in card_arts:
                line += card_art[row] + "  "
            print(line)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.balance = 500
        self.bet = 0
        self.last_bet = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        print(f"{NEON_PINK}{'═'*70}{RESET}")
        print(f"{BOLD}{NEON_CYAN}╔═══════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_PINK}         ▄████▄  ▓██   ██▓ ▄▄▄▄   ▓█████  ██▀███                  {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_BLUE}        ▒██▀ ▀█   ▒██  ██▒▓█████▄ ▓█   ▀ ▓██ ▒ ██▒                {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_BLUE}        ▒▓█    ▄   ▒██ ██░▒██▒ ▄██▒███   ▓██ ░▄█ ▒                {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_YELLOW}        ▒▓▓▄ ▄██▒  ░ ▐██▓░▒██░█▀  ▒▓█  ▄ ▒██▀▀█▄      {BLINK}$$$${RESET}        {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_YELLOW}        ▒ ▓███▀ ░  ░ ██▒▓░░▓█  ▀█▓░▒████▒░██▓ ▒██▒                {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}║{NEON_RED}        ░ ░▒ ▒  ░   ██▒▒▒ ░▒▓███▀▒░░ ▒░ ░░ ▒▓ ░▒▓░ JACK           {NEON_CYAN}║{RESET}")
        print(f"{BOLD}{NEON_CYAN}╚═══════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"{NEON_CYAN}     Dealer hits soft 17  •  Blackjack pays 3:2  •  Double after split     {RESET}")
        print(f"{NEON_PINK}{'═'*70}{RESET}")
        print(f"{NEON_GREEN}💰 Balance: ${self.balance}{RESET}", end="")
        if self.bet > 0:
            print(f"    {NEON_YELLOW}🎰 Current Bet: ${self.bet}{RESET}")
        else:
            print()
        print(f"{NEON_PINK}{'═'*70}{RESET}\n")
    
    def get_bet(self):
        while True:
            try:
                print(f"{NEON_CYAN}Enter bet amount (multiples of $5, min $5) or type 'exit' to quit:{RESET}")
                if self.last_bet > 0 and self.last_bet <= self.balance:
                    print(f"{NEON_YELLOW}Press ENTER to repeat last bet (${self.last_bet}) or type new amount:{RESET}")
                
                bet_input = input(f"{NEON_GREEN}${RESET}").strip().lower()
                
                # Check for exit
                if bet_input in ['exit', 'quit', 'x', 'q']:
                    return None
                
                # Handle repeat bet
                if bet_input == "" and self.last_bet > 0 and self.last_bet <= self.balance:
                    return self.last_bet
                
                bet = int(bet_input)
                
                if bet < 5:
                    print(f"{NEON_RED}⚠ Minimum bet is $5!{RESET}")
                elif bet % 5 != 0:
                    print(f"{NEON_RED}⚠ Bet must be in $5 increments!{RESET}")
                elif bet > self.balance:
                    print(f"{NEON_RED}⚠ Insufficient funds! Balance: ${self.balance}{RESET}")
                else:
                    self.last_bet = bet
                    return bet
            except ValueError:
                if bet_input not in ['exit', 'quit', 'x', 'q']:
                    print(f"{NEON_RED}⚠ Invalid input! Enter a number or 'exit' to quit.{RESET}")
    
    def play_hand(self, hand, dealer_hand, hand_num=None, total_hands=1):
        while not hand.stood and not hand.is_bust():
            self.clear_screen()
            self.display_header()
            
            # Show dealer's hand
            print(f"{NEON_BLUE}╔═══════════════ DEALER ═══════════════╗{RESET}")
            print(f"{NEON_BLUE}║ {DIM}The house always wins...{RESET}             {NEON_BLUE}║{RESET}")
            print(f"{NEON_BLUE}╚══════════════════════════════════════╝{RESET}")
            dealer_hand.display_art(hide_first=True)
            print()
            
            # Show player's hand(s)
            if total_hands > 1:
                hand_label = f"HAND {hand_num} - Bet: ${hand.bet}"
            else:
                hand_label = ""
            
            print(f"{NEON_YELLOW}╔═══════════════ PLAYER ═══════════════╗{RESET}")
            print(f"{NEON_YELLOW}║ Value: {hand.get_value():<2} {RESET}                           {NEON_YELLOW}║{RESET}")
            if hand_label:
                print(f"{NEON_YELLOW}║ {hand_label:<36} ║{RESET}")
            print(f"{NEON_YELLOW}╚══════════════════════════════════════╝{RESET}")
            hand.display_art(label=hand_label)
            print()
            
            # Check for blackjack on initial deal
            if len(hand.cards) == 2 and hand.is_blackjack():
                print(f"{NEON_GREEN}🎉 BLACKJACK!{RESET}")
                hand.stood = True
                break
            
            # Check for 21 (auto-stand)
            if hand.get_value() == 21:
                print(f"{NEON_GREEN}✨ 21! Auto-standing.{RESET}")
                hand.stood = True
                time.sleep(1)
                break
            
            # Check for bust
            if hand.is_bust():
                print(f"{NEON_RED}💥 BUST!{RESET}")
                break
            
            # Build options string
            options = ["[H]it", "[S]tand"]
            if hand.can_double() and hand.bet <= self.balance:
                options.append("[D]ouble")
            if hand.can_split() and hand.bet <= self.balance:
                options.append("S[P]lit")
            
            print(f"{NEON_CYAN}{' or '.join(options)}?{RESET}")
            action = input().lower()
            
            if action == 'h':
                hand.add_card(self.deck.draw())
            elif action == 's':
                hand.stood = True
            elif action == 'd' and hand.can_double() and hand.bet <= self.balance:
                # Double down
                self.balance -= hand.bet
                hand.bet *= 2
                hand.doubled = True
                hand.add_card(self.deck.draw())
                hand.stood = True
                if not hand.is_bust():
                    print(f"{NEON_YELLOW}Doubled down! Total bet: ${hand.bet}{RESET}")
                    time.sleep(1)
            elif action == 'p' and hand.can_split() and hand.bet <= self.balance:
                # Return True to indicate split
                return True
        
        return False  # No split
    
    def play_round(self):
        self.clear_screen()
        self.display_header()
        
        # Get bet
        self.bet = self.get_bet()
        if self.bet is None:  # User chose to exit
            return False
        self.balance -= self.bet
        
        # Deal initial cards
        player_hands = [Hand(self.bet)]
        dealer_hand = Hand()
        
        player_hands[0].add_card(self.deck.draw())
        dealer_hand.add_card(self.deck.draw())
        player_hands[0].add_card(self.deck.draw())
        dealer_hand.add_card(self.deck.draw())
        
        # Check for dealer blackjack first
        if dealer_hand.is_blackjack():
            self.show_final_results(player_hands, dealer_hand)
            return
        
        # Play each hand
        hand_index = 0
        while hand_index < len(player_hands):
            hand = player_hands[hand_index]
            
            # Play this hand
            should_split = self.play_hand(hand, dealer_hand, hand_index + 1, len(player_hands))
            
            if should_split:
                # Create new hand from split
                self.balance -= hand.bet
                new_hand = Hand(hand.bet)
                new_hand.add_card(hand.cards.pop())
                player_hands.append(new_hand)
                
                # Add new cards to both hands
                hand.add_card(self.deck.draw())
                new_hand.add_card(self.deck.draw())
                
                print(f"{NEON_YELLOW}Split! Playing {len(player_hands)} hands.{RESET}")
                time.sleep(1)
                continue  # Replay current hand
            
            hand_index += 1
        
        # Dealer's turn (only if at least one hand is still active)
        active_hands = [h for h in player_hands if not h.is_bust()]
        if active_hands:
            while dealer_hand.get_value() < 17 or dealer_hand.has_soft_17():
                dealer_hand.add_card(self.deck.draw())
        
        # Show results
        self.show_final_results(player_hands, dealer_hand)
    
    def show_final_results(self, player_hands, dealer_hand):
        self.clear_screen()
        self.display_header()
        
        # Show dealer's final hand
        print(f"{NEON_BLUE}╔═══════════════ DEALER ═══════════════╗{RESET}")
        print(f"{NEON_BLUE}║ Value: {dealer_hand.get_value():<2} {RESET}                           {NEON_BLUE}║{RESET}")
        print(f"{NEON_BLUE}╚══════════════════════════════════════╝{RESET}")
        dealer_hand.display_art()
        print()
        
        dealer_value = dealer_hand.get_value()
        dealer_blackjack = dealer_hand.is_blackjack()
        total_winnings = 0
        
        # Show each player hand and calculate winnings
        for i, hand in enumerate(player_hands):
            if len(player_hands) > 1:
                print(f"\n{NEON_YELLOW}═══════ HAND {i+1} ═══════{RESET}")
            
            print(f"{NEON_YELLOW}╔═══════════════ PLAYER ═══════════════╗{RESET}")
            print(f"{NEON_YELLOW}║ Value: {hand.get_value():<2} | Bet: ${hand.bet:<4}          {NEON_YELLOW}║{RESET}")
            print(f"{NEON_YELLOW}╚══════════════════════════════════════╝{RESET}")
            hand.display_art()
            
            player_value = hand.get_value()
            player_blackjack = hand.is_blackjack()
            
            # Determine outcome
            if player_value > 21:
                print(f"{NEON_RED}💥 BUST! Lost ${hand.bet}{RESET}")
            elif dealer_blackjack and player_blackjack:
                print(f"{NEON_YELLOW}🤝 Push! Both have Blackjack.{RESET}")
                total_winnings += hand.bet
            elif player_blackjack and not dealer_blackjack:
                winnings = int(hand.bet * 2.5)  # Original bet + 1.5x
                print(f"{NEON_GREEN}🎉 BLACKJACK! Won ${winnings - hand.bet} (paid 3:2){RESET}")
                total_winnings += winnings
            elif dealer_value > 21:
                print(f"{NEON_GREEN}💰 Dealer BUST! Won ${hand.bet}{RESET}")
                total_winnings += hand.bet * 2
            elif player_value > dealer_value:
                print(f"{NEON_GREEN}🎊 WIN! Won ${hand.bet}{RESET}")
                total_winnings += hand.bet * 2
            elif player_value < dealer_value:
                print(f"{NEON_RED}😢 LOSE! Lost ${hand.bet}{RESET}")
            else:
                print(f"{NEON_YELLOW}🤝 PUSH! It's a tie.{RESET}")
                total_winnings += hand.bet
        
        self.balance += total_winnings
        print(f"\n{NEON_CYAN}{'═'*40}{RESET}")
        print(f"{NEON_GREEN}New Balance: ${self.balance}{RESET}")
    
    def run(self):
        self.clear_screen()
        print(f"{BOLD}{NEON_PINK}Welcome to CYBERJACK!{RESET}")
        print(f"{NEON_CYAN}Where neon lights meet lady luck...{RESET}\n")
        print(f"{DIM}Entering the underground casino...{RESET}")
        time.sleep(2)
        
        while self.balance >= 5:
            result = self.play_round()
            if result is False:  # User chose to exit during betting
                break
            
            if self.balance < 5:
                print(f"\n{NEON_RED}💸 Game Over! Insufficient funds.{RESET}")
                print(f"{DIM}Your credits have been depleted...{RESET}")
                break
            
            print(f"\n{NEON_CYAN}Play again? [Y/N] (Press ENTER for Yes){RESET}")
            response = input().lower()
            if response == 'n':
                break
        
        print(f"\n{NEON_PINK}Thanks for playing CYBERJACK!{RESET}")
        print(f"{NEON_GREEN}💰 Final Balance: ${self.balance}{RESET}")
        print(f"{DIM}Disconnecting from the neon underground...{RESET}")

if __name__ == "__main__":
    game = BlackjackGame()
    game.run()
