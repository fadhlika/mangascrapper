from database import db

class Manga(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    link = db.Column(db.Unicode)

    def __init__(self, title, link):
        self.title = title
        self.link = link

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode)
    link = db.Column(db.Unicode)

    manga_id = db.Column(db.Integer, db.ForeignKey('manga.id'))
    manga = db.relationship('Manga', backref=db.backref('manga', lazy='dynamic'))

    def __init__(self, title, link, manga):
        self.title = title
        self.link = link
        self.manga = manga

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer)
    link = db.Column(db.Unicode)
    
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    chapter = db.relationship('Chapter', backref=db.backref('chapter', lazy='dynamic'))

    def __init__(self, no, link, chapter):
        self.no = no
        self.link = link
        self.chapter = chapter