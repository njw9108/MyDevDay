from pymongo import MongoClient

from flask import Flask, Blueprint, render_template, jsonify, request  # Flask 서버 객체 import

app = Flask(__name__)

client = MongoClient('boox.synology.me', 27018, username="mydevday", password="devday2205")

db = client.mydevday_post

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
    print(devid)
    if devid is None:
        return render_template('MyDev/mydev.html')
    else:
        return render_template('MyDev/read.html')


# 글 수정 페이지
@mydev.route('/mydev/edit', methods=['GET'])
def devday_edit():
    return render_template('MyDev/edit.html')


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
    print(feeling_receive)
    emoticon_receive = request.form['emoticon_give']
    print(emoticon_receive)

    print(writer_receive, date_receive, title_receive, category_receive, goal_receive, todoList_receive,
          todayLearned_receive, feeling_receive, emoticon_receive)

    db.post.insert_one(
        {'writer': writer_receive, 'date': date_receive, 'title': title_receive, 'category': category_receive,
         'goal': goal_receive, 'todayLearned': todayLearned_receive, 'todo': todoList_receive,
         'feeling': feeling_receive, 'emoticon': emoticon_receive})

    return jsonify({'result': 'success', 'msg': '포스팅 완료'})


# 글 수정 요청(Edit)
@mydev.route('/mydev/edit', methods=['POST'])
def edit_dev_post():
    print("글 작성 api 받음")
    writer_receive = request.form['writer_give']
    date_receive = request.form['date_give']
    title_receive = request.form['title_give']
    category_receive = request.form['category_give']
    goal_receive = request.form['goal_give']
    todayLearned_receive = request.form['todayLearned_give']
    todoList_receive = request.form['todoList_give']
    feeling_receive = request.form['feeling_give']
    # emoticon_receive = request.form['emoticon_give']

    print(writer_receive, date_receive, title_receive, category_receive, goal_receive, todoList_receive,
          todayLearned_receive, feeling_receive)

    db.post.updateOne(
        {'writer': writer_receive, 'date': date_receive, 'title': title_receive, 'category': category_receive,
         'goal': goal_receive, 'todayLearned': todayLearned_receive, 'todo': todoList_receive,
         'feeling': feeling_receive})

    return jsonify({'result': 'success', 'msg': '수정 완료'})

# 글 정보 요청(Read)
