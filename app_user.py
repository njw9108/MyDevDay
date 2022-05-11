from pymongo import MongoClient
from flask import Flask, Blueprint, render_template, session, jsonify, request, redirect, url_for # Flask 서버 객체 import

app = Flask(__name__)

client = MongoClient('boox.synology.me', 27018 ,username="mydevday", password="devday2205" )
db = client.mydevday_user1

SECRET_KEY = 'mydevday'

import jwt
import datetime
import hashlib

user = Blueprint('user', __name__)
##############################
# user
##############################

# user 화면 (필요시..) 로그인여부에 따라 다른 URL 또는 Front 구분 처리.
@user.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

@user.route('/user', methods=['GET'])
def user_page():
    msg = request.args.get("msg")
    return render_template('User/login.html', msg=msg)

# user 가입
@user.route('/user/signup', methods=['GET'])
def user_signup():
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

    db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': name_receive})

    return jsonify({'result': 'success', 'msg': '회원가입이 완료되었습니다'})

# user 회원가입 ID 중복확인
@user.route('/user/signup/idcheck', methods=['POST'])
def id_check():
    sameid_receive = request.form['id_give']
    exists = db.users.find_one({"id": sameid_receive})
    print(sameid_receive, exists)
    return jsonify({'result': 'success', 'sameid': exists})

    

# user 로그인 시도 요청 API
@user.route('/user/login', methods=['POST'])
def user_try_login():
    # login 시도. (로그인 성공후 필요시 정보 전달 샘플)
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '로그인 성공되었습니다',
                'row_count': 1,
                'row': [
                    {
                        'user_id': 'a_user',
                    },
                ]
            }
        })

# user 로그인 여부 요청 API
@user.route('/user/islogin', methods=['POST'])
def user_is_login():
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '사용자가 로그인 되어 있습니다.',
                'row_count': 0,
                'row': [
                    {
                    }
                ]
            }
        })
# user 사용자 정보 요청 API
@user.route('/user/info', methods=['POST'])
def user_info():
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '사용자가 정보 조회 성공',
                'row_count': 1,
                'row': [
                    {
                        'user_id': 'z_user',
                        'user_name': 'zzzzz',
                    }
                ]
            }
        })

