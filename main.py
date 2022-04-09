import json
from xml.dom.minidom import Identified
from xml.etree.ElementTree import tostring
import pytest
from flask import Flask, render_template, request, session, url_for, flash, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, user_logged_in
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Commentary, Reaction, ReactionArticle, Tag, TagArticle, User, Article, Profile, db
from config import Config, DevConfig, ProdConfig
from datetime import datetime
# pip install pymysql
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.static_folder = Config.STATIC_FOLDER
app.config['SECRET_KEY'] = Config.SECRET_KEY
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Declaration des fonctions utilitaires


def showProfile(): # Permet de recuperer tous les profils
    profiles = Profile.query.order_by(Profile.name).all()
    return profiles

def showTags():
    tags = Tag.query.order_by(Tag.name).all()
    return tags


def groupArticles(liste):
    completeListe = []
    to_skip = []
    for i in range(len(liste)):
        if i not in to_skip:  # Si la ligne n'a pas deja ete traite
            tagListe = []
            tagListe.append(liste[i][2].name)  # On ajoute le tag a la liste
            for j in range(len(liste)):
                # Si L'article est le meme, on ajoute le tag a la liste
                if(liste[j][0].id == liste[i][0].id) and (i != j):
                    tagListe.append(liste[j][2].name)
                    # On skip la ligne quand on retombe dessus
                    to_skip.append(j)
            completeListe.append([liste[i][0], liste[i][1], tagListe])
    return completeListe


def Login(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not sha256_crypt.verify(password, user.password):
        return False
    # Si la condition au dessus est sautee, alors l'utilisateur a les bons credentials

    login_user(user)
    return True


def AddUser(username, password, first_name, last_name, email):
    user = User.query.filter_by(username=username).first()
    if user:  # On verifie que le nom d'utilisateur ne soit pas deja utilise
        return False
    new_user = User(username=username, password=sha256_crypt.encrypt(
        password), first_name=first_name, last_name=last_name, email=email)  # On hash le mot de passe
    db.session.add(new_user)  # On ajoute l'utilisateur a la bdd
    db.session.commit()
    return True

# Declaration des routes


@app.route('/')
def default():  # Route par defaut = index
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index():
    nb = -1
    liste = []
    if request.method == 'GET':  # Si on a un filtre actif, la quantite d'article charge differe
        listeUser = User.query.order_by(User.username).all()
        if request.args.get('articles'):
            if request.args.get('articles') == 'all' or request.args.get('articles') == 0:
                listeArticle = db.session.query(
                    Article, User, Tag).join(User, User.id == Article.userId).join(TagArticle, TagArticle.articleId == Article.id).join(Tag, Tag.id == TagArticle.tagId).order_by(Article.date_publication.desc()).all()
            else:
                nb = int(request.args.get('articles'))
    if(nb == -1):  # -1 = valeur par defaut : on charge 10 articles
        listeArticle = db.session.query(
            Article, User, Tag).join(User, User.id == Article.userId).join(TagArticle, TagArticle.articleId == Article.id).join(Tag, Tag.id == TagArticle.tagId).order_by(Article.date_publication.desc()).limit(10).all()
    else:  # Sinon on charge le nombre d'article demandés
        listeArticle = db.session.query(
            Article, User, Tag).join(TagArticle, TagArticle.articleId == Article.id).join(Tag, Tag.id == TagArticle.tagId).order_by(Article.date_publication.desc()).limit(nb).all()
    for row in listeArticle:
        article = row[0]
        user = row[1]
        tag = row[2]
        liste.append([article, user, tag])
    liste = groupArticles(liste)
    return render_template("index.html", liste=liste, listeUser=listeUser)


@ app.route('/logout/')
def Logout():
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('index'))


@ app.route('/connexion/', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Si les champs ne sont pas ou mal remplis, on renvoie une erreur
        if not username:
            return render_template('connexion.html', error=1)
        elif not password:
            return render_template('connexion.html', error=2)
        else:  # Sinon on connecte l'utilisateur
            if(Login(username, password)):  # Si la connection est reussie
                return redirect(url_for('index'))
            else:  # Sinon on retourne une erreur
                return render_template('connexion.html', error=3)
    return render_template('connexion.html')


@ app.route('/inscription/', methods=['GET', 'POST'])
def inscription():
    profiles = showProfile()
    if request.method == 'POST': # On récupère les données entrées par l'usager
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Si les champs ne sont pas ou mal remplis, on renvoie une erreur
        if not username:
            return render_template("inscription.html", error=1)
        elif not password:
            return render_template("inscription.html", error=2)
        elif not confirm_password:
            return render_template("inscription.html", error=3)
        elif password != confirm_password:
            return render_template("inscription.html", error=4)

        else:  # Sinon on ajoute l'utilisateur
            if AddUser(username, password, first_name, last_name, email):
                return redirect(url_for('connexion'))
            else:
                return render_template("inscription.html", error=5)
    return render_template('inscription.html')


@ app.route('/article/<id>', methods=['GET'])
def article(id):
    listeComments = []
    # On recupere tous les articles
    article = Article.query.filter(Article.id == id).one()
    # On recupere l'auteur de l'article
    user = User.query.filter(User.id == article.userId).one()
    comments = Commentary.query.filter(
        Commentary.articleId == article.id).order_by(Commentary.date.desc()).all()  # On recupere tout les commentaires lies a l'article
    for comment in comments:  # Pour chaque commentaire :
        # On recupere le nom de l'auteur
        author = User.query.filter(User.id == comment.userId).one()
        # On lie le nom et le commentaire dans un array
        listeComments.append([author, comment])
    finalReactions = []
    if current_user.is_authenticated:
        reactions = db.session.query(Reaction).all()
        for reaction in reactions:
            if ReactionArticle.query.filter(ReactionArticle.articleId == id).filter(ReactionArticle.userId == current_user.id).filter(ReactionArticle.reactionId == reaction.id).count() != 0:
                finalReactions.append([reaction, 1])
            else:
                finalReactions.append([reaction, 0])
    # On envoie les donnees a l'html
    return render_template('article.html', article=article, user=user, comments=listeComments, reactions=finalReactions)


@app.route('/addArticle/', methods=['GET', 'POST'])
def addArticle():
    tags = showTags()
    if request.method == 'POST': # On récupère les données entrées par l'usager
        newTitle = request.get_json()[0]
        newContent = request.get_json()[1]
        allTags = request.get_json()[2]
        new_article = Article(
            int(current_user.id), newTitle, newContent)
        db.session.add(new_article)  # On ajoute l'article a la bd
        for tag in allTags:
            tagId = db.session.query(Tag.id).filter(Tag.name == tag).one()
            new_tagArticle = TagArticle(articleId=int(
                new_article.id), tagId=int(tagId[0]))
            # On ajoute chaque tagArticle lie a l'article
            db.session.add(new_tagArticle)
        db.session.commit()

    return render_template('addArticle.html', tags=tags)


@ app.route('/user/<id>', methods=['GET'])
def user(id):
    # On recupere le user
    user = User.query.filter(User.id == id).one()
    profile = Profile.query.filter(Profile.id == user.profileId).one()
    listProfile = Profile.query.order_by(Profile.id).all()
    # On envoie les donnees a l'html
    return render_template('user.html', user=user, profile=profile, listProfile=listProfile)


@app.route('/tags/')
def tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/reactions/')
def reactions():
    reactions = Reaction.query.all()
    return render_template('reactions.html', reactions=reactions)

# Fin des routes - pages


@app.route('/addComment/', methods=['POST'])
def addComment():
    if request.method == 'POST':
        text = request.form['text']
        articleId = request.form['articleId']
        if not text or text == '':  # Si le texte est vide, on renvoie sur la page avec une erreur
            return render_template("article.html", id=article.id, error=1)
        else:
            new_comment = Commentary(
                int(current_user.id), int(articleId), str(text))
            db.session.add(new_comment)  # On ajoute l'utilisateur a la bdd
            db.session.commit()
            return json.dumps({'status': 'ok', 'commentAuthor': User.query.filter(User.id == new_comment.userId).one().username, 'commentText': text})
    return json.dumps({'status': 'nope'})


@app.route('/updateArticlePublish/', methods=['POST'])
def updateArticlePublish():
    if request.method == 'POST':
        newContent = request.form['contentName']
        newTitle = request.form['titleName']
        articleId = request.form['articleId']
        now = datetime.utcnow()
        date = ""+now.strftime(
            '%Y')+"-"+now.strftime('%m')+"-"+now.strftime('%d')+" "+now.strftime('%H:%M:%S')  # On met la date sur le bon format de la bdd
        if not newTitle or newTitle == '':  # si le titre est vide, on renvoie sur la page avec une erreur
            return render_template("article.html", id=article.id, error=1)
        else:
            db.session.query(Article).filter_by(id=articleId).update(
                {"title": newTitle, "content": newContent, "date_publication": date, "statut": 1})
            db.session.commit()

            return json.dumps({'status': 'ok', 'articleId': articleId, 'articleTitle': newTitle, 'articleContent': newContent, 'date': date})
    return json.dumps({'status': 'nope'})


@app.route('/updateArticleDraft/', methods=['POST'])
def updateArticleDraft():
    if request.method == 'POST':
        newContent = request.form['contentName']
        newTitle = request.form['titleName']
        articleId = request.form['articleId']
        now = datetime.utcnow()
        date = ""+now.strftime(
            '%Y')+"-"+now.strftime('%m')+"-"+now.strftime('%d')+" "+now.strftime('%H:%M:%S')  # Bon format de la date
        if not newTitle or newTitle == '':  # Check titre vide
            return render_template("article.html", id=article.id, error=1)
        else:
            db.session.query(Article).filter_by(id=articleId).update(
                {"title": newTitle, "content": newContent, "date_revision": date, "statut": 0})
            db.session.commit()

            return json.dumps({'status': 'ok', 'articleId': articleId, 'articleTitle': newTitle, 'articleContent': newContent, 'date': date})
    return json.dumps({'status': 'nope'})


@app.route('/updateComment/', methods=['POST'])
def updateComment():
    if request.method == 'POST':
        commentToUpdate = request.form['id']
        contentToUpdate = request.form['contentComment']
        db.session.query(Commentary).filter_by(id=commentToUpdate).update(
            {'text': contentToUpdate})
        db.session.commit()
        return json.dumps({'status': 'ok', 'id': commentToUpdate, 'content': contentToUpdate})

    return json.dumps({'status': 'nope'})


@app.route('/deleteArticle', methods=['GET'])
def deleteArticle():
    articleToDelete = request.args.get('key') #On récupère l'id de l'article à supprimer
    if request.method == "GET":
        db.session.query(Commentary).filter_by(
            articleId=articleToDelete).delete()
        db.session.query(TagArticle).filter_by(
            articleId=articleToDelete).delete()
        db.session.query(Article).filter_by(id=articleToDelete).delete() # On supprime l'article de la bd
        db.session.commit()
    return json.dumps({'status': 'nope'})


@app.route('/deleteComment', methods=['GET'])
def deleteComment():
    commentToDelete = request.args.get('id') # On récupère l'id du commentaire à supprimer
    if request.method == "GET":
        db.session.query(Commentary).filter_by(
            id=commentToDelete).delete()  # On supprime le commentaire de la bd
        db.session.commit()
        return json.dumps({'status': 'ouaip'})
    return json.dumps({'status': 'nope'})


@app.route('/toggleReactionUser', methods=['GET'])
def toggleReactionUser():
    typeReaction = request.args.get('type')
    articleId = request.args.get('id')
    reactionId = Reaction.query.filter(
        Reaction.description == typeReaction).one().id
    # Si l'utilisateur a deja ajoute cette reaction, on la supprime, sinon on la cree
    if ReactionArticle.query.filter(ReactionArticle.articleId == articleId).filter(ReactionArticle.userId == current_user.id).filter(ReactionArticle.reactionId == reactionId).count() > 0:
        db.session.query(ReactionArticle).filter_by(userId=current_user.id).filter_by(
            articleId=articleId).filter_by(reactionId=reactionId).delete()
        return json.dumps({'status': 'ouaip'})
    else:
        new_reaction = ReactionArticle(
            int(articleId), current_user.id, int(reactionId))
        db.session.add(new_reaction)
        db.session.commit()
        return json.dumps({'status': 'ouaip'})


@app.route('/updateUser/', methods=['POST'])
def updateUser():
    username = request.get_json()[0] # On récupère les données entrées par l'usager
    password = request.get_json()[1]
    firstName = request.get_json()[2]
    lastName = request.get_json()[3]
    email = request.get_json()[4]
    profil = request.get_json()[5]
    id = request.get_json()[6]
    profileId = Profile.query.filter(Profile.name == profil).one().id # On récupère dans la bd l'id du nouveau profil
    db.session.query(User).filter_by(id=id).update(
        {'username': username, 'password': password, 'first_name': firstName, 'last_name': lastName, 'email': email, 'profileId': profileId}) # On effectue les changements demandé par l'usager dans la bd
    db.session.commit()
    return json.dumps({'status': 'yep'})


@app.route('/updateReaction/', methods=['POST'])
def updateReaction():
    loaded = request.get_json()
    reactionId = loaded['id']
    description = loaded['description']
    icone = loaded['icone']
    db.session.query(Reaction).filter_by(id=reactionId).update(
        {'description': description, 'icone': icone})
    db.session.commit()
    return json.dumps({'status': 'yep', 'id': reactionId})


@app.route('/updateTag/', methods=['POST'])
def updateTag():
    loaded = request.get_json()
    tagId = loaded['id']
    name = loaded['name']
    db.session.query(Tag).filter_by(id=tagId).update(
        {'name': name})
    db.session.commit()
    return json.dumps({'status': 'yep', 'id': tagId})


@app.route('/deleteUser/', methods=['GET'])
def deleteUser():
    userToDelete = request.args.get('key') # On récupère l'id du user à supprimer
    if request.method == "GET":
        db.session.query(Article).filter_by(
            userId=userToDelete).delete()
        db.session.query(Commentary).filter_by(
            userId=userToDelete).delete()
        db.session.query(User).filter_by(
            id=userToDelete).delete() # On supprime le user de la bd
        db.session.commit()
    return json.dumps({'status': 'nope'})


@app.route('/addTag/', methods=['POST'])
def addTag():
    tagName = request.form['tagName']
    new_tag = Tag(tagName)
    db.session.add(new_tag)
    db.session.commit()
    return json.dumps({'status': 'yep', 'id': int(new_tag.id), 'name': str(tagName)})


@app.route('/addReaction/', methods=['POST'])
def addReaction():
    reactionName = request.form['reactionName']
    reactionClass = request.form['reactionClass']
    new_reaction = Reaction(reactionName, reactionClass)
    db.session.add(new_reaction)
    db.session.commit()
    return json.dumps({'status': 'yep', 'id': int(new_reaction.id), 'name': str(reactionName), 'icone': str(reactionClass)})


@app.route('/deleteTag', methods=['GET'])
def deleteTag():
    tagId = request.args.get('id')
    db.session.query(Tag).filter(Tag.id == tagId).delete()
    return json.dumps({'status': 'ouaip'})


@app.route('/deleteReaction', methods=['GET'])
def deleteReaction():
    reactionId = request.args.get('id')
    db.session.query(Reaction).filter(Reaction.id == reactionId).delete()
    return json.dumps({'status': 'ouaip'})


if __name__ == '__main__':
    app.run(debug=True)
