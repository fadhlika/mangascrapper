from flask import Flask, jsonify, abort
from lxml import html
import requests

app = Flask(__name__)

def getUrls(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)

    titles = tree.xpath('//td/strong/a[@href]')

    urls = []

    for title in titles:
        urls.append(title.attrib['href'])
    
    return urls

urls = getUrls("http://mangastream.com/manga")

@app.route('/')
def index():
    return "Hello World!"

@app.route('/manga/all')
def get_all_manga():
    return jsonify({'mangas':urls})

@app.route('/manga/<string:manga_title>')
def get_manga(manga_title):
    manga = [m for m in urls if manga_title in m]
    if len(manga) == 0:
        abort(404)
    return jsonify({"manga":manga})

if __name__ == "__main__":
    app.run()