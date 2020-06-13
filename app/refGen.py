import random
import string

def refGen(stringLength):
    from app.models import User
    choices = string.ascii_letters + string.digits
    a = ''.join(random.choice(choices) for i in range(stringLength))
    x = User.query.filter_by(torefID=a)
    if x is None:
        return a
    else:
        a = ''.join(random.choice(choices) for i in range(stringLength))
        return a
    
