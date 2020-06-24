from flask import jsonify, request
from app import app, db #import the variable 'app' from module 'app'
from app.models import User
from app.validations import validate
from app.login import logincheck
from flask_login import current_user, login_user, logout_user
from datetime import datetime

@app.route('/api/postsignup', methods=['GET','POST'])
def postSignUp():
    UD = request.json["userData"]
    u = User(firstname = UD["firstname"], lastname = UD["lastname"], email = UD["email"],
    contactnum = UD["contactnum"], fromrefID = UD["fromrefID"], hasPaid = 0,
    numberOfReferals = 0, isAdmin = 0)
    a = validate(u.email, u.contactnum, u.fromrefID)
    print(u)
    if a == 0:
        print("User ref Id sent")
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
        return jsonify({'error': a})

@app.route('/api/postpay', methods=['GET','POST'])
def postpay():
    UD = request.json["userData"]
    user = User.query.filter_by(email=UD["email"]).first()
    user.paynum = UD["paynum"]
    user.bname = UD["bname"]
    user.ifsc = UD["ifsc"]
    db.session.commit()
    return jsonify({'paychoice':'done'})

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
    currentUserEmail = request.json["CUE"]['currentUserEmail']
    user = User.query.filter_by(email=currentUserEmail).first()
    print("Accountdeets sent!")
    return jsonify({
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "contactnum": user.contactnum,
        "torefID": user.torefID,
        "hasPaid": user.hasPaid,
        "numberOfReferals": user.numberOfReferals,
        "isAdmin": user.isAdmin,
        "paynum": user.paynum,
    })

@app.route('/api/paysuccess', methods=['GET','POST'])
def paysuccess():
    currentUserEmail = request.json["CUE"]['currentUserEmail']
    user = User.query.filter_by(email=currentUserEmail).first()
    if user is not None:
        is user.hasPaid is not 1:
            print("Pay success for :", user.firstname)
            user.hasPaid = 1
            user.datePaid = datetime.utcnow()
            usxx = User.query.filter_by(torefID=user.fromrefID).first()
            if usxx is not None:
                usxx.numberOfReferals += 1
            db.session.commit()
            return jsonify({
                "payment" : "success"
            })
        else:
            print("User tried paymentsuccess, but user already paid")
            return jsonify({
                "payment" : "notloggedin"
            })
    else:
        print("Tried to access payment without logging in")
        return jsonify({
            "payment" : "notloggedin"
        })

@app.route('/api/checkpaid', methods=['GET','POST'])
def checkpaid():
    currentUserEmail = request.json["CUE"]['currentUserEmail']
    user = User.query.filter_by(email=currentUserEmail).first()
    if user is None:
        print("No user")
        return jsonify({
            "checkpaid" : "nouser"
        })
    elif user.hasPaid == 1:
        print("Payment verified")
        return jsonify({
            "checkpaid" : "paid"
        })
    else:
        print("Not paid")
        return jsonify({
            "checkpaid" : "unpaid"
        })

@app.route('/api/admin')
def admin():
    print("Admin requested...")
    print()
    users = User.query.all()
    usersResponse = []
    print("Users Retrived...")
    print()
    for user in users:
        d = user.__dict__
        print("Added referees key...")
        if '_sa_instance_state' in d:
            print("Found sa instance of", user)
            del d['_sa_instance_state']
            print("Deleted sa instance of ", user)
            print()
        usersResponse.append(d)
        print("User: ", user.firstname, " appended")
        print()
        print()
    print("End Admin Request...")    
    return jsonify(usersResponse)

@app.route('/api/load')
def load():
    return jsonify({"load": "success"})