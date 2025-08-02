from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, DevOps!"

@app.route("/about")
def about():
    return "<h2>이것은 소개 페이지입니다.</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80) 
    # app.run()
    # 0.0.0.0 은 전체 네트워크 인터페이스에 연결하라는 의미로서, 내부망 노출로 인한 보안위험성
    # port:80 은 http 통신의 표준포트로서 포트충돌이 가능성이 있는 1024번 이하의 포트에 속한다. 
