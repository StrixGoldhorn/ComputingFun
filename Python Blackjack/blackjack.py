from deck import Deck, Card
from queue import Queue
import random


class Hand:
  val10 = ["10", "J", "Q", "K"]

  def __init__(self):
    self.cards = []

  def checkBlackjack(self):
    if len(self.cards) == 2 and (
      (self.cards[0].val == "A" and self.cards[1].val in Hand.val10) or
      (self.cards[1].val == "A" and self.cards[0].val in Hand.val10)):
      print("Blackjack!")
      return True
    return False

  def calculate(self):
    total = [0]
    for card in self.cards:
      for cnt in range(len(total)):
        if card.val == "A":
          total.append(total[cnt] + 1)
          total[cnt] += 11
        elif card.val in Hand.val10:
          total[cnt] += 10
        else:
          total[cnt] += int(card.val)
    filtered = list(set(filter(lambda a: a <= 21, total)))
    filtered.sort()
    return filtered

  def bust(self):
    if len(self.calculate()) == 0:
      return True
    else:
      return False


class Blackjack:

  def __init__(self, noOfDecks):
    self.playingDeck = Queue()
    self.discardDeck = Queue()
    for i in range(noOfDecks):
      temp = Deck()
      for card in temp.deck:
        self.playingDeck.push(card)

    self.dealer = Hand()
    self.player = Hand()

    self.count = 0

  def showDeck(self):
    self.playingDeck.display()

  def shuffleDeck(self):
    self.count = 0
    all = []
    for i in range(self.playingDeck.size()):
      all.append(self.playingDeck.pop())
    random.shuffle(all)
    for i in all:
      self.playingDeck.push(i)

  def deal(self):
    if self.playingDeck.size() >= 4:
      print(f"Cards left: {self.playingDeck.size()}")
      print(f"Current count: {self.count}")

      # deal cards
      self.dealer.cards.append(self.playingDeck.pop())
      self.player.cards.append(self.playingDeck.pop())
      self.dealer.cards.append(self.playingDeck.pop())
      self.player.cards.append(self.playingDeck.pop())

      # show dealer's first and both of player's
      print(f"Dealer: {self.dealer.cards[0]} | ? ?")
      print(f"Player: {self.player.cards[0]} | {self.player.cards[1]}")

      self.play()

    else:
      print("Out of cards! Adding and shuffling with discarded cards.")
      for i in range(self.discardDeck.size()):
        self.playingDeck.push(self.discardDeck.pop())
      self.shuffleDeck()

  def play(self):
    winner = None

    # player makes move
    if self.player.checkBlackjack():
      winner = self.player

    else:
      stand = False

      # if player did not blackjack and has not stand
      # does not account for 5 card rule
      while not stand:

        choice = "a"
        while choice not in ["h", "s"]:
          choice = input("Hit or Stand? (h/s): ").lower()
          print("-" * 50)

        if choice == "s":
          stand = True
        else:
          self.player.cards.append(self.playingDeck.pop())
          print(f"Dealer: {self.dealer.cards[0]} | ? ?")
          print("Player: ", end="")
          for p in self.player.cards:
            print(p, end=" | ")
          print()

      # after player stands, dealer makes move
      while self.dealer.bust() == False and self.dealer.calculate()[0] < 17:
        self.dealer.cards.append(self.playingDeck.pop())

    # show final
    print("Dealer: ", end="")
    for d in self.dealer.cards:
      print(d, end=" | ")
    print()

    print("Player: ", end="")
    for p in self.player.cards:
      print(p, end=" | ")
    print()

    # results
    if winner != None:
      print(f"Player wins due to Blackjack.")

    elif self.dealer.bust() and not self.player.bust():
      print(f"Dealer busts.\nPlayer wins with {self.player.calculate()[-1]}.")

    elif not self.dealer.bust() and self.player.bust():
      print(f"Player busts.\nDealer wins with {self.dealer.calculate()[-1]}.")

    elif self.dealer.bust() and self.player.bust():
      print(f"Both Dealer and Player busts.")

    elif self.dealer.calculate()[-1] < self.player.calculate()[-1]:
      print(
        f"Player wins with {self.player.calculate()[-1]} against Dealer's {self.dealer.calculate()[-1]}"
      )

    elif self.dealer.calculate()[-1] > self.player.calculate()[-1]:
      print(
        f"Dealer wins with {self.dealer.calculate()[-1]} against Player's {self.player.calculate()[-1]}"
      )

    else:
      print(
        f"Push! Both Dealer and Player attained {self.dealer.calculate()[-1]}")

    # return cards, edit count
    for card in self.dealer.cards:
      self.updateCount(card)
      self.discardDeck.push(card)
    self.dealer.cards = []

    for card in self.player.cards:
      self.updateCount(card)
      self.discardDeck.push(card)
    self.player.cards = []

  # based on Wong Halves card counting system
  def updateCount(self, card):
    if card.val in ["2", "7"]:
      self.count += 0.5

    elif card.val in ["3", "4", "6"]:
      self.count += 1

    elif card.val == "5":
      self.count += 1.5

    elif card.val == "9":
      self.count -= 0.5

    elif card.val in ["10", "J", "Q", "K", "A"]:
      self.count -= 1
