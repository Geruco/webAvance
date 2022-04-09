from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    profileId = db.Column(db.Integer, db.ForeignKey(
        'profile.id'), nullable=False, default=3)
    profile = db.relationship(
        'Profile', backref=db.backref('users', lazy=True))

    def init(self, username, password, last_name, first_name, email):
        self.username = username
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.email = email


class Profile(db.Model):
    tablename = 'profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def init(self, name):
        self.name = name


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_publication = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow)
    date_revision = db.Column(
        db.DateTime, nullable=True, default=datetime.utcnow)
    statut = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship('User', backref=db.backref('articles', lazy=True))

    def __init__(self, userId, title, content):
        self.userId = userId
        self.title = title
        self.content = content


class Commentary(db.Model):
    __tablename__ = 'commentary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    articleId = db.Column(db.Integer, db.ForeignKey(
        'article.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship(
        'User', backref=db.backref('commentaries', lazy=True))
    article = db.relationship(
        'Article', backref=db.backref('commentaries', lazy=True))

    def __init__(self, userId, articleId, text):
        self.userId = userId
        self.articleId = articleId
        self.text = text


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name


class TagArticle(db.Model):
    __tablename__ = 'tagarticle'
    articleId = db.Column(db.Integer, db.ForeignKey(
        'article.id'), primary_key=True, nullable=False)
    tagId = db.Column(db.Integer, db.ForeignKey('tag.id'),
                      primary_key=True, nullable=False)

    article = db.relationship(
        'Article', backref=db.backref('tagsarticle', lazy=True))
    tag = db.relationship('Tag', backref=db.backref('tagsarticle', lazy=True))

    def __init__(self, articleId, tagId):
        self.articleId = articleId
        self.tagId = tagId


class Reaction(db.Model):
    __tablename__ = 'reaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255), nullable=False)
    icone = db.Column(db.String(255), nullable=False)

    def __init__(self, description, icone):
        self.description = description
        self.icone = icone


class ReactionArticle(db.Model):
    __tablename__ = 'reactionarticle'
    articleId = db.Column(db.Integer, db.ForeignKey(
        'article.id'), primary_key=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey(
        'user.id'), primary_key=True, nullable=False)
    reactionId = db.Column(db.Integer, db.ForeignKey(
        'reaction.id'), primary_key=True, nullable=False)

    article = db.relationship(
        'Article', backref=db.backref('reactionsArticle', lazy=True))
    user = db.relationship(
        'User', backref=db.backref('reactionsArticle', lazy=True))
    reaction = db.relationship(
        'Reaction', backref=db.backref('reactionsArticle', lazy=True))

    def __init__(self, articleId, userId, reactionId):
        self.articleId = articleId
        self.userId = userId
        self.reactionId = reactionId
