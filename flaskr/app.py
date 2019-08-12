from flaskr import app, db


@app.route('/')
def index():
    return 'This is the Index Page'


if __name__ == '__main__':
    app.run(debug=True)
