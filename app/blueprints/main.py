from flask import Blueprint, render_template
from app.models.models import Home, Galerie, News, Docs

main_bps = Blueprint("main_bps", __name__)


# Routes
@main_bps.route('/')
def index():
    home = Home.query.all()

    return render_template('index.html', home=home)

def galeria():
    galeria = Galerie.query.all()    
    return render_template('galeria.html', galeria=galeria)

def noticias():
    noticias = News.query.all()
    return render_template('noticia.html', noticias=noticias)

def documentos():
    documentos = Docs.query.all()
    return render_template('documentos', documentos=documentos)

def configure(app):
    app.register_blueprint(main_bps)
