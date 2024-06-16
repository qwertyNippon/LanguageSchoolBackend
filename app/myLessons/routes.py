from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send
import random
from string import ascii_uppercase
from app import socketio, db
from app.models import User
from .forms import CreatePostForm, UpdatePostForm

myLessons = Blueprint('myLessons', __name__, template_folder='myLessons_templates')

rooms = {}

def generate_unique_code(length):
    while True:
        code = ''.join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            break
    return code

@myLessons.route("/MyLessons", methods=["POST", "GET"])
@login_required
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code
        if create:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for(".room"))

    return render_template("home.html")

@myLessons.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for(".home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def handle_message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def handle_connect():
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def handle_disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

@myLessons.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    from app.models import MyLessons  # Late import to avoid circular import issues
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            img_url = form.img_url.data

            new_lesson = MyLessons(title=title, body=body, img_url=img_url, user_id=current_user.id)
            new_lesson.save_post()
            flash('Lesson created successfully', 'success')
            return redirect(url_for('.home'))
    return render_template('create_post.html', form=form)
