import utils

class Room:
    name, strength, group = '', '', -1

    def __init__(self, name, strength, group):
        self.name = name
        self.strength = strength
        self.group = group


def getSeating(data: list[Room]) -> dict[str, dict[str, list[int]]]:
    '''
    INSTRUCTIONS:

    The variable data will be a list of objects of type Room (defined above)
    Process it accordingly and give the output as a dict where:
        1. The keys are the room names
        2. The values are a dict themselves of the format:
            i. The keys are the classes alloted
            ii. The values consist of a list of two elements where the first is 
                the starting roll and the second is the ending roll (both inclusive)

    You can use the utility functions like so: utils.getData(), utils.getDF({})...
    '''