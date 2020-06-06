# -*- coding: utf-8 -*-
from flask import Flask
from datetime import datetime
from bluelog.models import Post #大写
from bluelog.extensions import db
import os, json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data-dev.db')
db.init_app(app)


def file2jsonlist(input_file):
    in_file = open(input_file, 'r')
    jsonlist = json.loads(in_file.read())
    print(f"{input_file}, done.")
    in_file.close()
    return(jsonlist)

print("1. 读取json")

bv_list = file2jsonlist("bluelog/static/bv_pic/bv.json")

new_list = []

print("2. issues数据清洗")
for i in bv_list:
    one_post = Post(
        title = i["title"],
        body = i["desc"],
        #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        can_comment = True,
        category_id = 1,
        pic_url = f"{i['bvid']}.jpg",
        bvid = i["bvid"],
        stars = i["stat"]["favorite"]//100,
        username = i["owner"]["name"],
        aid = i["aid"],
        cid = i["cid"],
        # <iframe src="//player.bilibili.com/player.html?aid={{ post.aid }}&bvid={{ post.bid }}&cid={{ post.cid}}&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" high_quality=1> </iframe>
        vid_url = f'<iframe src="//player.bilibili.com/player.html?bvid={i["bvid"]}&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" high_quality=1> </iframe>'    
    )
    # print(one_post)
       
    with app.app_context():
        # 不重复添加
        if len(Post.query.filter_by(bvid=i["bvid"]).all()) == 0:
            db.session.add(one_post)
            db.session.commit()
            print(f"Adding...{i['bvid']}")
        else:
            print(f"Duplicated...{i['bvid']}")

"""
refer
https://stackoverflow.com/questions/46540664/no-application-found-either-work-inside-a-view-function-or-push-an-application

"""