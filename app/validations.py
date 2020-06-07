from app import app, db
from app.models import User

def validate(em, cn, fromref):
    emx = User.query.filter_by(email=em).first()
    cnx = User.query.filter_by(contactnum=cn).first()
    usx = User.query.filter_by(torefID=fromref).first()

    isFromRefEmpty = 1 if (fromref == '') else 0

    if isFromRefEmpty == 0:
        if (emx is not None) and (cnx is None) and (usx is not None):
            print('Email exists')
            return 1
        elif (emx is None) and (cnx is not None) and (usx is not None):
            print('Phone exists')
            return 2
        elif (emx is not None) and (cnx is not None) and (usx is not None):
            print('Email and Phone exists')
            return 3
        elif usx is None:
            print('Enter valid Referal Code')
            return 4
        else:
            print('Validated 0, Referal code given by user: ', usx.firstname)
            return 0
    else:
        if (emx is not None) and (cnx is None):
            print('Email exists')
            return 1
        elif (emx is None) and (cnx is not None):
            print('Phone exists')
            return 2
        elif (emx is not None) and (cnx is not None):
            print('Email and Phone exists')
            return 3
        else:
            print('Validated 0')
            return 0

        