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
    galeria = Galerie.query.filter(Galerie.id == foto_id).first()
    return render_template('galerie_content.html', galeria=galeria)

#Galeria: Retorna hub
@main_bps.route('/galerie/hub')
def galerie_hub():
    galerie_db = Galerie.query.all()
    destaque = Galerie.query.order_by(desc(Galerie.created_at)).first()
    
    return render_template('galerie_page.html', galerie_db=galerie_db, destaque=destaque)


#Galeria: Retorna Page
@main_bps.route('/galerie/page')
def galerie_page():
    galerie_types = Gallerie_types.query.all()
    galerie_db = Galerie.query.all()
    home = Sobre.query.all()[0]

    return render_template('galerie_page.html', home=home, galerie_types=galerie_types, galerie_db=galerie_db)

##############################################################

#Noticias: Retorna Page
@main_bps.route('/noticias/page')
def noticias_page():
    noticias_types = News_types.query.all()
    noticias_db = News.query.all()
    home = Sobre.query.all()[0]

    return render_template('news_page.html', home=home, noticias_db=noticias_db, noticias_types=noticias_types)

#Noticias: Retorna hub
@main_bps.route('/noticias/hub/<type_id>')
def noticias_hub(type_id):
    noticias_db = News.query.filter(News.news_type_id == type_id).all()
    destaque = News.query.filter(News.news_type_id == type_id).order_by(desc(News.created_at)).first()

    return render_template('news_hub.html', noticias=noticias_db, destaque=destaque)

#Noticias: Retorna conteudo
@main_bps.route('/noticias/content/<news_id>')
def noticias_content(news_id):
    noticia = News.query.filter(News.id == news_id).first()
    return render_template('news_content.html', noticia=noticia)

#################################################################

#Sobre: Retorna Page
@main_bps.route('/sobre/content/sobre_type')
def sobre_content(sobre_type):
    sobre = Sobre.query.filter(Sobre.tipo == sobre_type).first()
    return render_template('sobre_content.html', sobre=sobre)

#Sobre: Retorna Hub
@main_bps.route('/sobre/page')
def sobre_page():
    sobre_db = Sobre.query.all()
    home = Sobre.query.all()[0]
    return render_template('sobre_page.html', sobre_db=sobre_db, home=home)

################################################################
def configure(app):
    app.register_blueprint(main_bps)
