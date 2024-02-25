from app import app
from flask import render_template, request, jsonify, session
from .models import User
from flask_login import current_user
from werkzeug.security import check_password_hash


@app.route('/')
def land():
    user_list = User.query.all()
    follow_set = set()

    if current_user.is_authenticated:
        users_following = current_user.following.all()
        for u in users_following:
            follow_set.add(u.id)
        for x in user_list:
            if x.id in follow_set:
                x.flag = True
    
    print(user_list, '\n', follow_set)
        
        

    # return render_template('index.html', u_list=user_list)


# @app.route("/@me")
# def get_current_user():
#     user_id = session.get("user_id")

#     if not user_id:
#         return jsonify({"error" : "Security Clearance Needed"}), 401

#     user = User.query.filter_by(id=user_id).first()
#     return jsonify({
#     "id" : user.id,
#     "email" : user.email
# })

# @app.route('/login', methods=["POST"])
# def qwertylogin_user():
#     data = request.get_json()
    # print(data)
    # u = data['username']
    # user = User.query.filter_by(username=u).first()
    # if user:
    #     if check_password_hash(user.password, data['pass']):
    #         return {
    #             'status':'ok',
    #             'message' : 'authenticated',
    #             'data': user.to_dict()
    #         }
    #     else:
    #         return {
    #             'status' : 'NOT ok',
    #             'message': 'Wrong Password',
    #             }, 400
#     return {
#         'status': 'NOT ok',
#         'message': "username not found",
#         'error': 'no username match'
#     }

# @app.route('/signup', methods=["POST"])
# def qwertysignup():
#     data=request.get_json()
#     print(data)
#     u = data['username']
#     email = data['email']
#     password = data['pass']
#     # password = request.json['password']
#     user = User(u, email, password)
#     user.save_me()
#     status = "OK"

    # user_exst = User.query.filter_by(username=u).first()
    # if user_exst:
    #     data = "already used"
    # user = User.query.filter_by(username=u).first()



#     return {
#     "status" : status,
#     "Message" : " sign up complete"
# }


# @app.route('/logout', methods=["POST"])
# def logout_user():
#     session.pop("user_id")
#     return '200'