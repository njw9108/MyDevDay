from flask import Flask, Blueprint, render_template, jsonify, request # Flask 서버 객체 import
user = Blueprint('user', __name__)

##############################
# user
##############################

# user 화면 (필요시..) 로그인여부에 따라 다른 URL 또는 Front 구분 처리.
@user.route('/user', methods=['GET'])
def user_page():
    return render_template('User/login.html')

# user 로그인 시도 요청 API
@user.route('/userlogin', methods=['POST'])
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
@user.route('/userislogin', methods=['POST'])
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
@user.route('/userinfo', methods=['POST'])
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

