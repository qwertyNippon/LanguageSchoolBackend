from flask import Blueprint, request, json

from ..models import Post, Movie, Bikes


api = Blueprint('api', __name__, url_prefix='/api')

@api.get('/posts') 
def get_posts():
    posts = Post.query.all()
    post_list = [p.to_dict() for p in posts]
    return {
        'status' : 'ok',
        'posts' : post_list 
    }

@api.get('/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'post': post.to_dict(),
            'status': 'ok'
        }
    else:
        return {
            'status' : 'NOT ok',
            'message' : 'there is no post for that id'
        }
    
@api.post('/createpost')
def create_post_api():
    data = request.json  #this is coming from the POST request body
    title = data['title']
    body = data['body']
    img_url = data['img_url']
    user_id = data['user_id']

    new = Post(title, body, img_url, user_id)
    new.save_post()
    return {
        'status': 'ok',
        'message' : 'New post has been created!'
    }

@api.get('/movies')
def get_movies():
    movies = Movie.query.all()
    movie_list = [m.to_dict() for m in movies]
    return {
        'status' : 'ok',
        'movies' : movie_list
    }

@api.get('/movie/id/<int:mov_id>')
def get_mov_by_id(mov_id):
    mov = Movie.query.get(mov_id)
    if mov:
        return {
            'movie': mov.to_dict(),
            'status': 'ok'
        }
    else:
        return {
            'status' : 'NOT ok',
            'message' : 'there is no movie for that id'
        }
    
@api.get('/movie/title/<mov_title>')
def get_mov_by_title(mov_title):
    mov = Movie.query.filter_by(title=mov_title).first()
    if mov:
        return {
            'movie': mov.to_dict(),
            'status': 'ok'
        }
    else:
        return {
            'status' : 'NOT ok',
            'message' : 'there is no movie for that id'
        }

@api.get('/bikes')
def get_bikes():
    bikes = Bikes.query.all()
    bike_list = [b.to_dict() for b in bikes]
    return {
        'status' : 'ok',
        'movies' : bike_list
    }

@api.post('/echoaxios')
def echo_axios():
    print(request)
    data = request.get_json()
    print(data)
    return {
        'status' : 'ok',
        'axios_msg': 'it does work!',
        'data': data
    }

@api.post('/echofetch')
def echo_fetch():
    print(request)
    data = request.get_json()
    print(data)
    return {
        'status' : 'ok',
        'fetch_msg': 'Fetch works too!',
        'data': data
    }