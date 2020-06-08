from flask import jsonify, request
from app import app, db #import the variable 'app' from module 'app'
from app.models import User
from app.validations import validate
from app.login import logincheck
from flask_login import current_user, login_user, logout_user

@app.route('/api/postsignup', methods=['GET','POST'])
def postSignUp():
    UD = request.json["userData"]
    u = User(firstname = UD["firstname"], lastname = UD["lastname"], email = UD["email"], contactnum = UD["contactnum"], fromrefID = UD["fromrefID"])
    a = validate(u.email, u.contactnum, u.fromrefID)
    print(u)
    if a == 0:
        u.set_password(UD["password"])
        u.genRefID()
        db.session.add(u)
        db.session.commit()
        return jsonify({'refID':u.torefID})
    else:
        if a == 1:
            err = "Email already exists"
        if a == 2:
            err = "Phone number already exists"
        if a == 3:
            err = "Email and Phone number already exist" 
        if a == 4:
            err = "Enter valid Referal Code"
        print(jsonify({'error': err}))       
        return jsonify({'error': err})

@app.route('/api/postlogin', methods=['GET','POST'])
def postLogin():
    UD = request.json["userData"]
    usrMail = UD['email']
    usrPwd = UD['password']
    a = logincheck(usrMail,usrPwd)
    logout_user()
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return jsonify({"auth": 10})
    else:
        if a == 1:
            return jsonify({"auth": 1})
        elif a == 2:
            return jsonify({"auth": 2})
        else:
            user = User.query.filter_by(email=usrMail).first()
            login_user(user)
            return {"auth":0}
    
@app.route('/api/logout')
def logout():
    logout_user()
    print("logged out")
    return {"auth": -1}

@app.route('/api/accountdeets', methods=['GET','POST'])
def accountdeets():
    if not current_user.is_authenticated:
        print("User not authenticated yet")
        return jsonify({"auth": -1})
    else:
        currentUserEmail = request.json["CUE"]['currentUserEmail']
        user = User.query.filter_by(email=currentUserEmail).first()
        print("Accountdeets sent!")
        return jsonify({
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "contactnum": user.contactnum,
            "torefID": user.torefID,
        })

