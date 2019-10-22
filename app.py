from flask import Flask, render_template
from flask_caching import Cache
import os, json, requests

response = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=4d2360655220d65f91d1ebbde776d1c1')
data1 = response.json()
with open('trendingMoviesAPI.json', 'w', encoding='utf-8') as f:
    json.dump(data1, f, ensure_ascii=False, indent=4)

app = Flask(__name__)
app.static_folder = 'templates'
environment=os.getenv("ENVIRONMENT","development")

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)


@app.route('/')
@cache.cached(timeout=50)
def index():
    return  render_template('index.html', data=data1)

if __name__ == '__main__':
    debug=False
    if environment == "development" or environment == "local":
        debug=True
    app.run(host="0.0.0.0",debug=debug, port=os.environ.get('PORT'))