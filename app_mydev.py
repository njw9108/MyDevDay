import jwt
from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for  # Flask 서버 객체 import

from pymongo import MongoClient
app = Flask(__name__)
mydev = Blueprint('mydev', __name__)

import hashlib
import certifi
import datetime

ca = certifi.where()

client = MongoClient('boox.synology.me', 27018, username="mydevday", password="devday2205")
db = client.mydevday_user1

SECRET_KEY = 'mydevday'
##############################
# mydevday
##############################

# mydev 페이지
@mydev.route('/mydev', methods=['GET'])
def devday_list():
    return render_template('MyDev/mydev.html')

# 글 쓰기 페이지
@mydev.route('/mydev/write', methods=['GET'])
def devday_write():
    return render_template('MyDev/write.html')

# 글 읽기 페이지
@mydev.route('/mydev/<devid>', methods=['GET'])
def devday_read(devid):
    print(devid)
    if devid is None:
        return render_template('MyDev/mydev.html')
    else:
        return render_template('MyDev/read.html')

# 특정 년월 데이터 요청 API
@mydev.route('/mydev/<date>', methods=['POST'])
def devday_calendar(date):
    print(f"{date} 년월 API 정보 요청 받음.")
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '내가 작성한 글 목록 조회 성공',
                'row_count': 1,
                'row': [
                    {
                        'user_id': 'c_user',
                        'dev_id': 33,
                        'subject': 'pyCharm 사용법 정리',
                        'content': '사용법 1) ~~~ Blabla..',
                        'memo1': '메모1',
                        'memo2': '메모2',
                        'memo3': '메모3',
                        'memo4': '메모4',
                        'memo5': '메모5',
                        'feeling': '기분 굳~',
                        'emoticon': ';->',
                        'date': '20220505',
                        'like_count': 5,
                    },
                ]
            }
        })


# 내 paycharm 에선 실행되는데 가져오니까 계속 오류나서 일단 주석처리하고 하나씩 살려보자..

# 신규 글 작성
# @mydev.route('/mydev/write', methods=['POST'])
# def write_dev_post():
#     token_receive = request.cookies.get('mytoken')
#     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#     user_info = db.user.find_one({"id": payload["id"]})
#
#     subject_receive = request.form["subject_give"]
#     category_receive = request.form["category_give"]
#     dream_receive = request.form["dream_give"]
#     content_receive = request.form["content_give"]
#     todo_receive = request.form["todo_give"]
#     feeling_receive = request.form["feeling_give"]
#     emoticon_receive = request.form["emoticon_give"]
#     date_receive = request.form["date_give"]
#
#     doc = {
#         "id": user_info["id"],
#         "subject": subject_receive,
#         "category": category_receive,
#         "dream": dream_receive,
#         "content": content_receive,
#         "todo": todo_receive,
#         "feeling": feeling_receive,
#         "emoticon": emoticon_receive,
#         "date": date_receive
#     }
#     db.mydev.insert_one(doc)
#     return jsonify({"result": "success", 'msg': '나의 개발일지 저장 완료!'})

#
# # GET 전체 글 & 유저별 글을 볼수 있음
# @app.route("/devday", methods=['GET'])
# def devday():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         # payload 좋아요 구현 시 사용 예정
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         username_receive = request.args.get("username_give")
#         if username_receive == "":
#             posts = list(db.mydev.find({}).sort("date", -1).limit(10))
#         else:
#             posts = list(db.mydev.find({"id": username_receive}).sort("date", -1).limit(3))
#         for post in posts:
#             post["_id"] = str(post["_id"])
#         return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", "posts": posts})
#     except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
#         return redirect(url_for("/login"))
#
# 로그인 된 유저만 call 할 수 있는 API입니다. (유일하게 작동..)
@app.route('/user/info', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
    return jsonify({'result': 'success', 'nickname': userinfo['name']})
