import flask 

IP = '10.245.81.64'
app = flask.Flask(__name__)
@app.route('/')
def index():
    return 'Hello world'
if __name__ == '__main__':
    app.run(debug=True, port=80, host=IP)
