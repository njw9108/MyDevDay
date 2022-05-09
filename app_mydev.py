from flask import Flask, Blueprint, render_template, jsonify, request # Flask 서버 객체 import
mydev = Blueprint('mydev', __name__)

##############################
# mydevday
##############################

# 공개된 년월 데이터 요청 API
@mydev.route('/mydev', methods=['GET'])
def devday_list():
    return render_template('MyDev/mydev.html')
    
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
