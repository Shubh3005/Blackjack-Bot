# Card Counting using Hi-Lo system
def get_card_value(card):
    # Assign values to cards based on the Hi-Lo system
    if card in ['2', '3', '4', '5', '6']:
        return 1
    elif card in ['10', 'J', 'Q', 'K', 'A']:
        return -1
    else:
        return 0

def count_cards(cards):
    # Initialize the running count
    running_count = 0
    for card in cards:
        running_count += get_card_value(card.upper())
    return running_count

# Blackjack strategy advice
def get_strategy(player_hand, dealer_upcard, can_split, can_double):
    # Example logic to implement the Blackjack strategy chart from the image
    # This can be more comprehensive depending on your needs

    # Convert dealer's upcard to a simplified version
    dealer = dealer_upcard if dealer_upcard != 'A' else 11
    if dealer == 'J' or dealer == 'Q' or dealer == 'K':
        dealer = 10

    # Split logic
    if can_split and player_hand[0] == player_hand[1]:
        pair_value = player_hand[0]
        return pair_strategy(pair_value, dealer)

    # Calculate the total for the hand
    hand_total = sum_hand(player_hand)
    
    # Hard totals (no ace counted as 11)
    if hand_total <= 8:
        return 'H'  # Always hit
    elif hand_total == 9:
        return 'D' if 3 <= dealer <= 6 else 'H'
    elif hand_total == 10:
        return 'D' if dealer <= 9 else 'H'
    elif hand_total == 11:
        return 'D'
    elif hand_total == 12:
        if 4 <= dealer <= 6:
            return 'S'
        else:
            return 'H'
    elif 13 <= hand_total <= 16:
        if 2 <= dealer <= 6:
            return 'S'
        else:
            return 'H'
    elif hand_total >= 17:
        return 'S'  # Always stand on 17 or higher

    # Soft totals (ace counted as 11)
    return soft_strategy(player_hand, dealer, can_double)

# Calculate total value of the hand
def sum_hand(hand):
    total = 0
    aces = 0
    for card in hand:
        if card in ['J', 'Q', 'K']:
            total += 10
        elif card == 'A':
            total += 11
            aces += 1
        else:
            total += int(card)
    
    # Adjust for aces being counted as 1 if total is over 21
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

# Soft hand strategy (has an ace)
def soft_strategy(player_hand, dealer, can_double):
    hand_total = sum_hand(player_hand)
    if hand_total == 18:
        if 2 <= dealer <= 6:
            return 'Ds' if can_double else 'S'
        elif 7 <= dealer <= 8:
            return 'S'
        else:
            return 'H'
    elif 19 <= hand_total <= 21:
        return 'S'
    else:
        return 'H'

# Pair splitting strategy
def pair_strategy(pair_value, dealer):
    if pair_value in ['A', '8']:
        return 'Y'  # Always split Aces and 8s
    elif pair_value == 'T':
        return 'N'  # Never split 10s
    elif pair_value == '9':
        if 2 <= dealer <= 6 or 8 <= dealer <= 9:
            return 'Y'
        else:
            return 'S'
    elif pair_value == '7':
        if 2 <= dealer <= 7:
            return 'Y'
        else:
            return 'H'
    elif pair_value == '6':
        if 2 <= dealer <= 6:
            return 'Y'
        else:
            return 'H'
    # Add more rules for other pairs as needed
    return 'N'

# Main function to integrate everything
def blackjack_bot():
    # Input card sequence for counting
    cards = input("Enter the cards dealt (separated by space): ").split()

    # Calculate card count
    running_count = count_cards(cards)
    print(f"Running Count: {running_count}")

    # Input player hand and dealer upcard
    player_hand = input("Enter your hand cards (separated by space): ").split()
    dealer_upcard = input("Enter dealer's upcard: ")

    # Check if player can split or double
    can_split = input("Can you split your hand? (yes/no): ").lower() == 'yes'
    can_double = input("Can you double down? (yes/no): ").lower() == 'yes'

    # Get strategy advice
    advice = get_strategy(player_hand, dealer_upcard, can_split, can_double)
    
    # Output strategy advice
    print(f"Strategy advice: {advice}")

# Run the bot
blackjack_bot()
