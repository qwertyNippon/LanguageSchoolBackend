from app import app

from flask import render_template
from .models import User
from flask_login import current_user

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
        
        

    return render_template('index.html', u_list=user_list)

