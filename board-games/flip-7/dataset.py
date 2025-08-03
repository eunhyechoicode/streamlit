inputs = [
    {"input_question": "How many total cards are in Flip 7?"},
    {"input_question": "How many action cards are there in Flip 7, and what types?"},
    {"input_question": "How many modifier cards are in Flip 7?"},
    {"input_question": "What does it mean to bust in Flip 7?"},
    {"input_question": "What happens when you achieve a Flip 7?"},
    {"input_question": "What does the Freeze card do in Flip 7?"},
    {"input_question": "What is the win condition in Flip 7?"},
    {"input_question": "When and how is the Second Chance card used in Flip 7?"},
    {"input_question": "How does the Flip 3 card work in Flip 7?"},
    {"input_question": "Do modifier cards count toward Flip 7?"}
]

outputs = [
    {"output_answer": "According to the game rules, Flip 7 contains a total of 94 cards, including number cards, action cards, and modifier cards."},
    {"output_answer": "According to the game rules, there are 9 action cards in Flip 7: 3 Flip 3 cards, 3 Freeze cards, and 3 Second Chance cards."},
    {"output_answer": "According to the game rules, Flip 7 includes 12 modifier cards: two each of +2, +4, +6, +8, +10, and x2."},
    {"output_answer": "According to the game rules, a bust happens when a player flips a number card that matches one they already have, causing them to be out of the round and score nothing."},
    {"output_answer": "According to the game rules, achieving a Flip 7 ends the round immediately and awards the player 15 bonus points."},
    {"output_answer": "According to the game rules, the Freeze card immediately ends the receiving player’s turn and locks in their current points for scoring."},
    {"output_answer": "According to the game rules, the game ends after a round in which at least one player reaches 200 points. The player with the highest score at that point wins."},
    {"output_answer": "According to the game rules, the Second Chance card can be used to avoid busting by discarding both the duplicate number and the Second Chance card. Only one may be held at a time."},
    {"output_answer": "According to the game rules, a Flip 3 card forces the player to flip three cards one by one. The process stops early if the player busts or achieves a Flip 7. Action cards drawn are handled afterward."},
    {"output_answer": "According to the game rules, modifier cards like +2 or x2 do not count toward the seven unique number cards needed for a Flip 7."}
]

metadata = [
    {"contexts": "Flip 7 includes 94 total cards consisting of number cards (0–12), action cards (Flip 3, Freeze, Second Chance), and modifier cards (+2 to +10, x2)."},
    {"contexts": "Action cards in Flip 7 include 3 Flip 3 cards, 3 Freeze cards, and 3 Second Chance cards, totaling 9 action cards."},
    {"contexts": "Modifier cards include two of each: +2, +4, +6, +8, +10, and x2, for a total of 12 modifier cards."},
    {"contexts": "A player busts when they flip a number card that matches a number already in their line, making them immediately out of the round with zero points."},
    {"contexts": "When a player flips 7 unique number cards, the round ends instantly and that player earns an additional 15 points."},
    {"contexts": "The Freeze card forces a player out of the round immediately, but they keep all their face-up cards and score them at the end of the round."},
    {"contexts": "The game ends once any player reaches 200 or more points. The player with the highest total score at the end of that round is the winner."},
    {"contexts": "A Second Chance card cancels a bust by discarding both the duplicate number card and the Second Chance card. Only one can be held at a time, and unused ones are discarded at round’s end."},
    {"contexts": "A Flip 3 card causes the player to flip three cards sequentially. It ends early if the player busts or gets a Flip 7. Additional action cards drawn during this are resolved afterward."},
    {"contexts": "Modifier cards increase scoring but do not count as number cards and therefore do not contribute toward completing a Flip 7."}
]
