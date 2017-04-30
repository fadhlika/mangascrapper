from flask import Flask, jsonify, abort
import flask_restless as rest
from database import db
from lxml import html
import requests
from manga import Manga, Chapter, Page

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.cli.command('initdb')
def initialize_database():
    db.create_all()

    manga_page = requests.get('http://mangastream.com/manga')
    manga_tree = html.fromstring(manga_page.content)

    mangas = manga_tree.xpath('//td/strong/a[@href]')

    for manga in mangas:
        mng = Manga(manga.text, manga.attrib['href'])
        db.session.add(mng)
        
        chapter_page = requests.get(mng.link)
        chapter_tree = html.fromstring(chapter_page.content)

        chapters = chapter_tree.xpath('//td/a[@href]')
        for chapter in chapters:
            ch = Chapter(chapter.text, chapter.attrib['href'], mng)
            db.session.add(ch)

            page_page = requests.get(ch.link)
            page_tree = html.fromstring(page_page.content)

            page_number = int(page_tree.xpath("//li/a[contains(text(), 'Last Page')]")[0].text.split('(')[1].split(')')[0])

            for i in range(1, page_number):
                page_link = ch.link[:-1] + str(i)
                
                page_link_page = requests.get(page_link)
                page_link_tree = html.fromstring(page_link_page.content)

                image_link = page_link_tree.xpath("//div/a/img")[0]
                
                page = Page(i, 'http:' + image_link.attrib['src'], ch)
                db.session.add(page)

                print(mng.title, ch.title, page.link)

    db.session.commit()

manager = rest.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Manga, methods=['GET'])
manager.create_api(Chapter, methods=['GET'])
manager.create_api(Page, methods=['GET'])

@app.route('/')
def index():
    return "Hello World!"

if __name__ == "__main__":
    app.run()