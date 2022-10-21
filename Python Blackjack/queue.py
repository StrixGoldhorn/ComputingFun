class Node:
  def __init__(self, data = None, ptr = None):
    self.data = data
    self.ptr = ptr

class LinkedList:
  def __init__(self):
    self.head = None

  def insert(self, data, pos):
    if self.isEmpty():
      self.head = Node(data)

    elif pos == 1:
      self.head = Node(data, self.head)
      
    else:
      cnt = 1
      curr = self.head
      while cnt != pos:
        cnt += 1
        prev = curr
        curr = curr.ptr

      prev.ptr = Node(data, curr)

  def remove(self, pos):
    if self.isEmpty():
      print("There is nothing to remove.")
      
    elif pos == 1:
      temp = self.head.data
      self.head = self.head.ptr
      return temp
      
    else:
      cnt = 1
      curr = self.head
      while cnt != pos:
        cnt += 1
        prev = curr
        curr = curr.ptr
        
      temp = curr.data
      prev.ptr = curr.ptr
      return temp
      
  def display(self):
    curr = self.head
    while curr != None:
      print(curr.data)
      curr = curr.ptr
  
  def isEmpty(self):
    return self.head == None

  def size(self):
    cnt = 0
    curr = self.head
    while curr != None:
      cnt += 1
      curr = curr.ptr
    return cnt



class Queue(LinkedList):
  def __init__(self):
    super().__init__()

  def push(self, data):
    super().insert(data, self.size()+1)

  def pop(self):
    return super().remove(1)

  def display(self):
    print("Front")
    super().display()
    print("Back")