from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route(['GET'], "/userData")
def getUserData(id: int):
    pass

if __name__ == '__main__':
    app.run(debug=True)