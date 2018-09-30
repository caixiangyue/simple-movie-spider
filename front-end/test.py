from flask import Flask
from flask import render_template
import pymongo
app = Flask(__name__)

@app.route('/')
def hello_world():
    client = pymongo.MongoClient(host='localhost',port=27017)
    db = client.movie
    movies = db.movies.find()
    # for movie in movies.find():
    #     print(movie)
    return render_template('index.html',movies=movies)

if __name__ == '__main__':
    app.run(host='0.0.0.0')