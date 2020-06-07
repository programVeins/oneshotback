import random
import string

def refGen(stringLength):
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for i in range(stringLength))