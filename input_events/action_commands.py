import random

ARRAY_OF_ACTIONS = ['text', 'tap', 'swipe', 'keyevent', 'draganddrop']
def select_action():
    return ARRAY_OF_ACTIONS[random.randrange(len(ARRAY_OF_ACTIONS))]