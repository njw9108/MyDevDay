from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import util
if not hasattr(util, 'dburi') or util.dburi is None:
    util.dburi = 'mongodb://localhost'


##############################
# root
##############################
@app.route('/')
def home():
    return render_template('index.html')
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '3팀 전국구 MyDevDay 입니다.'
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

##############################
# user
##############################

# user 화면 (필요시..) 로그인여부에 따라 다른 URL 또는 Front 구분 처리.
@app.route('/user', methods=['GET'])
def user_page():
    return render_template('user.html')

# user 로그인 요청 API
@app.route('/user', methods=['POST'])
def user_login():
    # login 성공. (필요시 정보 전달 샘플)
    return jsonify({
            'result' : {
                'success': 'true',
                'message': '로그인 성공되었습니다'
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

# user 정보 수정 요청 API
@app.route('/user', methods=['PUT'])
def user_edit():
    # 사용자 정보 수정 처리
    return jsonify('user edit')

# user 삭제 요청 API
@app.route('/user', methods=['DELETE'])
def user_delete():
    # 사용자 삭제 처리
    return


##############################
# mydevday
##############################

# 내가 작성한 년월 데이터 요청 API
@app.route('/mydevday/<date>', methods=['GET'])
def mydevday_calendar(date):
    return date;



##############################
# devday
##############################

# 공개된 년월 데이터 요청 API
@app.route('/devday/<date>', methods=['GET'])
def devday_calendar(date):
    return date;




# 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=8899, debug=True)