

class SnakeApi():

    def __init__(self):
        pass

    def info(self):
        return {
            "apiversion": "1",
            "author": "bigbrains-snake",  # TODO: Your Battlesnake Username
            "color": "#19A7CE",  # TODO: Choose color
            "head": "evil",  # TODO: Choose head
            "tail": "hook",  # TODO: Choose tail
        }
    
    def start(self):
        return "start"

    def move(self):
        return "move"

    def end(self):
        return "end"