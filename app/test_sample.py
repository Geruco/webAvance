
from app.conftest import *
from app.main import app

#test que l'index est bien accessible
#def test_app(app): 
#    response = app.test_client().get('/index')
#    assert response.status_code == 200

def test_new_user(new_user):
    assert new_user.username == 'untest'
    assert new_user.password == 'test123'
    assert new_user.first_name == 'bob'
    assert new_user.last_name == 'lachance'
    assert new_user.email == 'bob@outlook.com'
    assert new_user.profileId == 3

def test_new_article(new_article):
    assert new_article.title == 'Flask'
    assert new_article.content == 'Contenu de Flask'
    assert new_article.userId == 1

def test_new_commentary(new_commentary):
    assert new_commentary.text == 'un commentaire'
    assert new_commentary.userId == 1
    assert new_commentary.articleId == 1

def test_new_profile(new_profile):
    assert new_profile.name == 'Administrator'

def test_new_reaction(new_reaction):
    assert new_reaction.description == 'cardId'
    assert new_reaction.icone == 'fa-id-card'

def test_new_reactionArticle(new_reactionArticle):
    assert new_reactionArticle.articleId == 1
    assert new_reactionArticle.reactionId == 1
    assert new_reactionArticle.userId == 1

def test_new_tag(new_tag):
    assert new_tag.name == 'Pirate'

def test_new_tagArticle(new_tagArticle):
    assert new_tagArticle.articleId == 1
    assert new_tagArticle.tagId == 1

    
# tests pour voir si pytest fonctionne
#def test_always_passes():
#    assert True

#def test_always_fails():
#    assert False
