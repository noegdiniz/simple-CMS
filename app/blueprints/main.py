from flask import Blueprint, render_template, abort
from app.models.models import Sobre, Galerie, News, Docs, Gallerie_types, News_types
from sqlalchemy import desc

main_bps = Blueprint('main_bps', __name__)

###########################################################

# Routes
@main_bps.route('/')
def index():
    home = Sobre.query.first()
    fotos = Galerie.query.join(Gallerie_types, Galerie.gallerie_type_id == Gallerie_types.id).filter(Gallerie_types.publico == True).order_by(desc(Galerie.created_at)).limit(6).all()
    noticias = News.query.join(News_types, News.news_type_id == News_types.id).filter(News_types.publico == True).order_by(desc(News.created_at)).limit(6).all()
    
    titulo_padrao = Sobre.query.offset(1).first()
    return render_template('index.html', home=home, fotos=fotos, noticias=noticias, titulo_padrao=titulo_padrao)

############################################################

#Galeria: Retorna conteudo
@main_bps.route('/galerie/content/<foto_id>')
def galerie_content(foto_id):
    galerie_types = Gallerie_types.query.all()
    galeria = Galerie.query.filter(Galerie.id == foto_id).join(Gallerie_types).filter(Gallerie_types.publico == True).first()
    if not galeria:
        abort(404)
    
    titulo_padrao = Sobre.query.offset(1).first()
    return render_template('galerie_content.html', galeria=galeria, galerie_types=galerie_types, titulo_padrao=titulo_padrao)

#Galeria: Retorna Page
@main_bps.route('/galerie/page/<type_id>')
@main_bps.route('/galerie/page')
def galerie_page(type_id=None):
    galerie_types = Gallerie_types.query.all()

    if type_id:
        galerie_db = Galerie.query.filter(Galerie.gallerie_type_id == type_id).join(Gallerie_types).filter(Gallerie_types.publico == True).all()
    else:
        galerie_db = Galerie.query.join(Gallerie_types).filter(Gallerie_types.publico == True).all()

    titulo_padrao = Sobre.query.offset(1).first()
    return render_template('galerie_page.html', type_id=type_id, galerie_types=galerie_types, galerie_db=galerie_db, titulo_padrao=titulo_padrao)

##############################################################

#Noticias: Retorna Page
@main_bps.route('/noticias/page/<type_id>')
@main_bps.route('/noticias/page')
def noticias_page(type_id=None):
    noticias_types = News_types.query.all()
    if type_id:
        noticias_db = News.query.filter(News.news_type_id == type_id).all()
    else:
        noticias_db = News.query.join(News_types).filter(News_types.publico == True).all()

    titulo_padrao = Sobre.query.offset(1).first()
    return render_template('news_page.html', type_id=type_id, noticias_db=noticias_db, noticias_types=noticias_types, titulo_padrao=titulo_padrao)


#Noticias: Retorna conteudo
@main_bps.route('/noticias/content/<news_id>')
def noticias_content(news_id):
    noticias_types = News_types.query.all()
    noticia = News.query.filter(News.id == news_id).join(News_types).filter(News_types.publico == True).first()
    if not noticia:
        abort(404)

    titulo_padrao = Sobre.query.offset(1).first()
    return render_template('news_content.html', noticia=noticia, noticias_types=noticias_types, titulo_padrao=titulo_padrao)

#################################################################

#Sobre: Retorna Hub
@main_bps.route('/sobre/page/<id>')
@main_bps.route('/sobre/page')
def sobre_page(id=None):
    sobre_db = Sobre.query.offset(1).all()

    if id:
        sobre = Sobre.query.filter(Sobre.id == id).first()
        if not sobre:
            abort(404)
    else:
        sobre = None

    return render_template('sobre_page.html', sobre_db=sobre_db, sobre=sobre)

################################################################
def configure(app):
    app.register_blueprint(main_bps)
