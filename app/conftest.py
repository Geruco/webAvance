import pytest
from main  import *


#@pytest.fixture(scope="session")
#def app():
#    app = Flask(__name__)

#    ctx = app.app_context()
#    ctx.push()

#    def teardown():
#       ctx.pop()

#    request.addfinalizer(teardown)
#    return app


#@pytest.fixture(scope='function')
#def client(app):
#    with app.test_client() as client:
#        yield client

@pytest.fixture(scope='module')
def new_user():
    user = User(username='untest',
            password='test123',
            first_name='bob',
            last_name='lachance',
            email='bob@outlook.com',
            profileId=3)
    return user

@pytest.fixture(scope='module')
def new_article():
    article = Article(title='Flask',
            content='Contenu de Flask',
            userId = 1)
    return article

@pytest.fixture(scope='module')
def new_commentary():
    commentary = Commentary(text = 'un commentaire',
            userId = 1,
            articleId = 1)
    return commentary

@pytest.fixture(scope='module')
def new_profile():
    profile = Profile(name = 'Administrator')
    return profile

@pytest.fixture(scope='module')
def new_reaction():
    reaction = Reaction(description = 'cardId',
            icone ='fa-id-card')
    return reaction

@pytest.fixture(scope='module')
def new_reactionArticle():
    reactionArticle = ReactionArticle(articleId = 1,
            reactionId = 1,
            userId = 1)
    return reactionArticle

@pytest.fixture(scope='module')
def new_tag():
    tag = Tag(name = 'Pirate')
    return tag

@pytest.fixture(scope='module')
def new_tagArticle():
    tagArticle = TagArticle(articleId = 1,
                tagId= 1)
    return tagArticle