import random


class Card:

  def __init__(self, suit, val):
    self.suit = suit
    self.val = val
    # Values A, 2-10, JQK

  def __str__(self):
    return self.suit + " " + self.val

  def __repr__(self):
    return self.suit + " " + self.val


class Deck:
  suits = ["♧", "♢", "♡", "♤"]

  def __init__(self):
    self.deck = []
    for suit in Deck.suits:
      self.deck.append(Card(suit, "A"))
      for i in range(2, 11):
        self.deck.append(Card(suit, str(i)))
      self.deck.append(Card(suit, "J"))
      self.deck.append(Card(suit, "Q"))
      self.deck.append(Card(suit, "K"))

  def shuffleDeck(self):
    random.shuffle(self.deck)

  def dispDeck(self):
    for card in self.deck:
      print(card.suit, card.val)
