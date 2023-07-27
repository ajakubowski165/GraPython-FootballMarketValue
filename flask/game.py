from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Who is more expensive?'


if __name__ == '__main__':
    app.run(debug=True)