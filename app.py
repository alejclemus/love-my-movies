from flask import Flask, render_template
from flask_caching import Cache
from tmdbv3api import TMDb
import os, json

tmdb = TMDb()
tmdb.api_key = 'YOUR_API_KEY'
tmdb.language = 'en'
tmdb.debug = True

app = Flask(__name__)
app.static_folder = 'templates'
environment=os.getenv("ENVIRONMENT","development")

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

filename = os.path.join(app.static_folder, 'jsons', 'trending_movies.json')
with open(filename) as test_file:
    data = json.load(test_file)


@app.route('/')
@cache.cached(timeout=50)
def index():
    return  render_template('index.html', data=data)

if __name__ == '__main__':
    debug=False
    if environment == "development" or environment == "local":
        debug=True
    app.run(host="0.0.0.0",debug=debug, port=os.environ.get('PORT'))