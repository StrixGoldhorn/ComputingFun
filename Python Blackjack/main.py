from blackjack import Blackjack

# set desired number of decks
noOfDecks = 1

b = Blackjack(noOfDecks)
b.shuffleDeck()

# too addictive till you can't leave it so a whileTrue loop is applicable
while True:
  print("-" * 22 + "New Game" + "-" * 22)
  b.deal()
  print()
  print()
