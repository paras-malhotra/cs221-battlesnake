import torch
print(torch.__version__)

import torch.nn as nn
import torch.optim as optim

import numpy as np
from numpy import linalg as LA
import uuid


class SnakeInference():

    def __init__(self):
        self.model = CIFAR10Model(channel_count=15,
                                  label_count=1)
        self.model.load_state_dict(torch.load('/content/drive/MyDrive/snake-model-1.pth'))
        self.model.eval()
        

    def value(self, example):
        shaped = ShapedExample(example)
        board = shaped.board_curr.get_board()
        input = torch.Tensor(np.array([board])).type(torch.FloatTensor)
        inferred = self.model(input)
        return inferred.detach().numpy()[0][0]


class ShapedExample():
  
  def __init__(self, example):
    self.example = example
    self.board_curr = GameBoard(example, example['gameState'])
    try:
        self.board_next = GameBoard(example, example['nextState']) 
        self.board_alts = []
        for action in ['left', 'right', 'up', 'down']:
          alt = self.example.copy()
          alt['action'] = action
          board = GameBoard(alt, example['nextState'])
          self.board_alts.append(board)
     except:
        print("NEXT_STATE_IS_UNKNOWN")
        pass


class GameBoard():

  def __init__(self, example, state):
    ### general
    self.id = uuid.uuid4()
    # channel
    self.channel_names = ['self_head', 'self_body', 'self_health', 'self_length',
                          'adversary_head', 'adversary_body', 'adversary_health', 'adversary_length',
                          'food', 'hazards', 
                          'left', 'right', 'down', 'up', 
                          "None"]
    # size
    cnn_size = 32
    if state['height'] > cnn_size or state['height'] > cnn_size:
      raise NotImplementedError("CNN only supports 32x32 grid")
    self.rows = cnn_size 
    self.cols = cnn_size                           
    ### specific
    self.example = example
    self.state = state
    self.set_board()
    self.set_food()
    self.set_hazard()
    self.set_player()
    self.set_action()

  def get_id(self):
    return self.id

  def channel_list(self):
    return self.channel_names

  def channel_count(self):
    return len(self.channel_names)

  def channel_idx(self, name):
    if name is None:
      name = "None"
    return self.channel_names.index(name)

  def set_board(self):
    board = []
    for i in range(self.channel_count()):
      board.append(self.new_channel())
    self.board = board

  def get_board(self):
    return self.board

  def get_reward(self):
    try:
      return self.example['reward']
    except:
      pass
    return 0

  def new_channel(self):
    channel = np.zeros((self.rows, self.cols))
    return channel

  def get_channel(self, name):
    return self.board[self.channel_idx(name)]

  def set_channel(self, name, channel):
    self.board[self.channel_idx(name)] = channel

  def mark_channel(self, name, locations, value=1):
    channel = self.get_channel(name)
    if isinstance(locations, list):
      for loc in locations:
        x, y = loc
        curr = channel[x][y]
        channel[x][y] = max([value, curr])
    else:
      for y, x in np.ndindex(channel.shape):
        curr = channel[x][y]
        channel[x][y] = max([value, curr])
    self.set_channel(name, channel)
    
  def set_food(self, name='food'):
    self.mark_channel(name, self.state[name])

  def set_hazard(self, name='hazards'):
    self.mark_channel(name, self.state[name])

  def set_action(self, name='action'):
    actual = self.example[name]
    self.mark_channel(actual, actual)

  def set_player(self):
    # {'health': 100,
    # 'body': [[6, 8]],
    # 'head': [6, 8],
    # 'length': 1,
    # 'id': 1,
    # 'alive': True,
    # 'ours': True}
    for player in self.state['players']:
      health = player['health']
      body = player['body']
      head = [player['head']]
      length = player['length']
      if player['alive']:
        if player['ours']:
          self.mark_channel('self_health', health, health)
          self.mark_channel('self_body', body)
          self.mark_channel('self_head', head)
          self.mark_channel('self_length', length)
        else:
          self.mark_channel('adversary_health', health, health)
          self.mark_channel('adversary_body', body)
          self.mark_channel('adversary_head', head)
          self.mark_channel('adversary_length', length)


class CIFAR10Model(nn.Module):
    def __init__(self, 
                 channel_count, # adversary, self, hazard, food, etc
                 label_count = 10
                 ):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=channel_count,  
                               out_channels=32, # number of filters
                               kernel_size=(3,3), 
                               stride=1, 
                               padding=1)
        self.act1 = nn.ReLU()
        self.drop1 = nn.Dropout(0.3)
 
        self.conv2 = nn.Conv2d(in_channels=32, 
                               out_channels=32, 
                               kernel_size=(3,3), 
                               stride=1, 
                               padding=1)
        self.act2 = nn.ReLU()
        self.pool2 = nn.MaxPool2d(kernel_size=(2, 2))
 
        self.flat = nn.Flatten()
 
        self.fc3 = nn.Linear(8192, 512)
        self.act3 = nn.ReLU()
        self.drop3 = nn.Dropout(0.5)
 
        self.fc4 = nn.Linear(512, label_count)
 
    def forward(self, x):
        # input 3x32x32, output 32x32x32
        x = self.conv1(x)
        x = self.act1(x)
        x = self.drop1(x)
        # input 32x32x32, output 32x32x32
        x = self.act2(self.conv2(x))
        # input 32x32x32, output 32x16x16
        x = self.pool2(x)
        # input 32x16x16, output 8192
        x = self.flat(x)
        # input 8192, output 512
        x = self.act3(self.fc3(x))
        x = self.drop3(x)
        # input 512, output 10
        x = self.fc4(x)
        return x        
