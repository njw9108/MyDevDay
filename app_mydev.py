from pymongo import MongoClient

from flask import Flask, Blueprint, render_template, jsonify, request  # Flask 서버 객체 import
from bson import ObjectId

import jwt
import datetime
import hashlib
from datetime import datetime, timedelta

app = Flask(__name__)

client = MongoClient('boox.synology.me', 27018, username="mydevday", password="devday2205")

db = client.mydevday

SECRET_KEY = 'mydevday'

mydev = Blueprint('mydev', __name__)


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
    print('글 읽기 페이지 devid = ', devid)
    if devid is None:
        return render_template('MyDev/mydev.html')
    else:
        return render_template('MyDev/read.html', devid=devid)

# 글 수정 페이지
@mydev.route('/mydev/write/<devid>', methods=['GET'])
def devday_edit(devid):
    print('수정 페이지 devid = ', devid)
    return render_template('MyDev/write.html', devid=devid)


# 특정 년월 데이터 요청 API
@mydev.route('/mydev/<date>', methods=['POST'])
def devday_calendar(date):
    print(f"{date} 년월 API 정보 요청 받음.")
    return jsonify({
        'result': {
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


# 신규 글 작성
@mydev.route('/mydev/write', methods=['POST'])
def write_dev_post():
    print("글 작성 api 받음")
    writer_receive = request.form['writer_give']
    date_receive = request.form['date_give']
    title_receive = request.form['title_give']
    category_receive = request.form['category_give']
    goal_receive = request.form['goal_give']
    todayLearned_receive = request.form['todayLearned_give']
    todoList_receive = request.form['todoList_give']
    feeling_receive = request.form['feeling_give']
    emoticon_receive = request.form['emoticon_give']

    print(writer_receive, date_receive, title_receive, category_receive, goal_receive, todoList_receive,
          todayLearned_receive, feeling_receive, emoticon_receive)

    db.post.insert_one(
        {'writer': writer_receive, 'date': date_receive, 'title': title_receive, 'category': category_receive,
         'goal': goal_receive, 'todayLearned': todayLearned_receive, 'todo': todoList_receive,
         'feeling': feeling_receive, 'emoticon': emoticon_receive})

    return jsonify({'result': 'success', 'msg': '포스팅 완료'})


# 글 읽기(Read)
@mydev.route('/mydev/read/<devid>', methods=['POST'])
def read_dev_post(devid):
    print("글 읽기 api 받음")

    devday = db.post.find_one({'_id': ObjectId(devid)})

    data = {
        'user_id': devday['writer'],
        'dev_id': str(devday['_id']),
        'subject': devday['title'],
        'content': '',
        'category': devday['category'],
        'memo1': devday['goal'],
        'memo2': devday['todayLearned'],
        'memo3': devday['todo'],
        'memo4': '',
        'memo5': '',
        'feeling': devday['feeling'],
        'emoticon': devday['emoticon'],
        'date': devday['date'],
    }

    return jsonify({
        'result': {
            'success': 'true',
            'message': 'devday 가져오기 성공',
            'data': data,
        }
    })


# 글 수정 요청(Edit)
@mydev.route('/mydev/write/<devid>', methods=['PUT'])
def edit_dev_post(devid):
    print("글 수정 api 받음")

    writer_receive = request.form['writer_give']
    date_receive = request.form['date_give']
    title_receive = request.form['title_give']
    category_receive = request.form['category_give']
    goal_receive = request.form['goal_give']
    todayLearned_receive = request.form['todayLearned_give']
    todoList_receive = request.form['todoList_give']
    feeling_receive = request.form['feeling_give']
    emoticon_receive = request.form['emoticon_give']

    print(writer_receive, date_receive, title_receive, category_receive, goal_receive, todoList_receive,
          todayLearned_receive, feeling_receive, emoticon_receive)

    db.post.update_one({'_id': ObjectId(devid)}, {
        '$set': {'writer': writer_receive, 'date': date_receive, 'title': title_receive, 'category': category_receive,
                 'goal': goal_receive, 'todayLearned': todayLearned_receive, 'todo': todoList_receive,
                 'feeling': feeling_receive, 'emoticon': emoticon_receive}})

    return jsonify({'result': 'success', 'msg': '수정 완료'})

# 글 삭제 요청(Delete)
@mydev.route('/mydev/write/<devid>', methods=['DELETE'])
def delete_dev_post(devid):
    print("글 삭제 api 받음")

    db.post.delete_one({'_id': ObjectId(devid)})

    return jsonify({'result': 'success', 'msg': '삭제 완료'})

# 내가 쓴글 데이터 요청 API
@mydev.route('/mydev', methods=['POST'])
def mydev_list():
    print('mydev_list')

    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    print(payload["id"])

    datas = list(db.post.find({"writer": payload["id"]}).sort('date', -1))

    ret_datas = [];
    for d in datas:
        ret_datas.append({
            'user_id': d['writer'],
            'dev_id': str(d['_id']),
            'subject': d['title'],
            'content': '',
            'category': d['category'],
            'memo1': d['goal'],
            'memo2': d['todayLearned'],
            'memo3': d['todo'],
            'memo4': '',
            'memo5': '',
            'feeling': d['feeling'],
            'emoticon': '',
            'date': d['date'],
            'like_count': 123,  # 임시
            'comment_count': 321,  # 임시
        })

    if len(datas) >= 1:
        return jsonify({
            'result': {
                'success': 'true',
                'message': 'mydev 목록 가져오기 성공',
                'row_count': len(datas),
                'row': ret_datas,
            }
        })
    else:
        return jsonify({
            'result': {
                'success': 'false',
                'message': 'mydev 목록이 없습니다',
                'row_count': 0,
                'row': [],
            }
        })



# 좋아요
@mydev.route('/mydev/<devid>/like', methods=['POST'])
def dev_post_like(devid):
    print("좋아요 api 받음 devid=" + devid)
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    datas = list(db.devday_like.find({"dev_id": devid, "user_id": payload["id"]}).sort('date', -1))
    if (1 <= len(datas)):
        return jsonify({
            'result': { 'success': 'false', 'message': '이미 좋아요를 하셨습니다.' }
        })
    else:
        db.devday_like.insert_one({'dev_id': devid, 'user_id': payload['id']})
        return jsonify({
            'result': { 'success': 'true', 'message': '좋아요 성공' }
        })
# 좋아요 해제
@mydev.route('/mydev/<devid>/like', methods=['DELETE'])
def dev_post_unlike(devid):
    print("좋아요 삭제 api 받음 devid=" + devid)
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    db.devday_like.delete_one({'dev_id': devid, 'user_id': payload['id']})
    return jsonify({
        'result': { 'success': 'true', 'message': '좋아요 삭제 성공' }
    })
# 좋아요 갯수
@mydev.route('/mydev/<devid>/likecount', methods=['POST'])
def dev_post_likecount(devid):
    print("좋아요 갯수 요청 api 받음 devid=" + devid)
    datas = list(db.devday_like.find({'dev_id': devid}))
    print(len(datas))
    return jsonify({
        'result': { 'success': 'true', 'message': '좋아요 삭제 성공', 'row_count':1,
            'row': [
                { 'like_count' : len(datas) },
            ]
        }
    })

# 댓글 추가
@mydev.route('/mydev/<devid>/comment', methods=['POST'])
def dev_post_comment_add(devid):
    print("댓글 추가 api 받음 devid=" + devid)
    comment_receive = request.form['comment_give']
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    currdate = datetime.today().strftime("%Y/%m/%d %H:%M:%S")

    db.devday_comment.insert_one({'dev_id': devid, 'user_id': payload['id'], 'comment': comment_receive, 'date':currdate})
    return jsonify({
        'result': { 'success': 'true', 'message': '댓글 성공' }
    })
# 댓글 수정
@mydev.route('/mydev/<devid>/comment/<commentid>', methods=['PUT'])
def dev_post_comment_edit(devid, commentid):
    print("댓글 수정 api 받음 devid=" + devid + ", commentid=" + commentid)
    comment_receive = request.form['comment_give']
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    db.devday_comment.update_one({'_id':ObjectId(commentid), 'dev_id':devid, 'user_id':payload['id']}, {
        '$set': {'comment': comment_receive }})
    return jsonify({
        'result': { 'success': 'true', 'message': '댓글 수정 성공' }
    })
# 댓글 삭제
@mydev.route('/mydev/<devid>/comment/<commentid>', methods=['DELETE'])
def dev_post_comment_del(devid, commentid):
    print("댓글 삭제 api 받음 devid=" + devid + ", commentid=" + commentid)
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    db.devday_comment.delete_one({'_id':ObjectId(commentid), 'dev_id':devid, 'user_id':payload['id']})
    return jsonify({
        'result': { 'success': 'true', 'message': '댓글 삭제 성공' }
    })
# 댓글 목록
@mydev.route('/mydev/<devid>/commentlist', methods=['POST'])
def dev_post_commentlist(devid):
    print("댓글 목록 api 받음 devid=" + devid)

    datas = list(db.devday_comment.find({'dev_id': devid}))
    ret_datas = [];
    for d in datas:
        ret_datas.append({
            'comment_id': str(d['_id']),
            'user_id': d['user_id'],
            'comment': d['comment'],
            'date': d['date'],
        })

    return jsonify({
        'result': { 'success': 'true', 'message': '댓글 성공', 'row_count':len(datas),
        'row': ret_datas }
    })