# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

def player(prev_play, opponent_history=[], my_history=[], markov_chain=[{}]):
    # Initialize responses that beat each move
    beats = {'R': 'P', 'P': 'S', 'S': 'R'}
    
    # Reset game state
    if not prev_play:
        opponent_history.clear()
        my_history.clear()
        # Initialize Markov Chain with all possible states
        markov_chain[0] = {
            'R': {'R': 0, 'P': 0, 'S': 0},
            'P': {'R': 0, 'P': 0, 'S': 0},
            'S': {'R': 0, 'P': 0, 'S': 0},
            'RR': {'R': 0, 'P': 0, 'S': 0},
            'RP': {'R': 0, 'P': 0, 'S': 0},
            'RS': {'R': 0, 'P': 0, 'S': 0},
            'PR': {'R': 0, 'P': 0, 'S': 0},
            'PP': {'R': 0, 'P': 0, 'S': 0},
            'PS': {'R': 0, 'P': 0, 'S': 0},
            'SR': {'R': 0, 'P': 0, 'S': 0},
            'SP': {'R': 0, 'P': 0, 'S': 0},
            'SS': {'R': 0, 'P': 0, 'S': 0}
        }
        return 'R'

    # Update histories
    opponent_history.append(prev_play)

    # Add abbey-specific pattern detection before Markov chain logic
    if len(opponent_history) > 3:
        # Look for shorter patterns (3 moves) with higher frequency threshold
        sequence = ''.join(opponent_history[-3:])
        pattern_count = ''.join(opponent_history).count(sequence)
        
        if pattern_count >= 3:  # Increased frequency threshold
            potential_next = []
            for move in ['R', 'P', 'S']:
                count = ''.join(opponent_history).count(sequence + move)
                potential_next.append((move, count))
            
            most_likely = max(potential_next, key=lambda x: x[1])[0]
            return beats[most_likely]

    # Update Markov Chain probabilities
    if len(opponent_history) >= 2:
        # Single previous move
        prev_state = opponent_history[-2]
        markov_chain[0][prev_state][prev_play] += 1

        # Two previous moves
        prev_state_2 = ''.join(opponent_history[-3:-1])
        if prev_state_2 in markov_chain[0]:
            markov_chain[0][prev_state_2][prev_play] += 1

    # Make prediction based on Markov Chain
    def predict_next(state):
        if state in markov_chain[0]:
            predictions = markov_chain[0][state]
            if sum(predictions.values()) > 0:
                return max(predictions, key=predictions.get)
        return None

    # Try different prediction strategies
    prediction = None
    
    # Try two-move pattern prediction
    if len(opponent_history) >= 2:
        last_two = ''.join(opponent_history[-2:])
        prediction = predict_next(last_two)

    # If no two-move pattern, try single-move prediction
    if prediction is None and opponent_history:
        prediction = predict_next(opponent_history[-1])

    # If no pattern detected, use frequency analysis
    if prediction is None and len(opponent_history) >= 5:
        last_five = opponent_history[-5:]
        prediction = max(set(last_five), key=last_five.count)

    # Default to countering last move if no pattern found
    if prediction is None:
        prediction = prev_play if prev_play else 'R'

    # Return the move that beats the prediction
    return beats[prediction]
