from flask import Flask
from route.user import blueprint as user_blueprint
from route.nba import blueprint as nba_blueprint
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(nba_blueprint)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
