from flask import Flask, request # flask.py 안에 Flask class 로드
#from flask import request 요청 관련 클래스
#from flask import render_template # html 로드하는 클래스
from werkzeug.utils import secure_filename # 파일이름, 경로에 대한 기본적인 보안
# 내장 변수 __name__을 매개변수로 Flask 클래스를 생성
# 생성된 인스턴스를 app에 저장!!

# flask server 보안 규칙
# 1. html문서들은 render_template로 로드 시
# 반드시 templates 폴더 내에 존재해야 한다.
# 2. 모든 경로에 대해 접근 불가
# 단, static 경로만 접근 가능
import os

if not os.path.exists('static/imgs'):
    os.makedirs('static/imgs')

app = Flask(__name__) 

@app.route('/') # IPv4:port + '/'  경로에 접속 시 호출되는 함수 정의!!
def index():
    # return 에 쓸수있는 결과는 html
    # 1. 태그를 직접 
    # 2. 라이브러리 render_template 이용

    # request 관련 페이지들은
    # route 설정시 반드시 전송방식을 정의해야 한다
    # 받아오는 코드
    
    return """
        <style>
          form{
             transform: scale();
             transform-origin: top left;
          }
        </style>
        <form action="/detect" method="post" enctype="multipart/form-data">
            <input type="file" name="file"><br>
            <input type="submit" value="전송">
        </form>
    """

@app.route('/detect', methods=['POST']) # root 경로에서 넘어 온 이미지를 받아오는 페이지
def detect():
    # 받아오는코드
    # request 관련 페이지들은
    # route 설정 시 반드시 전송방식을 정의해야 한다
    # GET -> request.args['Key값']
    # POST -> request.form['Key값']
    # file -> request.files['Key값']

    f = request.files['file']
    filename = secure_filename(f.filename)
    img_path = 'static/imgs/' + filename
    f.save(img_path)
    i = ImageDetect() # 대문자로 시작 + 소괄호 => 클래스
    result = i.detect_img(img_path)

    if result.size == 0:
        return '<h1>탐색 결과 없음..</h1>'
    
    conf = result[0][4]
    nc = int(result[0][5]) # 실수타입 정수로 형변환
    label = i.data[nc]
    output = '<h1>{}일 확률이 {:.2f}%입니다.</h1>'.format(label, conf * 100)

    return output
    # file관련 경로, 이름들은 보안을 지켜주자

# 내가 직접 실행시(run) 내장변수 __name__이 __main__으로 변한다
if __name__ == '__main__':
    app.run(host = 'localhost', port = 5021)
