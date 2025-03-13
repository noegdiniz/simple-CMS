from flask import Blueprint, render_template
from app.models.models import Sobre, Galerie, News, Docs, Gallerie_types, News_types
from sqlalchemy import desc

main_bps = Blueprint('main_bps', __name__)


###########################################################

# Routes
@main_bps.route('/')
def index():
    home = Sobre.query.all()[0]
    fotos = Galerie.query.order_by(desc(Galerie.created_at)).limit(6).all()
    noticias = News.query.order_by(desc(News.created_at)).limit(6).all()

    return render_template('index.html', home=home, fotos=fotos, noticias=noticias)

############################################################

#Galeria: Retorna conteudo
@main_bps.route('/galerie/content/<foto_id>')
def galerie_content(foto_id):
    galerie_types = Gallerie_types.query.all()
    galeria = Galerie.query.filter(Galerie.id == foto_id).first()
    return render_template('galerie_content.html', galeria=galeria, galerie_types=galerie_types)

#Galeria: Retorna Page
@main_bps.route('/galerie/page/<type_id>')
@main_bps.route('/galerie/page')
def galerie_page(type_id=None):
    galerie_types = Gallerie_types.query.all()

    if type_id:
        galerie_db = Galerie.query.filter(Galerie.gallerie_type_id == type_id).all()
    else:
        galerie_db = Galerie.query.all()

    home = Sobre.query.all()[0]

    return render_template('galerie_page.html', home=home,type_id=type_id, galerie_types=galerie_types, galerie_db=galerie_db)

##############################################################

#Noticias: Retorna Page
@main_bps.route('/noticias/page/<type_id>')
@main_bps.route('/noticias/page')
def noticias_page(type_id = None):
    noticias_types = News_types.query.all()
    if type_id:
        noticias_db = News.query.filter(News.news_type_id == type_id).all()
    else:
        noticias_db = News.query.all()

    home = Sobre.query.all()[0]

    return render_template('news_page.html', home=home, noticias_db=noticias_db, noticias_types=noticias_types)


#Noticias: Retorna conteudo
@main_bps.route('/noticias/content/<news_id>')
def noticias_content(news_id):
    noticias_types = News_types.query.all()
    noticia = News.query.filter(News.id == news_id).first()

    return render_template('news_content.html', noticia=noticia, noticias_types=noticias_types)

#################################################################

#Sobre: Retorna Hub
@main_bps.route('/sobre/page')
def sobre_page():
    sobre_db = Sobre.query.all()[1:]
    home = Sobre.query.all()[0]
    return render_template('sobre_page.html', sobre_db=sobre_db, home=home)

################################################################
def configure(app):
    app.register_blueprint(main_bps)
