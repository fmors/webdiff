from flask import Flask
from v1.routes import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/v1')


@app.route('/')
def hi():
    return 'Welcome to Fernando\'s webdiff!'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
