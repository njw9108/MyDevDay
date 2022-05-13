from flask import Flask, Blueprint, render_template, jsonify, request # Flask 서버 객체 import
devday = Blueprint('devday', __name__)

# mongo
from pymongo import MongoClient
client = MongoClient('mongodb://mydevday:devday2205@boox.synology.me/admin', 27018)
db = client.mydevday

# time
import time

##############################
# main
##############################

# 메인 화면
@devday.route('/')
def main():
    # mongo test
    ip_addr = request.remote_addr;
    url = request.url;
    user_agent = request.user_agent.string;
    current_time = time.strftime('%y-%m-%d %H:%M:%S');
    doc = {'ip_addr':ip_addr, 'url':url, 'user_agent':user_agent, 'connect_time':current_time}
    db.log.insert_one(doc)

    return render_template('DevDay/index.html')
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '3팀 전국구 MyDevDay.'
            },
            'row_count': 1,
            'row': [
                {
                    'name': 'Andy',
                    'tel': '010-3292-3892',
                    'email': 'booxboox@naver.com'
                },
            ]
        })
# test page
@devday.route('/test')
def test():
    return render_template('DevDay/index_test.html')

# 공개된 전체 데이터 요청 API
@devday.route('/devday', methods=['POST'])
def devday_list():
    print('devday_list')
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '전체 공개 devday 목록 예제',
                'row_count': 2,
                'row': [
                    {
                        'user_id': 'a_user',
                        'dev_id': 1,
                        'subject': 'Flask 사용법 정리',
                        'content': '사용법 1) ~~~ Blabla..',
                        'memo1': '메모1',
                        'memo2': '메모2',
                        'memo3': '메모3',
                        'memo4': '메모4',
                        'memo5': '메모5',
                        'feeling': '기분 짱',
                        'emoticon': ';-)',
                        'date': '20220501',
                        'like_count': 123,
                        'comment_count': 321,
                    },
                    {
                        'user_id': 'z_user',
                        'dev_id': 99,
                        'subject': 'Python은 이렇게~~',
                        'content': 'Python 정의 1) ~~~ Blabla..',
                        'memo1': '메모1',
                        'memo2': '메모2',
                        'memo3': '메모3',
                        'memo4': '메모4',
                        'memo5': '메모5',
                        'feeling': '기분 So-so',
                        'emoticon': ':-|',
                        'date': '20220505',
                        'like_count': 3,
                        'comment_count': 9,
                    },
                ]
            }            
        })
