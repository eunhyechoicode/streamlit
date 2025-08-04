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
    {"output_answer": "Hey there! 🎮 Flip 7 comes packed with 94 amazing cards - that includes number cards, action cards, and cool modifier cards! Let's get playing! ✨"},
    {"output_answer": "Great question! 🌟 You've got 9 exciting action cards to play with: 3 Flip 3 cards, 3 Freeze cards, and 3 Second Chance cards! Each one adds its own special twist! 🎲"},
    {"output_answer": "Let me help you with that! 🎉 You get 12 awesome modifier cards - two each of +2, +4, +6, +8, +10, and x2! Perfect for boosting those scores! ✨"},
    {"output_answer": "Oops! 🎲 A bust happens when you flip a matching number - that means you're out of the round with zero points. But don't worry, there's always next round! 💫"},
    {"output_answer": "Amazing achievement! 🎉 When you get a Flip 7, you instantly end the round AND score a sweet 15 bonus points! That's what we call a power move! ✨"},
    {"output_answer": "Hey friend! 🌟 The Freeze card ends someone's turn right away but lets them keep their current points - it's like hitting pause on their turn! 🎲"},
    {"output_answer": "Let me help you with that! 🏆 Race to 200 points or more - whoever has the highest score when someone hits that mark wins the game! Time to aim high! ✨"},
    {"output_answer": "Great question! 🎮 The Second Chance card is your get-out-of-bust card! Just discard it along with the duplicate number and keep playing! Remember, you can only hold one at a time! 🌟"},
    {"output_answer": "Hey there! ✨ With a Flip 3 card, you'll flip three cards one after another - so exciting! If you bust or hit Flip 7, everything stops. Action cards wait until after! 🎲"},
    {"output_answer": "Good thinking! 🎯 Modifier cards are awesome for points, but they don't count toward your Flip 7 goal - only those number cards count! Keep that in mind for your strategy! ✨"}
]

metadata = [
    {"contexts": "Flip 7 includes 94 total cards consisting of number cards (0–12), action cards (Flip 3, Freeze, Second Chance), and modifier cards (+2 to +10, x2)."},
    {"contexts": "Action cards in Flip 7 include 3 Flip 3 cards, 3 Freeze cards, and 3 Second Chance cards, totaling 9 action cards."},
    {"contexts": "Modifier cards include two of each: +2, +4, +6, +8, +10, and x2, for a total of 12 modifier cards."},
    {"contexts": "A player busts when they flip a number card that matches a number already in their line, making them immediately out of the round with zero points."},
    {"contexts": "When a player flips 7 unique number cards, the round ends instantly and that player earns an additional 15 points."},
    {"contexts": "The Freeze card forces a player out of the round immediately, but they keep all their face-up cards and score them at the end of the round."},
    {"contexts": "The game ends once any player reaches 200 or more points. The player with the highest total score at the end of that round is the winner."},
    {"contexts": "A Second Chance card cancels a bust by discarding both the duplicate number card and the Second Chance card. Only one can be held at a time, and unused ones are discarded at round's end."},
    {"contexts": "A Flip 3 card causes the player to flip three cards sequentially. It ends early if the player busts or gets a Flip 7. Additional action cards drawn during this are resolved afterward."},
    {"contexts": "Modifier cards increase scoring but do not count as number cards and therefore do not contribute toward completing a Flip 7."}
]