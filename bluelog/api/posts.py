# sunnyseed edited
from flask import jsonify, request, g, url_for, current_app
from ..extensions import db
from ..models import Post #, Permission
from . import api
# from .decorators import permission_required
from .errors import forbidden
# 日志
import logging

logging.basicConfig(filename='post.log', level=logging.INFO)


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=10, # current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1)
    json_posts = []
    for post in posts:
        json_posts.append(post.to_json())
    return jsonify({
        'posts': json_posts, #[post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
# @auth.login_required
# @permission_required(Permission.WRITE)
def new_post():
    post = Post.from_json(request.json)
    logging.error(request.json)
    # post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id)}
