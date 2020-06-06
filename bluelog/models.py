# -*- coding: utf-8 -*-
"""
    :author: sunnyseed
"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bluelog.extensions import db

# from flask import url_for

     

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text, default="")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), default=1)
    # 增加标题图片链接
    pic_url = db.Column(db.String(255), default="")
    username = db.Column(db.String(20), default="")

    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    stars = db.Column(db.Integer, default=0)
    bvid = db.Column(db.String(20), default="")
    aid = db.Column(db.String(20), default="")
    cid = db.Column(db.String(20), default="") 
    vid_url = db.Column(db.String(255), default="")
   
    # @staticmethod
    def to_json(self):
        json_post = {
            # 'url': url_for('api.get_post', id=self.id),
            'id': self.id,
            'title': self.title,
            # 'body': self.body,
            'timestamp': self.timestamp,
            'stars': self.stars,
            'bvid': self.bvid
        }
        return json_post
        
    # @staticmethod
    def from_json(json_post):
        title = json_post.get('title')
        if title is None or title == '':
            raise ValidationError('post does not have a title')
        
        body = json_post.get('body')
        can_comment = json_post.get('can_comment')
        category_id = json_post.get('category_id')
        pic_url = json_post.get('pic_url')
        bvid = json_post.get('bvid')
        stars = json_post.get('stars')
        username = json_post.get('username')
        vid_url = json_post.get('vid_url')

        return Post(title=title,
                    body=body,
                    can_comment=can_comment,
                    category_id=category_id,
                    pic_url=pic_url,
                    bvid=bvid,
                    stars=stars,
                    username=username,
                    vid_url=vid_url
                    )
      

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    post = db.relationship('Post', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    # Same with:
    # replies = db.relationship('Comment', backref=db.backref('replied', remote_side=[id]),
    # cascade='all,delete-orphan')


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
