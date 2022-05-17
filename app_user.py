from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for  # Flask 서버 객체 import
from pymongo import MongoClient
# 패키지? 각자 설치해야함(근데 설치한걸 푸쉬로 공유는 불가능 한가? 질문해야지)
# PyJWT 패키지 설치하기
import jwt
import datetime
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('boox.synology.me', 27018, username="mydevday", password="devday2205")

db = client.mydevday_user1

SECRET_KEY = 'mydevday'

user = Blueprint('user', __name__)


##############################
# user
##############################

# user 화면 (필요시..) 로그인여부에 따라 다른 URL 또는 Front 구분 처리.
"""
@user.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        print(user_info)
        return render_template('DevDay/index.html', name=user_info["name"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("user.login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("user.login", msg="로그인 정보가 존재하지 않습니다."))
"""

@user.route('/user', methods=['GET'])
def login():
    msg = request.args.get("msg")
    return render_template('User/login.html', msg=msg)


# user 가입
@user.route('/user/signup', methods=['GET'])
def register():
    return render_template('User/signup.html')


#################################
#  로그인을 위한 API
#################################

# user 회원가입 API
@user.route('/user/signup/create', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'name': name_receive})

    return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다'})


# user 회원가입 ID 중복확인
@user.route('/user/signup/idcheck', methods=['POST'])
def id_check():
    sameid_receive = request.form['id_give']
    exists = db.user.find_one({"id": sameid_receive}, {'_id': False})
    print(sameid_receive, exists)
    return jsonify({'result': 'success', 'sameid': exists})


# user 로그인 API
@user.route('/user/login', methods=['POST'])
def user_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash}, {'_id': False})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'msg': '로그인 성공.', 'token': token, })
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# user 사용자 정보 확인 api
@user.route('/user/info', methods=['POST'])
def user_valid():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload["id"]})
        print(user_info)
        return jsonify({
            'result' : {
                'success': 'true',
                'message': '사용자 정보 성공',
                'row_count': 1,
                'row': [
                    {
                        'user_id': payload["id"],
                        'user_name': user_info["name"],
                    },
                ]
            }
        })
    except jwt.ExpiredSignatureError:
        return jsonify({
            'result' : {
                'success': 'false',
                'message': '사용자 정보 실패 (ExpiredSignatureError)'
            },
            'row_count': 0,
            'row': [{},]
        })
    except jwt.exceptions.DecodeError:
        return jsonify({
            'result' : {
                'success': 'false',
                'message': '사용자 정보 실패 (DecodeError)'
            },
            'row_count': 0,
            'row': [{},]
        })

# user 사용자 로그인 여부 확인 api
@user.route('/user/islogin', methods=['POST'])
def checkcookie():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return jsonify({
            'result' : {
                    'success': 'true',
                    'message': '사용자 로그인 되어 있음',
                    'row_count': 0,
                    'row': [ {}, ]
                }
            })
    else :
        return jsonify({
            'result' : {
                    'success': 'false',
                    'message': '사용자 로그인 되어 있지 않음',
                    'row_count': 0,
                    'row': [ {}, ]
                }
            })

# user 정보 수정페이지
@user.route('/user/update', methods=['GET'])
def update():
    return render_template('User/updateinfo.html')