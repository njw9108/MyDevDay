from flask import Flask, Blueprint, render_template, jsonify, request # Flask 서버 객체 import
devday = Blueprint('devday', __name__)

##############################
# main
#######################fe#######

# 메인 화면
# 메인 화면
@devday.route('/')
def main():
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
                    },
                ]
            }            
        })
