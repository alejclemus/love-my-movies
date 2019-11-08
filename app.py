from flask import Flask, render_template
from flask_caching import Cache
from tmdbv3api import TMDb, Movie
import os, json, requests, redis

response = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=4d2360655220d65f91d1ebbde776d1c1')
data1 = response.json()
with open('trendingMoviesAPI.json', 'w', encoding='utf-8') as f:
    json.dump(data1, f, ensure_ascii=False, indent=4)

##https://pypi.org/project/tmdbv3api/    
class database:
    key = "4d2360655220d65f91d1ebbde776d1c1"
    redis_server = None
    enviroment = ""
    
    def __init__(self, key, enviroment):
        self.key = key
        self.enviroment=enviroment
    

    def beginRedis(self):
        movie = Movie()
        if self.enviroment == "development":
            self.enviroment="localhost"
        else:
            self.enviroment="docker_redis"

        self.redis_server = redis.StrictRedis(host=self.enviroment, port=6379, db=0)
        api = TMDb()
        api.key = self.key
        self.getPopular(movie)

    def getPopular(self, movie):
        popular = movie.popular()
        self.saveMovies(popular)


    def saveMovies(self, eachMovie):
        with self.redis_server.pipeline() as pipe:
            for eachMovie in eachMovie:
                pipe.hset(eachMovie.title, "title" ,eachMovie.title)
                pipe.hset(eachMovie.title, "overview" ,eachMovie.overview)
                pipe.hset(eachMovie.title, "poster_path" ,eachMovie.poster_path)
                pipe.hset(eachMovie.title, "vote_count", eachMovie.vote_count)
                pipe.hset(eachMovie.title, "id", eachMovie.id)
            pipe.execute()    


app = Flask(__name__)
tmdb = TMDb()
key = "4d2360655220d65f91d1ebbde776d1c1"
tmdb.api_key = '4d2360655220d65f91d1ebbde776d1c1'
app.static_folder = 'templates'
environment=os.getenv("ENVIRONMENT","development")

database = database(key, environment)
database.beginRedis()
redis_server=database.redis_server

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/', methods=['POST','GET'])
@cache.cached(timeout=50)
def index():
    return  render_template('index.html', data=data1, redis_server=redis_server)

if __name__ == '__main__':
    debug=False
    if environment == "development" or environment == "local":
        debug=True
    app.run(host="0.0.0.0",debug=debug, port=os.environ.get('PORT'))