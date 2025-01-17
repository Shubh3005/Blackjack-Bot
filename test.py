import random
from collections import Counter

# Define card values and suits
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Create a deck of cards
def create_deck():
    return [(value, suit) for suit in SUITS for value in VALUES]

# Shuffle and deal cards
def deal(deck, num_cards):
    return [deck.pop() for _ in range(num_cards)]

# Evaluate the poker hand
def evaluate_hand(hand):
    values = [card[0] for card in hand]
    suits = [card[1] for card in hand]

    # Convert face cards to numbers for easier comparison
    value_ranks = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    value_counts = Counter([value_ranks[value] for value in values])
    
    is_flush = len(set(suits)) == 1
    is_straight = len(value_counts) == 5 and max(value_counts) - min(value_counts) == 4
    
    if is_flush and is_straight:
        return ('Straight Flush', max(value_counts))  # Highest card in the straight flush
    if 4 in value_counts.values():
        return ('Four of a Kind', value_counts.most_common(1)[0][0])
    if 3 in value_counts.values() and 2 in value_counts.values():
        return ('Full House', value_counts.most_common(1)[0][0])
    if is_flush:
        return ('Flush', max(value_counts))
    if is_straight:
        return ('Straight', max(value_counts))
    if 3 in value_counts.values():
        return ('Three of a Kind', value_counts.most_common(1)[0][0])
    if list(value_counts.values()).count(2) == 2:
        return ('Two Pair', value_counts.most_common(1)[0][0])
    if 2 in value_counts.values():
        return ('One Pair', value_counts.most_common(1)[0][0])
    
    return ('High Card', max(value_counts))

class PokerBot:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.chips = 1000  # Start with 1000 chips
        self.current_bet = 0

    def receive_hand(self, hand):
        self.hand = hand
    
    def evaluate(self):
        hand_rank, high_card = evaluate_hand(self.hand)
        return hand_rank, high_card
    
    def make_decision(self, current_bet):
        hand_rank, high_card = self.evaluate()
        
        # Simple strategy
        if hand_rank in ['Straight Flush', 'Four of a Kind', 'Full House', 'Flush']:
            return 'raise', min(self.chips, current_bet + 50)
        elif hand_rank in ['Straight', 'Three of a Kind']:
            return 'call', current_bet
        elif hand_rank == 'Two Pair' and high_card >= 10:
            return 'call', current_bet
        else:
            return 'fold', 0
    
    def bet(self, amount):
        self.chips -= amount
        self.current_bet += amount

# Simulate a round with the bot
def simulate_round():
    deck = create_deck()
    random.shuffle(deck)

    bot = PokerBot("Bot 1")
    player = PokerBot("Player")

    # Deal hands
    bot.receive_hand(deal(deck, 5))
    player.receive_hand(deal(deck, 5))

    # Simple betting simulation
    current_bet = 10
    player_bet = 10
    bot_bet = bot.make_decision(current_bet)
    
    print(f"Player's hand: {player.hand}, Bet: {player_bet}")
    print(f"Bot's hand: {bot.hand}, Decision: {bot_bet[0]}, Bet: {bot_bet[1]}")

# Run the round simulation
simulate_round()
